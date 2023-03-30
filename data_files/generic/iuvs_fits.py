"""This module provides objects for pulling data from the IUVS fits files.
"""
'''from astropy.io import fits
import numpy as np


class Level1a:
    def __init__(self, hdul: fits.hdu.hdulist.HDUList):
        self.hdul = hdul

    def get_detector_raw(self) -> np.ndarray:
        return self.hdul['primary'].data

    def get_integration_timestamp(self) -> np.ndarray:
        return self.hdul['integration'].data['timestamp']

    def get_integration_ephemeris_time(self) -> np.ndarray:
        return self.hdul['integration'].data['et']

    def get_integration_utc(self) -> np.ndarray:
        return self.hdul['integration'].data['utc']

    def get_integration_mirror_data_number(self) -> np.ndarray:
        return self.hdul['integration'].data['mirror_dn']

    def get_integration_mirror_angle(self) -> np.ndarray:
        return self.hdul['integration'].data['mirror_deg']

    def get_integration_field_of_view(self) -> np.ndarray:
        return self.hdul['integration'].data['fov_deg']

    def get_integration_lyman_alpha_centroid(self) -> np.ndarray:
        # As of v13 IUVS data, this array is populated with junk data
        return self.hdul['integration'].data['lya_centroid']

    def get_integration_detector_temperature(self) -> np.ndarray:
        return self.hdul['integration'].data['det_temp_c']

    def get_integration_case_temperature(self) -> np.ndarray:
        return self.hdul['integration'].data['case_temp_c']

    def get_spatial_pixel_low(self) -> np.ndarray:
        # The data is natively (1, n_spatial_bins)
        return np.squeeze(self.hdul['binning'].data['spapixlo'])

    def get_spatial_pixel_high(self) -> np.ndarray:
        # The data is natively (1, n_spatial_bins)
        return np.squeeze(self.hdul['binning'].data['spapixhi'])

    def get_spectral_pixel_low(self) -> np.ndarray:
        # The data is natively (1, n_spectral_bins)
        return np.squeeze(self.hdul['binning'].data['spepixlo'][0])

    def get_spectral_pixel_high(self) -> np.ndarray:
        # The data is natively (1, n_spectral_bins)
        return np.squeeze(self.hdul['binning'].data['spepixhi'][0])

    def get_bin_table_name(self) -> str:
        return self.hdul['binning'].data['bintablename'][0]

    def get_spatial_bin_size(self) -> int:
        return self.hdul['primary'].header['spa_size']

    def get_spectral_bin_size(self) -> int:
        return self.hdul['primary'].header['spe_size']

    def get_spatial_bin_latitude(self) -> np.ndarray:
        return self.hdul['pixelgeometry'].data['pixel_corner_lat']

    def get_spatial_bin_longitude(self) -> np.ndarray:
        return self.hdul['pixelgeometry'].data['pixel_corner_lon']

    def get_spatial_bin_tangent_altitude(self) -> np.ndarray:
        return self.hdul['pixelgeometry'].data['pixel_corner_mrh_alt']

    def get_spatial_bin_tangent_altitude_rate(self) -> np.ndarray:
        return self.hdul['pixelgeometry'].data['pixel_corner_mrh_alt_rate']

    def get_spatial_bin_line_of_sight(self) -> np.ndarray:
        return self.hdul['pixelgeometry'].data['pixel_corner_los']

    def get_spatial_bin_solar_zenith_angle(self) -> np.ndarray:
        return self.hdul['pixelgeometry'].data['pixel_solar_zenith_angle']

    def get_spatial_bin_emission_angle(self) -> np.ndarray:
        return self.hdul['pixelgeometry'].data['pixel_emission_angle']

    def get_spatial_bin_phase_angle(self) -> np.ndarray:
        return self.hdul['pixelgeometry'].data['pixel_phase_angle']

    def get_spatial_bin_zenith_angle(self) -> np.ndarray:
        return self.hdul['pixelgeometry'].data['pixel_zenith_angle']

    def get_spatial_bin_local_time(self) -> np.ndarray:
        return self.hdul['pixelgeometry'].data['pixel_local_time']

    def get_spatial_bin_right_ascension(self) -> np.ndarray:
        return self.hdul['pixelgeometry'].data['pixel_corner_ra']

    def get_spatial_bin_declination(self) -> np.ndarray:
        return self.hdul['pixelgeometry'].data['pixel_corner_dec']

    def get_spatial_bin_vector(self) -> np.ndarray:
        return self.hdul['pixelgeometry'].data['pixel_vec']

    def get_subsolar_latitude(self) -> np.ndarray:
        return self.hdul['spacecraftgeometry'].data['sub_solar_lat']

    def get_subsolar_longitude(self) -> np.ndarray:
        return self.hdul['spacecraftgeometry'].data['sub_solar_lon']

    def get_subspacecraft_latitude(self) -> np.ndarray:
        return self.hdul['spacecraftgeometry'].data['sub_spacecraft_lat']

    def get_subspacecraft_longitude(self) -> np.ndarray:
        return self.hdul['spacecraftgeometry'].data['sub_spacecraft_lon']

    def get_subspacecraft_altitude(self) -> np.ndarray:
        return self.hdul['spacecraftgeometry'].data['spacecraft_alt']

    def get_spacecraft_velocity_inertial_frame(self) -> np.ndarray:
        return self.hdul['spacecraftgeometry'].data['v_spacecraft_rate_inertial']

    def get_instrument_x_field_of_view(self) -> np.ndarray:
        return self.hdul['spacecraftgeometry'].data['vx_instrument_inertial']

    def get_instrument_sun_angle(self) -> np.ndarray:
        return self.hdul['spacecraftgeometry'].data['inst_sun_angle']

    def get_channel(self) -> str:
        return self.hdul['observation'].data['channel'][0]

    def get_integration_time(self) -> float:
        return self.hdul['observation'].data['int_time'][0]

    def get_observation_id(self) -> int:
        return self.hdul['primary'].header['obs_id']


class Level1b(Level1a):
    def __init__(self, hdul: fits.hdu.hdulist.HDUList):
        super().__init__(hdul)

    def get_detector_calibrated(self) -> np.ndarray:
        return self.hdul['primary'].data

    def get_detector_raw(self) -> np.ndarray:
        return self.hdul['detector_raw'].data

    def get_detector_dark_subtracted(self) -> np.ndarray:
        return self.hdul['detector_dark_subtracted'].data

    def get_detector_random_data_number_uncertainty(self) -> np.ndarray:
        return self.hdul['random_dn_unc'].data

    def get_detector_random_physical_uncertainty(self) -> np.ndarray:
        return self.hdul['random_phy_unc'].data

    def get_detector_systematic_physical_uncertainty(self) -> np.ndarray:
        return self.hdul['systematic_phy_unc'].data

    def get_mcp_voltage(self) -> float:
        return self.hdul['observation'].data['mcp_volt'][0]

    def get_mcp_voltage_gain(self) -> float:
        return self.hdul['observation'].data['mcp_gain'][0]'''
