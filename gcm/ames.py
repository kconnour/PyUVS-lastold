from netCDF4 import Dataset
import numpy as np

from radiative_properties.radprop import AbstractRadiativeProperties


class FixedSimulation:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def get_latitude_centers(self) -> np.ndarray:
        return self.dataset['lat'][:].data

    def get_latitude_edges(self) -> np.ndarray:
        return np.unique(self.dataset['grid_yt_bnds'][:].data)

    def get_longitude_centers(self) -> np.ndarray:
        return self.dataset['lon'][:].data

    def get_longitude_edges(self) -> np.ndarray:
        return np.unique(self.dataset['grid_xt_bnds'][:].data)

    def get_surface_elevation(self) -> np.ndarray:
        return self.dataset['zsurf'][:].data

    def get_surface_albedo(self) -> np.ndarray:
        return self.dataset['alb'][:].data

    def get_ak(self) -> np.ndarray:
        return self.dataset['pk'][:].data

    def get_bk(self) -> np.ndarray:
        return self.dataset['bk'][:].data

    # To add: thin, emis, gice, phalf


class AverageSimulation:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def get_visible_dust_optical_depth(self):
        return self.dataset['taudust_VIS'][:].data

    def get_visible_ice_optical_depth(self):
        return self.dataset['taucloud_VIS'][:].data


# TODO: they don't currently give me particle size info so I'm assuming a constant value. In the future, I should
#  use the values they give me instead of making up values (used when computing the dust and ice optical depths)
class DiurnalSimulation:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def get_simulation_sol_centers(self):
        return self.dataset['time'][:].data

    def get_simulation_sol_edges(self) -> np.ndarray:
        return np.unique(self.dataset['time_bnds'][:].data)

    def get_yearly_sol_centers(self):
        return np.mod(self.get_simulation_sol_centers(), 668)

    def get_yearly_sol_edges(self):
        return np.mod(self.get_simulation_sol_edges(), 668)

    def get_local_time_centers(self):
        return self.dataset['time_of_day_24'][:].data

    def get_local_time_edges(self):
        return np.unique(self.dataset['time_of_day_edges_24'][:].data)

    def get_solar_longitude_centers(self):
        return np.mod(self.dataset['areo'][:].data, 360)

    def get_surface_pressure(self):
        return self.dataset['ps'][:].data

    def get_surface_temperature(self):
        return self.dataset['ts'][:].data

    def get_atmospheric_temperature(self):
        return np.moveaxis(self.dataset['temp'][:].data, 2, -1)

    def get_dust_extinction_optical_depth_per_pascal(self) -> np.ndarray:
        return np.moveaxis(self.dataset['dustref'][:].data, 2, -1)

    def get_ice_absorption_optical_depth_per_pascal(self) -> np.ndarray:
        return np.moveaxis(self.dataset['cldref'][:].data, 2, -1)

    def get_atmospheric_pressure(self, grid: FixedSimulation):
        surface_pressure = self.get_surface_pressure()
        ak = grid.get_ak()
        bk = grid.get_bk()
        return np.multiply.outer(surface_pressure, bk) + ak

    def get_dust_column_optical_depth(self, grid: FixedSimulation, radprop: AbstractRadiativeProperties, target_wavelength: float, reference_wavelength: float = 0.690, particle_size: float = 1.2):
        simulation_extinction_optical_depth = self.get_dust_extinction_optical_depth_per_pascal()
        simulation_particle_sizes = np.ones(simulation_extinction_optical_depth.shape) * particle_size

        scaled_optical_depth = self._scale_extinction_optical_depth_to_target_wavelengths(
            simulation_extinction_optical_depth, simulation_particle_sizes, reference_wavelength, radprop,
            target_wavelength)

        return self._compute_optical_depth(scaled_optical_depth, grid)

    def get_ice_column_optical_depth(self, grid: FixedSimulation, radprop: AbstractRadiativeProperties, target_wavelength: float, reference_wavelength: float = 12, particle_size: float = 1.5):
        simulation_absorption_optical_depth = self.get_ice_absorption_optical_depth_per_pascal()
        simulation_particle_sizes = np.ones(simulation_absorption_optical_depth.shape) * particle_size

        # Convert absorption to extinction
        reference_wavelength_index = self._get_closest_index(radprop.get_wavelengths(), reference_wavelength)
        scaling_factor = radprop.get_extinction_cross_sections()[:, reference_wavelength_index] / \
                         radprop.get_absorption_cross_sections()[:, reference_wavelength_index]
        absorption_to_extinction_factor = np.interp(simulation_particle_sizes, radprop.get_particle_sizes(), scaling_factor)
        simulation_extinction_optical_depth = simulation_absorption_optical_depth * absorption_to_extinction_factor

        scaled_optical_depth = self._scale_extinction_optical_depth_to_target_wavelengths(
            simulation_extinction_optical_depth, simulation_particle_sizes, reference_wavelength, radprop,
            target_wavelength)

        return self._compute_optical_depth(scaled_optical_depth, grid)

    def _scale_extinction_optical_depth_to_target_wavelengths(self,
            simulation_extinction_optical_depth: np.ndarray,
            simulation_particle_sizes: np.ndarray,
            simulation_reference_wavelength: float,
            radprop: AbstractRadiativeProperties,
            target_wavelength: float) -> np.ndarray:

        radprop_particle_sizes = radprop.get_particle_sizes()
        radprop_wavelengths = radprop.get_wavelengths()
        radprop_extinction_cross_sections = radprop.get_extinction_cross_sections()

        target_wavelength_index = self._get_closest_index(radprop_wavelengths, target_wavelength)
        reference_wavelength_index = self._get_closest_index(radprop_wavelengths, simulation_reference_wavelength)

        target_cext = radprop_extinction_cross_sections[:, target_wavelength_index]
        reference_cext = radprop_extinction_cross_sections[:, reference_wavelength_index]

        scaling_factor = np.interp(simulation_particle_sizes, radprop_particle_sizes, target_cext / reference_cext)
        return simulation_extinction_optical_depth * scaling_factor

    @staticmethod
    def _get_closest_index(array: np.ndarray, value: float) -> int:
        return np.abs(array - value).argmin()

    def _compute_optical_depth(self, simulation_optical_depth: np.ndarray, grid: FixedSimulation) -> np.ndarray:
        atmospheric_pressure = self.get_atmospheric_pressure(grid)
        p_diff = np.diff(atmospheric_pressure, axis=-1)
        return np.sum(simulation_optical_depth * p_diff, axis=-1)
