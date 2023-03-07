from astropy.io import fits
import numpy as np


class RadpropFile:
    def __init__(self, hdul: fits.hdu.hdulist.HDUList):
        self.hdul = hdul

        self._raise_type_error_if_input_is_not_hdulist()
        self._raise_value_error_if_records_are_not_present()

    def _raise_type_error_if_input_is_not_hdulist(self):
        if not isinstance(self.hdul, fits.hdu.hdulist.HDUList):
            raise TypeError('The input is not a hdulist')

    def _raise_value_error_if_records_are_not_present(self):
        expected_records = ['primary', 'forw', 'pmom', 'phsfn', 'expansion', 'particle_sizes', 'wavelengths',
                            'scattering_angle']
        validation = []
        for record in expected_records:
            validation.append(record in self.hdul)

        if not all(validation):
            raise ValueError('Some expected fields are not present.')

    def get_particle_sizes(self) -> np.ndarray:
        return self.hdul['particle_sizes'].data

    def get_wavelengths(self) -> np.ndarray:
        return self.hdul['wavelengths'].data

    def get_scattering_angle(self) -> np.ndarray:
        return self.hdul['scattering_angle'].data

    def get_scattering_cross_section(self) -> np.ndarray:
        return self.hdul['forw'].data[..., 1]

    def get_extinction_cross_section(self) -> np.ndarray:
        return self.hdul['forw'].data[..., 0]

    def get_asymmetry_parameter(self) -> np.ndarray:
        return self.hdul['forw'].data[..., 2]

    def _get_raw_phase_function(self):
        return self.hdul['phsfn'].data

    def get_phase_function(self) -> np.ndarray:
        data = self.hdul['phsfn'].data
        return np.moveaxis(data, 0, -1)

    def get_legendre_coefficients(self) -> np.ndarray:
        data = self.hdul['pmom'].data
        return np.moveaxis(data, 0, -1)

    def get_reexpanded_phase_function(self) -> np.ndarray:
        data = self.hdul['expansion'].data
        return np.moveaxis(data, 0, -1)

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
