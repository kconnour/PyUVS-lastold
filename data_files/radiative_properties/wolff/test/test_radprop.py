from astropy.io import fits
import numpy as np
import pytest

from data_files.radiative_properties.wolff.radprop import RadpropFile


class TestRadpropFile:
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
        return 180

    @pytest.fixture
    def n_moments(self) -> int:
        return 64

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
    def example_file(self, primary, file_creation_date, history, forw, pmom, phsfn, expansion, particle_sizes, wavelengths, scattering_angles) -> fits.HDUList:
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

    def test_primary_gives_expected_answer(self, example_file, primary):
        radprop = RadpropFile(example_file)
        assert np.array_equal(radprop.get_primary(), primary)

    def test_get_particle_sizes_gives_expected_answer(self, example_file, particle_sizes):
        radprop = RadpropFile(example_file)
        assert np.array_equal(radprop.get_particle_sizes(), particle_sizes)

    def test_get_wavelengths_gives_expected_answer(self, example_file, wavelengths):
        radprop = RadpropFile(example_file)
        assert np.array_equal(radprop.get_wavelengths(), wavelengths)

    def test_get_scattering_angle_gives_expected_answer(self, example_file, scattering_angles):
        radprop = RadpropFile(example_file)
        assert np.array_equal(radprop.get_scattering_angles(), scattering_angles)

    def test_get_scattering_cross_section_gives_expected_answer(self, example_file, scattering_cross_section):
        radprop = RadpropFile(example_file)
        assert np.array_equal(radprop.get_scattering_cross_section(), scattering_cross_section)

    def test_get_extinctionc_cross_section_gives_expected_answer(self, example_file, extinction_cross_section):
        radprop = RadpropFile(example_file)
        assert np.array_equal(radprop.get_extinction_cross_section(), extinction_cross_section)

    def test_get_asymmetry_parameter_gives_expected_answer(self, example_file, asymmetry_parameter):
        radprop = RadpropFile(example_file)
        assert np.array_equal(radprop.get_asymmetry_parameter(), asymmetry_parameter)

    def test_get_phase_function_gives_expected_answer(self, example_file, phsfn):
        radprop = RadpropFile(example_file)
        assert np.array_equal(radprop.get_phase_function()[..., 0], phsfn[0])

    def test_get_legendre_coefficients_gives_expected_answer(self, example_file, pmom):
        radprop = RadpropFile(example_file)
        assert np.array_equal(radprop.get_legendre_coefficients()[..., 0], pmom[0])

    def test_get_phase_function_reexpansion_gives_expected_answer(self, example_file, expansion):
        radprop = RadpropFile(example_file)
        assert np.array_equal(radprop.get_phase_function_reexpansion()[..., 0], expansion[0])

    def test_get_file_creation_date_gives_expected_answer(self, example_file, file_creation_date):
        radprop = RadpropFile(example_file)
        assert np.array_equal(radprop.get_file_creation_date(), file_creation_date)

    def test_get_history_gives_expected_answer(self, example_file, history):
        radprop = RadpropFile(example_file)
        assert np.array_equal(radprop.get_history(), history)
