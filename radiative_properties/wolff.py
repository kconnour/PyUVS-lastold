from astropy.io import fits
import numpy as np


class RadiativeProperties:
    """An object that can extract various pieces of data from Mike Wolff's standard radiative property data file format.

    Parameters
    ----------
    hdul
        The hdulist

    Raises
    ------
    KeyError
        Raised if the file does not have all the expected fields
    TypeError
        Raised if the input is not an hdulist
    ValueError
        Raised if any of the input values in the hdulist are not as I expect.

    """
    def __init__(self, hdul: fits.hdu.hdulist.HDUList):
        self.hdul = hdul

    def _get_file_forward_scattering_properties(self) -> np.ndarray:
        return self.hdul['forw'].data

    def _get_file_legendre_coefficients(self) -> np.ndarray:
        return self.hdul['pmom'].data

    def _get_file_phase_function(self) -> np.ndarray:
        return self.hdul['phsfn'].data

    def _get_file_phase_function_reexpansion(self) -> np.ndarray:
        return self.hdul['expansion'].data

    def get_primary(self) -> np.ndarray:
        return self.hdul['primary'].data

    def get_particle_sizes(self) -> np.ndarray:
        return self.hdul['particle_sizes'].data

    def get_wavelengths(self) -> np.ndarray:
        return self.hdul['wavelengths'].data

    def get_scattering_angles(self) -> np.ndarray:
        return self.hdul['scattering_angle'].data

    def get_scattering_cross_section(self) -> np.ndarray:
        return self._get_file_forward_scattering_properties()[..., 1]

    def get_extinction_cross_section(self) -> np.ndarray:
        return self._get_file_forward_scattering_properties()[..., 0]

    def get_asymmetry_parameter(self) -> np.ndarray:
        return self._get_file_forward_scattering_properties()[..., 2]

    def get_phase_function(self) -> np.ndarray:
        return np.moveaxis(self._get_file_phase_function(), 0, -1)

    def get_legendre_coefficients(self) -> np.ndarray:
        return np.moveaxis(self._get_file_legendre_coefficients(), 0, -1)

    def get_phase_function_reexpansion(self) -> np.ndarray:
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
