from pathlib import Path

import numpy as np

from radiative_properties.abstract import AbstractRadiativeProperties


def make_dust_file() -> None:
    """Make the dust file.

    Ames provided me a file in the strangest format. This allows me to pretend that they originally gave me this
    saner file.

    Returns
    -------
    None

    """
    dust_vis = np.genfromtxt('/media/kyle/iuvs/radiative_properties/ames/raw/Dust_vis_wolff2010_JD_12bands.dat')
    dust_ir = np.genfromtxt('/media/kyle/iuvs/radiative_properties/ames/raw/Dust_ir_wolff2010_JD_12bands.dat')
    dust = np.hstack((dust_vis, dust_ir))
    np.save('/media/kyle/iuvs/radiative_properties/ames/Dust_wolff2010_JD_12bands.dat', dust)


def make_ice_file() -> None:
    """Make the ice file.

    Ames provided me a file in the strangest format. This allows me to pretend that they originally gave me this
    saner file.

    Returns
    -------
    None

    """
    ice_vis = np.genfromtxt('/media/kyle/iuvs/radiative_properties/ames/raw/waterCoated_vis_JD_12bands.dat')
    ice_ir = np.genfromtxt('/media/kyle/iuvs/radiative_properties/ames/raw/waterCoated_ir_JD_12bands.dat')
    ice = np.hstack((ice_vis, ice_ir))
    np.save('/media/kyle/iuvs/radiative_properties/ames/waterCoated_JD_12bands.dat', ice)


class AmesRadiativeProperties(AbstractRadiativeProperties):
    """An object that can extract various pieces of data from NASA Ames' standard radiative property data file format.

    Parameters
    ----------
    aerosol
        The aerosol to get the radiative properties of. Can be "dust" or "ice".
    version
        The version of the aerosol's radiative properties.

    Raises
    ------
    FileNotFoundError
        Raised if the input aerosol and version don't point to a valid file.

    """
    def __init__(self, aerosol: str, version: int):
        self._location = Path('/media/kyle/iuvs/radiative_properties/ames')
        self.radprop = self.open_file(aerosol, version)

    def open_file(self, aerosol: str, version: int):
        file_pattern = f'{aerosol}{version:02}*'
        filepath = list(self._location.glob(file_pattern))
        if not filepath:
            raise FileNotFoundError(f'Cannot find a file with at location {self._location}')
        return np.load(str(filepath[0]))

    def get_particle_size_centers(self) -> np.ndarray:
        bins = self.radprop.shape[0] // 3
        centers = np.zeros((bins,))
        centers[0] = 1e-7
        centers[-1] = 50e-6

        variance_psizes = np.exp(np.log(50e-6 / 1e-7) / (bins - 1) * 3)

        for i in range(bins - 1):
            centers[i + 1] = centers[i] * variance_psizes ** (1 / 3)
        return centers * 10 ** 6

    def get_particle_size_edges(self) -> np.ndarray:
        bins = self.radprop.shape[0] // 3

        boundaries = np.zeros((bins + 1,))
        boundaries[0] = 1e-9
        boundaries[-1] = 1e-2

        variance_psizes = np.exp(np.log(50e-6 / 1e-7) / (bins - 1) * 3)

        centers = self.get_particle_size_centers()

        for i in range(bins - 1):
            boundaries[i + 1] = ((2 * variance_psizes) / (variance_psizes + 1)) ** (1 / 3) * centers[i]
        return boundaries * 10 ** 6

    def get_particle_sizes(self) -> np.ndarray:
        return self.get_particle_size_centers()

    @staticmethod
    def wavenumber_to_wavelength(wavenumber: np.ndarray) -> np.ndarray:
        return 10**4 / wavenumber

    @staticmethod
    def get_wavenumber_edges() -> np.ndarray:
        """Get the wavenumber edges [1/cm]

        Returns
        -------
        The wavenumber edges.

        """
        return np.array([41666.67, 25000, 12500, 7651.11, 5370.57, 4030.63, 3087.37, 2222.22, 1250, 833.333, 416.667,
                         166.667, 10])

    def get_wavelength_edges(self) -> np.ndarray:
        # In microns
        return self.wavenumber_to_wavelength(self.get_wavenumber_edges())

    def get_wavelength_centers(self) -> np.ndarray:
        edges = self.get_wavelength_edges()
        return (edges[1:] + edges[:-1]) / 2

    def get_wavelengths(self) -> np.ndarray:
        return self.get_wavelength_centers()

    def get_scattering_cross_sections(self) -> np.ndarray:
        indices = np.arange(self.radprop.shape[0] // 3) * 3 + 1
        return self.radprop[indices]

    def get_extinction_cross_sections(self) -> np.ndarray:
        indices = np.arange(self.radprop.shape[0] // 3) * 3
        return self.radprop[indices]

    def get_asymmetry_parameters(self) -> np.ndarray:
        indices = np.arange(self.radprop.shape[0] // 3) * 3 + 2
        return self.radprop[indices]
