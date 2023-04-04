import numpy as np

from data_files.generic.typing import hdulist
from data_files.generic.miscellaneous import add_leading_axis_if_necessary


def make_spatial_bin_latitude(hduls: hdulist) -> np.ndarray:
    return np.concatenate([add_leading_axis_if_necessary(f['pixelgeometry'].data['pixel_corner_lat'], 3) for f in hduls]) if hduls else np.array([])


def make_spatial_bin_longitude(hduls: hdulist) -> np.ndarray:
    return np.concatenate([add_leading_axis_if_necessary(f['pixelgeometry'].data['pixel_corner_lon'], 3) for f in hduls]) if hduls else np.array([])


def make_spatial_bin_tangent_altitude(hduls: hdulist) -> np.ndarray:
    return np.concatenate([add_leading_axis_if_necessary(f['pixelgeometry'].data['pixel_corner_mrh_alt'], 3) for f in hduls]) if hduls else np.array([])


def make_spatial_bin_tangent_altitude_rate(hduls: hdulist) -> np.ndarray:
    return np.concatenate([add_leading_axis_if_necessary(f['pixelgeometry'].data['pixel_corner_mrh_alt_rate'], 3) for f in hduls]) if hduls else np.array([])


def make_spatial_bin_line_of_sight(hduls: hdulist) -> np.ndarray:
    return np.concatenate([add_leading_axis_if_necessary(f['pixelgeometry'].data['pixel_corner_los'], 3) for f in hduls]) if hduls else np.array([])


def make_spatial_bin_solar_zenith_angle(hduls: hdulist) -> np.ndarray:
    return np.concatenate([add_leading_axis_if_necessary(f['pixelgeometry'].data['pixel_solar_zenith_angle'], 2) for f in hduls]) if hduls else np.array([])


def make_spatial_bin_emission_angle(hduls: hdulist) -> np.ndarray:
    return np.concatenate([add_leading_axis_if_necessary(f['pixelgeometry'].data['pixel_emission_angle'], 2) for f in hduls]) if hduls else np.array([])


def make_spatial_bin_phase_angle(hduls: hdulist) -> np.ndarray:
    return np.concatenate([add_leading_axis_if_necessary(f['pixelgeometry'].data['pixel_phase_angle'], 2) for f in hduls]) if hduls else np.array([])


def make_spatial_bin_zenith_angle(hduls: hdulist) -> np.ndarray:
    return np.concatenate([add_leading_axis_if_necessary(f['pixelgeometry'].data['pixel_zenith_angle'], 2) for f in hduls]) if hduls else np.array([])


def make_spatial_bin_local_time(hduls: hdulist) -> np.ndarray:
    return np.concatenate([add_leading_axis_if_necessary(f['pixelgeometry'].data['pixel_local_time'], 2) for f in hduls]) if hduls else np.array([])


def make_spatial_bin_right_ascension(hduls: hdulist) -> np.ndarray:
    return np.concatenate([add_leading_axis_if_necessary(f['pixelgeometry'].data['pixel_corner_ra'], 3) for f in hduls]) if hduls else np.array([])


def make_spatial_bin_declination(hduls: hdulist) -> np.ndarray:
    return np.concatenate([add_leading_axis_if_necessary(f['pixelgeometry'].data['pixel_corner_dec'], 3) for f in hduls]) if hduls else np.array([])


def make_spatial_bin_vector(hduls: hdulist) -> np.ndarray:
    # original shape: (n_integrations, 3, spatial_bins, 5)
    # new shape: (n_integrations, n_spatial_bins, 5, 3)
    return np.moveaxis(np.concatenate([add_leading_axis_if_necessary(f['pixelgeometry'].data['pixel_vec'], 4) for f in hduls]), 1, -1) if hduls else np.array([])
