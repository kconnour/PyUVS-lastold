from pathlib import Path

from netCDF4 import Dataset
import numpy as np

from gcm.abstract import AbstractSimulation


class AmesSimulation(AbstractSimulation):
    def __init__(self, version: int, mars_year: int):
        self._location = self._make_simulation_files_location(version, mars_year)
        self._fixed = self._load_fixed()
        self._atmos_average = self._load_atmos_average()
        self._atmos_diurn = self._load_atmos_diurn()

    @staticmethod
    def _make_simulation_files_location(version: int, mars_year: int):
        location = Path('/media/kyle/iuvs/gcm/ames') / f'v{version:02}' / f'my{mars_year:02}'
        if not location.exists():
            raise NotADirectoryError('The request files are not in a directory that exists.')
        return location

    def _load_fixed(self):
        return Dataset(list(self._location.glob('*fixed.nc'))[0])

    def _load_atmos_average(self):
        return Dataset(list(self._location.glob('*atmos_average.nc'))[0])

    def _load_atmos_diurn(self):
        return Dataset(list(self._location.glob('*atmos_diurn.nc'))[0])

    def get_latitude_centers(self) -> np.ndarray:
        return self._fixed['lat'][:].data

    def get_latitude_edges(self) -> np.ndarray:
        return np.unique(self._fixed['grid_yt_bnds'][:].data)

    def get_longitude_centers(self) -> np.ndarray:
        return self._fixed['lon'][:].data

    def get_longitude_edges(self) -> np.ndarray:
        return np.unique(self._fixed['grid_xt_bnds'][:].data)

    def get_surface_elevation(self) -> np.ndarray:
        return self._fixed['zsurf'][:].data

    def get_surface_albedo(self) -> np.ndarray:
        return self._fixed['alb'][:].data

    def get_ak(self) -> np.ndarray:
        return self._fixed['pk'][:].data

    def get_bk(self) -> np.ndarray:
        return self._fixed['bk'][:].data

    # To add from fixed: thin, emis, gice, phalf

    def get_simulation_sol_centers(self):
        return self._atmos_diurn['time'][:].data

    def get_simulation_sol_edges(self) -> np.ndarray:
        return np.unique(self._atmos_diurn['time_bnds'][:].data)

    def get_yearly_sol_centers(self):
        return np.mod(self.get_simulation_sol_centers(), 668)

    def get_yearly_sol_edges(self):
        return np.mod(self.get_simulation_sol_edges(), 668)

    def get_local_time_centers(self):
        return self._atmos_diurn['time_of_day_24'][:].data

    def get_local_time_edges(self):
        return np.unique(self._atmos_diurn['time_of_day_edges_24'][:].data)

    def get_solar_longitude_centers(self):
        return np.mod(self._atmos_diurn['areo'][:].data, 360)

    def get_surface_pressure(self):
        return self._atmos_diurn['ps'][:].data

    def get_surface_temperature(self):
        return self._atmos_diurn['ts'][:].data

    def get_atmospheric_temperature(self):
        return np.moveaxis(self._atmos_diurn['temp'][:].data, 2, -1)

    def get_dust_visible_extinction_optical_depth_per_pascal(self) -> np.ndarray:
        return np.moveaxis(self._atmos_diurn['dustref'][:].data, 2, -1)

    def get_ice_visible_extinction_optical_depth_per_pascal(self) -> np.ndarray:
        return np.moveaxis(self._atmos_diurn['cldref'][:].data, 2, -1)

    def get_atmospheric_pressure(self):
        surface_pressure = self.get_surface_pressure()
        ak = self.get_ak()
        bk = self.get_bk()
        return np.multiply.outer(surface_pressure, bk) + ak

    def get_dust_visible_column_optical_depth(self):
        visible_opacity = self.get_dust_visible_extinction_optical_depth_per_pascal()
        return self._compute_optical_depth(visible_opacity)

    def get_ice_visible_column_optical_depth(self):
        visible_opacity = self.get_ice_visible_extinction_optical_depth_per_pascal()
        return self._compute_optical_depth(visible_opacity)

    @staticmethod
    def _get_closest_index(array: np.ndarray, value: float) -> int:
        return np.abs(array - value).argmin()

    def _compute_optical_depth(self, simulation_optical_depth: np.ndarray) -> np.ndarray:
        atmospheric_pressure = self.get_atmospheric_pressure()
        p_diff = np.diff(atmospheric_pressure, axis=-1)
        return np.sum(simulation_optical_depth * p_diff, axis=-1)


if __name__ == '__main__':
    sim = AmesSimulation(2, 30)
    print(sim.get_latitude_edges())
    print(sim.get_latitude_centers())
