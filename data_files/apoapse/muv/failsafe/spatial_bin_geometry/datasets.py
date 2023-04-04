import numpy as np

from data_files import generic


def make_spatial_bin_latitude(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_latitude(hduls)


def make_spatial_bin_longitude(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_longitude(hduls)


def make_spatial_bin_tangent_altitude(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_tangent_altitude(hduls)


def make_spatial_bin_tangent_altitude_rate(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_tangent_altitude_rate(hduls)


def make_spatial_bin_line_of_sight(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_line_of_sight(hduls)


def make_spatial_bin_solar_zenith_angle(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_solar_zenith_angle(hduls)


def make_spatial_bin_emission_angle(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_emission_angle(hduls)


def make_spatial_bin_phase_angle(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_phase_angle(hduls)


def make_spatial_bin_zenith_angle(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_zenith_angle(hduls)


def make_spatial_bin_local_time(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_local_time(hduls)


def make_spatial_bin_right_ascension(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_right_ascension(hduls)


def make_spatial_bin_declination(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_declination(hduls)


def make_spatial_bin_vector(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_vector(hduls)
