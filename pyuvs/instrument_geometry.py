import numpy as np

from pyuvs import iuvs_fits
from pyuvs.hdulist import hdulist
from pyuvs.miscellaneous import catch_empty_arrays


@catch_empty_arrays
def make_instrument_x_field_of_view(hduls: hdulist) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_instrument_x_field_of_view(f) for f in hduls])


@catch_empty_arrays
def make_instrument_sun_angle(hduls: hdulist) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_instrument_sun_angle(f) for f in hduls])


def make_app_flip(x_field_of_view: np.ndarray, spacecraft_velocity_inertial_frame: np.ndarray) -> np.ndarray:
    try:
        dot = x_field_of_view[:, 0] * spacecraft_velocity_inertial_frame[:, 0]
        app_flip = np.array([np.sum(dot) > 1])  # Orbit 3248 is an example of why this can't be 0
    except ValueError:
        app_flip = np.array([])
    return app_flip
