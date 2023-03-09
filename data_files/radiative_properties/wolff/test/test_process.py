import tempfile

from astropy.io import fits
from h5py import File
import numpy as np
import pytest

from data_files.radiative_properties.wolff.process import process_file


class Test_process_file:
    @pytest.fixture
    def file_creation_date(self) -> str:
        return '2022-01-01'

    @pytest.fixture
    def history(self) -> str:
        return 'my_file_history'

    @pytest.fixture
    def n_particle_sizes(self) -> int:
        return 2

    @pytest.fixture
    def n_wavelengths(self) -> int:
        return 4

    @pytest.fixture
    def n_scattering_angles(self) -> int:
        return 18

    @pytest.fixture
    def n_moments(self) -> int:
        return 8

    @pytest.fixture
    def primary(self) -> np.ndarray:
        return np.array([])

    @pytest.fixture
    def scattering_cross_section(self, n_particle_sizes, n_wavelengths) -> np.ndarray:
        return np.ones((n_particle_sizes, n_wavelengths))

    @pytest.fixture
    def extinction_cross_section(self, n_particle_sizes, n_wavelengths) -> np.ndarray:
        return np.ones((n_particle_sizes, n_wavelengths)) * 2

    @pytest.fixture
    def asymmetry_parameter(self, n_particle_sizes, n_wavelengths) -> np.ndarray:
        return np.ones((n_particle_sizes, n_wavelengths)) * 0.5

    @pytest.fixture
    def forw(self, scattering_cross_section, extinction_cross_section, asymmetry_parameter) -> np.ndarray:
        return np.dstack([extinction_cross_section, scattering_cross_section, asymmetry_parameter])

    @pytest.fixture
    def pmom(self, n_moments, n_particle_sizes, n_wavelengths) -> np.ndarray:
        return np.ones((n_moments, n_particle_sizes, n_wavelengths))

    @pytest.fixture
    def phsfn(self, n_scattering_angles, n_particle_sizes, n_wavelengths) -> np.ndarray:
        return np.ones((n_scattering_angles, n_particle_sizes, n_wavelengths))

    @pytest.fixture
    def expansion(self, n_scattering_angles, n_particle_sizes, n_wavelengths) -> np.ndarray:
        return np.ones((n_scattering_angles, n_particle_sizes, n_wavelengths))

    @pytest.fixture
    def particle_sizes(self, n_particle_sizes) -> np.ndarray:
        return np.arange(n_particle_sizes) + 1

    @pytest.fixture
    def wavelengths(self, n_wavelengths) -> np.ndarray:
        return np.arange(n_wavelengths) + 1

    @pytest.fixture
    def scattering_angles(self, n_scattering_angles) -> np.ndarray:
        return np.arange(n_scattering_angles)

    @pytest.fixture
    def example_input_file(self, primary, file_creation_date, history, forw, pmom, phsfn, expansion, particle_sizes, wavelengths, scattering_angles) -> fits.HDUList:
        primary = fits.PrimaryHDU(data=primary)

        primary.header['date'] = file_creation_date
        primary.header['history'] = history

        forw = fits.ImageHDU(name='forw', data=forw)
        pmom = fits.ImageHDU(name='pmom', data=pmom)
        phsfn = fits.ImageHDU(name='phsfn', data=phsfn)
        expansion = fits.ImageHDU(name='expansion', data=expansion)
        particle_sizes = fits.ImageHDU(name='particle_sizes', data=particle_sizes)
        wavelengths = fits.ImageHDU(name='wavelengths', data=wavelengths)
        scattering_angle = fits.ImageHDU(name='scattering_angle', data=scattering_angles)

        return fits.HDUList([primary, forw, pmom, phsfn, expansion, particle_sizes, wavelengths, scattering_angle])

    def test_process_file_produces_expected_data_file(self, example_input_file):
        # I don't know how to do this yet, but here's what to do:
        # 1. mock the return of fits.open() to give example_input_file
        # 2. make a tempfile: file = File(tempfile.TemporaryFile(), 'w')
        # 3. mock the return of File() to be the output of step 2
        # 4. Check the tempfile has the info of example_input_file in it

        #file = File(tempfile.TemporaryFile(), 'w')
        #process_file('junk-aerosol-file.fits.gz', 'dust', 1)
        pass
