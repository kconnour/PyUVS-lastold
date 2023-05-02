import abc
from datetime import datetime
from pathlib import Path
import warnings

from astropy.time import Time, TimeDelta
from astropy import units as u
from h5py import File
import numpy as np
from netCDF4 import Dataset
from scipy.constants import Planck, speed_of_light
from scipy.integrate import quadrature

from data_files import generic
import pyuvs as pu


def make_raw(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_detector_raw(hduls)


def make_dark_subtracted(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_detector_dark_subtracted(hduls)


def make_brightness(file: File) -> np.ndarray:
    good_integrations = file['apoapse/muv/integration/dayside_integrations'][:]

    dark_subtracted = file['apoapse/muv/dayside/detector/dark_subtracted'][:]
    spatial_bin_edges = file['apoapse/muv/dayside/binning/spatial_bin_edges'][:]
    spectral_bin_edges = file['apoapse/muv/dayside/binning/spectral_bin_edges'][:]
    spatial_bin_width = file['apoapse/muv/dayside/binning/spatial_bin_width'][:]
    spectral_bin_width = file['apoapse/muv/dayside/binning/spectral_bin_width'][:]
    integration_time = file['apoapse/integration/integration_time'][good_integrations]
    mcp_voltage = file['apoapse/muv/integration/mcp_voltage'][good_integrations]
    mcp_voltage_gain = file['apoapse/muv/integration/mcp_voltage_gain'][good_integrations]

    return generic.make_brightness(dark_subtracted, spatial_bin_edges, spectral_bin_edges, spatial_bin_width,
                                   spectral_bin_width, integration_time, mcp_voltage, mcp_voltage_gain)


def make_radiance(file: File) -> np.ndarray:
    dds = file['apoapse/muv/dayside/detector/dark_subtracted'][:]
    et = file['apoapse/apsis/ephemeris_time'][:]
    mars_sun_distance = file['apoapse/apsis/mars_sun_distance'][:]
    spectral_bin_edges = file['apoapse/muv/dayside/binning/spectral_bin_edges'][:]

    # Read in Justin's wavelengths (use None for now)
    wavelength_edges = None

    psf = pu.load_point_spread_function()

    timestamp = (Time(2000, format='jyear') + TimeDelta(et * u.s)).iso
    dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
    if dt < datetime(2020, 2, 1):
        solar_flux = Solstice(dt)
    else:
        solar_flux = TSIS1(timestamp)

    earth_sun_distance = 1.496e8  # km
    radius = earth_sun_distance / mars_sun_distance

    reflectance = np.zeros(dds.shape)
    for spatial_bin in range(reflectance.shape[1]):
        # Compute the wavelengths on a 1024 grid (but don't take all 1024 pixels since some are in the keyholes)
        # I have to do this because of the PSF
        pixel_edges = np.arange(spectral_bin_edges[0], spectral_bin_edges[-1] + 1)
        pixel_edge_wavelengths = np.interp(pixel_edges, spectral_bin_edges, wavelength_edges[spatial_bin, :])

        # Integrate the solar flux
        integrated_flux = np.array([solar_flux.integrate_flux(pixel_edge_wavelengths[i], pixel_edge_wavelengths[i+1]) for i in range(len(pixel_edge_wavelengths)-1)])
        integrated_flux *= radius ** 2

        # Convolve the flux by the PSF and rebin to IUVS resolution
        convolved_flux = np.convolve(integrated_flux, psf, mode='same')
        edge_indices = spectral_bin_edges - spectral_bin_edges[0]
        rebinned_solar_flux = np.array([np.sum(convolved_flux[edge_indices[i]: edge_indices[i + 1]]) for i in range(reflectance.shape[2])])

        for integration in range(reflectance.shape[0]):
            reflectance[integration, spatial_bin] = dds[integration, spatial_bin, :] * np.pi / rebinned_solar_flux

    return reflectance


class SolarFlux(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_irradiance(self):
        pass

    @abc.abstractmethod
    def get_wavelengths(self):
        pass

    def convert_flux_to_kR(self):
        return self.get_irradiance() * (self.get_wavelengths() * 10**-9) / (Planck * speed_of_light) * (4 * np.pi / 10**10) / 1000

    def integrate_flux(self, low: float, high: float) -> float:
        """Integrate the solar flux and get the kR of each spectral bin.

        Parameters
        ----------
        low
            The low wavelength (nm)
        high
            The high wavelengths (nm)

        Returns
        -------

        """
        def solar(wav):
            return np.interp(wav, self.get_wavelengths(), self.convert_flux_to_kR())

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            return quadrature(solar, low, high)[0]


class Solstice(SolarFlux):
    def __init__(self, dt: datetime):
        self.dt = dt
        self._base_path = Path('/mnt/iuvs/solar_flux/solstice')
        self.dataset = self._load_dataset()

    def _load_dataset(self):
        return Dataset(self._base_path / f'SORCE_SOLSTICE_L3_HR_V18_{self.dt.year}.nc')

    def get_irradiance(self):
        return self.dataset.variables['irradiance'][self.dt.timetuple().tm_yday - 1, :]

    def get_wavelengths(self):
        return self.dataset.variables['standard_wavelengths'][:]


class TSIS1(SolarFlux):
    def __init__(self, dt: datetime):
        self.dt = dt
        self._base_path = Path('/mnt/iuvs/solar_flux/tsis-1')
        self.dataset = self._load_dataset()

    def _load_dataset(self):
        return Dataset(self._base_path / f'tsis_ssi_L3_c24h_latest.nc')

    def get_wavelengths(self):
        return self.dataset['wavelength'][:]

    def get_irradiance(self):
        # NOTE: In theory I should adjust this spectrum to match what SOLSTICE would've measured. However, over the
        # spectral range I care about, the differences are so small that it's not worth the effort right now
        jd = Time(self.dt, format='isot').jd
        times = self.dataset['time'][:]
        idx = np.np.abs(times - jd).argmin()
        return self.dataset['irradiance'][idx, :]
