from pathlib import Path

from astropy.io import fits
import numpy as np

from radiative_properties.abstract import AbstractRadiativeProperties


class WolffRadiativeProperties(AbstractRadiativeProperties):
    """An object that can extract various pieces of data from Mike Wolff's standard radiative property data file format.

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
        self._location = Path('/media/kyle/iuvs/radiative_properties/wolff')
        self.hdul = self._open_file(aerosol, version)

    def _open_file(self, aerosol: str, version: int):
        file_pattern = f'{aerosol}{version:02}*'
        filepath = list(self._location.glob(file_pattern))
        if not filepath:
            raise FileNotFoundError(f'Cannot find a file with at location {self._location}')
        return fits.open(filepath[0])

    def _get_file_forward_scattering_properties(self) -> np.ndarray:
        return self.hdul['forw'].data

    def _get_file_legendre_coefficients(self) -> np.ndarray:
        return self.hdul['pmom'].data

    def _get_file_phase_function(self) -> np.ndarray:
        return self.hdul['phsfn'].data

    def _get_file_phase_function_reexpansion(self) -> np.ndarray:
        return self.hdul['expansion'].data

    def get_primary(self) -> np.ndarray:
        """Get the primary hdul.

        Returns
        -------
        The primary structure

        Notes
        -----
        This array should contain no relevant info.

        """
        return self.hdul['primary'].data

    def get_particle_sizes(self) -> np.ndarray:
        """Get the particle sizes associated with each of the radiative properties.

        Returns
        -------
        The particle sizes

        Notes
        -----
        The particle sizes are the centers of some particle size distribution.

        """
        return self.hdul['particle_sizes'].data

    def get_wavelengths(self) -> np.ndarray:
        return self.hdul['wavelengths'].data

    def get_scattering_angles(self) -> np.ndarray:
        return self.hdul['scattering_angle'].data

    def get_scattering_cross_sections(self) -> np.ndarray:
        return self._get_file_forward_scattering_properties()[..., 1]

    def get_extinction_cross_sections(self) -> np.ndarray:
        return self._get_file_forward_scattering_properties()[..., 0]

    def get_asymmetry_parameters(self) -> np.ndarray:
        return self._get_file_forward_scattering_properties()[..., 2]

    def get_phase_functions(self) -> np.ndarray:
        return np.moveaxis(self._get_file_phase_function(), 0, -1)

    def get_legendre_coefficients(self) -> np.ndarray:
        return np.moveaxis(self._get_file_legendre_coefficients(), 0, -1)

    def get_phase_function_reexpansions(self) -> np.ndarray:
        return np.moveaxis(self._get_file_phase_function_reexpansion(), 0, -1)

    def _get_header(self) -> fits.header.Header:
        return self.hdul['primary'].header

    def get_file_creation_date(self) -> str:
        header = self._get_header()
        return header['date']

    def get_history(self) -> str:
        header = self._get_header()
        history = str(header['history'])
        # The ??? currently only applies to the dust file
        return history.replace('???', '--')
