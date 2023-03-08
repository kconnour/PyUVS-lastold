from astropy.io import fits
import numpy as np


class RadpropFile:
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
        self._raise_errors_if_input_file_is_not_as_expected()

    def _raise_errors_if_input_file_is_not_as_expected(self):
        self._raise_type_error_if_input_is_not_hdulist()
        self._raise_key_error_if_expected_records_are_not_present()
        self._raise_value_error_if_input_arrays_do_not_have_expected_shapes()
        self._raise_value_error_if_unphysical_vales_are_present()

    def _raise_type_error_if_input_is_not_hdulist(self):
        if not isinstance(self.hdul, fits.hdu.hdulist.HDUList):
            raise TypeError(f'The input (type={type(self.hdul)} is not an hdulist.')

    def _raise_key_error_if_expected_records_are_not_present(self):
        expected_records = ['primary', 'forw', 'pmom', 'phsfn', 'expansion', 'particle_sizes', 'wavelengths',
                            'scattering_angle']
        validation = []
        for record in expected_records:
            validation.append(record in self.hdul)

        if not all(validation):
            raise KeyError('Some expected fields are not present.')

    def _raise_value_error_if_input_arrays_do_not_have_expected_shapes(self):
        self._raise_value_error_if_input_particle_sizes_are_not_one_dimensional()
        self._raise_value_error_if_input_wavelengths_are_not_one_dimensional()
        self._raise_value_error_if_input_scattering_angles_are_not_one_dimensional()

        self._raise_value_error_if_input_forward_scattering_properties_have_unexpected_dimensions()
        self._raise_value_error_if_input_legendre_coefficients_have_unexpected_dimensions()
        self._raise_value_error_if_input_phase_function_have_unexpected_dimensions()
        self._raise_value_error_if_input_phase_function_reexpansion_have_unexpected_dimensions()

    def _raise_value_error_if_input_particle_sizes_are_not_one_dimensional(self):
        particle_sizes = self.get_particle_sizes()
        if np.ndim(particle_sizes) != 1:
            raise ValueError('The particle sizes are not 1-dimensional.')

    def _raise_value_error_if_input_wavelengths_are_not_one_dimensional(self):
        wavelengths = self.get_wavelengths()
        if np.ndim(wavelengths) != 1:
            raise ValueError('The wavelengths are not 1-dimensional.')

    def _raise_value_error_if_input_scattering_angles_are_not_one_dimensional(self):
        angles = self.get_scattering_angles()
        if np.ndim(angles) != 1:
            raise ValueError('The scattering angles are not 1-dimensional.')

    def _raise_value_error_if_input_forward_scattering_properties_have_unexpected_dimensions(self):
        forw = self._get_file_forward_scattering_properties()
        if np.ndim(forw) != 3:
            raise ValueError('The forward scattering properties are not 3-dimensional.')

        particle_sizes = self.get_particle_sizes()
        wavelengths = self.get_wavelengths()

        if forw.shape[0] != particle_sizes.shape[0]:
            message = f'The forward scattering properties\' particle size axis (len={forw.shape[0]}) does not match ' \
                      f'the particle size grid (len={particle_sizes.shape[0]}).'
            raise ValueError(message)
        if forw.shape[1] != wavelengths.shape[0]:
            message = f'The forward scattering properties\' wavelength axis (len={forw.shape[1]}) does not match ' \
                      f'the wavelength grid (len={wavelengths.shape[0]}).'
            raise ValueError(message)
        if forw.shape[2] != 3:
            message = f'The forward scattering properties\' property axis (len={forw.shape[2]}) is not of length 3.'
            raise ValueError(message)

    def _raise_value_error_if_input_legendre_coefficients_have_unexpected_dimensions(self):
        pmom = self._get_file_legendre_coefficients()
        if np.ndim(pmom) != 3:
            raise ValueError('The Legendre coefficients are not 3-dimensional.')

        particle_sizes = self.get_particle_sizes()
        wavelengths = self.get_wavelengths()

        if pmom.shape[1] != particle_sizes.shape[0]:
            message = f'The Legendre coefficients\' particle size axis (len={pmom.shape[1]}) does not match ' \
                      f'the particle size grid (len={particle_sizes.shape[0]}).'
            raise ValueError(message)
        if pmom.shape[2] != wavelengths.shape[0]:
            message = f'The Legendre coefficients\' wavelength axis (len={pmom.shape[2]}) does not match ' \
                      f'the wavelength grid (len={wavelengths.shape[0]}).'
            raise ValueError(message)

    def _raise_value_error_if_input_phase_function_have_unexpected_dimensions(self):
        phsfn = self._get_file_phase_function()
        if np.ndim(phsfn) != 3:
            raise ValueError('The phase function is not 3-dimensional.')

        particle_sizes = self.get_particle_sizes()
        wavelengths = self.get_wavelengths()
        scattering_angles = self.get_scattering_angles()

        if phsfn.shape[0] != scattering_angles.shape[0]:
            message = f'The phase function\'s scattering angle axis (len={phsfn.shape[0]}) does not match ' \
                      f'the scattering angle grid (len={scattering_angles.shape[0]}).'
            raise ValueError(message)
        if phsfn.shape[1] != particle_sizes.shape[0]:
            message = f'The phase function\'s particle size axis (len={phsfn.shape[1]}) does not match ' \
                      f'the particle size grid (len={particle_sizes.shape[0]}).'
            raise ValueError(message)
        if phsfn.shape[2] != wavelengths.shape[0]:
            message = f'The phase function\'s wavelength axis (len={phsfn.shape[2]}) does not match ' \
                      f'the wavelength grid (len={wavelengths.shape[0]}).'
            raise ValueError(message)

    def _raise_value_error_if_input_phase_function_reexpansion_have_unexpected_dimensions(self):
        phsfn = self._get_file_phase_function_reexpansion()
        if np.ndim(phsfn) != 3:
            raise ValueError('The phase function re-expansion is not 3-dimensional.')

        particle_sizes = self.get_particle_sizes()
        wavelengths = self.get_wavelengths()
        scattering_angles = self.get_scattering_angles()

        if phsfn.shape[0] != scattering_angles.shape[0]:
            message = f'The phase function re-expansion\'s scattering angle axis (len={phsfn.shape[0]}) does not match ' \
                      f'the scattering angle grid (len={scattering_angles.shape[0]}).'
            raise ValueError(message)
        if phsfn.shape[1] != particle_sizes.shape[0]:
            message = f'The phase function re-expansion\'s particle size axis (len={phsfn.shape[1]}) does not match ' \
                      f'the particle size grid (len={particle_sizes.shape[0]}).'
            raise ValueError(message)
        if phsfn.shape[2] != wavelengths.shape[0]:
            message = f'The phase function re-expansion\'s wavelength axis (len={phsfn.shape[2]}) does not match ' \
                      f'the wavelength grid (len={wavelengths.shape[0]}).'
            raise ValueError(message)

    def _raise_value_error_if_unphysical_vales_are_present(self):
        self._raise_value_error_if_scattering_cross_section_is_larger_than_extinction_cross_section()
        self._raise_value_error_if_asymmetry_is_outside_its_valid_range()

    def _raise_value_error_if_scattering_cross_section_is_larger_than_extinction_cross_section(self):
        csca = self.get_scattering_cross_section()
        cext = self.get_extinction_cross_section()

        if np.any(csca > cext):
            message = 'Some values in the scatting cross section are larger than the extinction cross sections.'
            raise ValueError(message)

    def _raise_value_error_if_asymmetry_is_outside_its_valid_range(self):
        g = self.get_asymmetry_parameter()
        if np.any(~np.bitwise_and(-1 <= g, g <= 1)):
            message = 'Some asymmetry parameters have unphysical values.'
            raise ValueError(message)

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
        return history.replace('???', '--')

    # These work for dust1 but not ice. I could make Dust and Ice classes that inherit Radprop, but I'm afraid
    #  these change too frequently to be reliably coded. I need a more stable interface from Mike
    '''
    def get_sphericity(self) -> float:
        header = self._get_header()
        return header['spheric']

    def get_sphericitiy_comment(self) -> str:
        header = self._get_header()
        return header.comments['spheric']

    def get_source_of_refractive_indices(self) -> float:
        header = self._get_header()
        return header['diel']

    def get_source_of_refractive_indices_comment(self) -> str:
        header = self._get_header()
        return header.comments['diel']
    '''
if __name__ == '__main__':
    hd = fits.open('/media/kyle/iuvs/raw/radiative_properties/wolff/dust1-dust_all.fits.gz')
    rp = RadpropFile(hd)