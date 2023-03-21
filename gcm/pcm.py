from pathlib import Path

from netCDF4 import Dataset
import numpy as np

from gcm.abstract import AbstractSimulation


class PlanetaryClimateModelSimulation(AbstractSimulation):
    """An object that pulls data from PCM simulations.

    Parameters
    ----------
    version
    mars_year

    Notes
    -----
    These files are broken into 12 files that are each 1 "month". For this object I made a few changes from their
    native format:

    1. I concatenate arrays so each array accessed by this object covers the entire Mars year.
    2. I reshape the time axis to be [sol, local time]
    3. I remove the extra duplicate grid point. The longitude axis has shape (65,) where the first and last points
       are identical, so I only keep the first copy
    4. I roll the data such that the data go from 0 to 360. Though with their grid, it's more like 357 to 357.
    """

    def __init__(self, version: int, mars_year: int):
        self._location = self._make_simulation_files_location(version, mars_year)
        self._monthly_datasets = self._load_monthly_datasets()

    @staticmethod
    def _make_simulation_files_location(version: int, mars_year: int):
        location = Path('/media/kyle/iuvs/gcm/pcm') / f'v{version:02}' / f'my{mars_year:02}'
        if not location.exists():
            raise NotADirectoryError('The request files are not in a directory that exists.')
        return location

    def _load_monthly_datasets(self):
        files = self._location.glob('diagfi*.nc')
        return [Dataset(f) for f in files]

    def get_latitude_centers(self):
        return self._monthly_datasets[0]['latitude'][:].data

    def get_latitude_edges(self) -> np.ndarray:
        """Get the latitude edges.

        These values are not natively in the simulations, so I create them myself. Note at the poles, these values
        wrap around the pole.

        Returns
        -------

        """
        centers = self.get_latitude_centers()
        grid_difference = np.abs(np.diff(centers))[0]
        return np.concatenate((centers + grid_difference/2, [centers[-1] - grid_difference/2]))

    def get_longitude_centers(self):
        lon = self._monthly_datasets[0]['longitude'][:-1].data % 360
        lon = np.roll(lon, lon.shape[0]//2, axis=-1)
        return np.append(lon, 360)

    def get_longitude_edges(self) -> np.ndarray:
        centers = self.get_longitude_centers()
        grid_difference = np.abs(np.diff(centers))[0]
        return np.concatenate(([centers[0] - grid_difference/2], centers + grid_difference/2))

    def get_surface_pressure(self):
        ps = np.vstack([f['ps'][:, :, :-1].data for f in self._monthly_datasets])
        ps = np.reshape(ps, (ps.shape[0] // 24, 24, ps.shape[1], ps.shape[2]))
        ps = np.roll(ps, ps.shape[-1]//2, axis=-1)
        return np.concatenate((ps, ps[:, :, :, 0][..., None]), axis=-1)

    def get_surface_temperature(self):
        ts = np.vstack([f['tsurf'][:, :, :-1].data for f in self._monthly_datasets])
        ts = np.reshape(ts, (ts.shape[0]//24, 24, ts.shape[1], ts.shape[2]))
        ts = np.roll(ts, ts.shape[-1] // 2, axis=-1)
        return np.concatenate((ts, ts[:, :, :, 0][..., None]), axis=-1)

    def get_atmospheric_pressure(self):
        # This array takes up over 1GB or RAM so I'm not making it until I have a reason to
        pass

    def get_atmospheric_temperature(self):
        # This array takes up over 1GB or RAM so I'm not making it until I have a reason to
        pass

    def get_dust_ultraviolet_column_optical_depth(self):
        tau_dust = np.vstack([f['tau_dust'][:, :, :-1].data for f in self._monthly_datasets])
        tau_dust = np.reshape(tau_dust, (tau_dust.shape[0] // 24, 24, tau_dust.shape[1], tau_dust.shape[2]))
        tau_dust = np.roll(tau_dust, tau_dust.shape[-1] // 2, axis=-1)
        return np.concatenate((tau_dust, tau_dust[:, :, :, 0][..., None]), axis=-1)

    def get_ice_ultraviolet_column_optical_depth(self):
        tau_h2o_ice = np.vstack([f['tau_h2o_ice'][:, :, :-1].data for f in self._monthly_datasets])
        tau_h2o_ice = np.reshape(tau_h2o_ice, (tau_h2o_ice.shape[0] // 24, 24, tau_h2o_ice.shape[1], tau_h2o_ice.shape[2]))
        tau_h2o_ice = np.roll(tau_h2o_ice, tau_h2o_ice.shape[-1] // 2, axis=-1)
        return np.concatenate((tau_h2o_ice, tau_h2o_ice[:, :, :, 0][..., None]), axis=-1)
