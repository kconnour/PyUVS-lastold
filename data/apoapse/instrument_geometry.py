import numpy as np

from data.iuvs_fits import Level1b
from data.miscellaneous import catch_empty_arrays


@catch_empty_arrays
def make_instrument_x_field_of_view(hduls: list[Level1b]) -> np.ndarray:
    return np.concatenate([f.get_instrument_x_field_of_view() for f in hduls])


@catch_empty_arrays
def make_instrument_sun_angle(hduls: list[Level1b]) -> np.ndarray:
    return np.concatenate([f.get_instrument_sun_angle() for f in hduls])


def make_app_flip(x_field_of_view: np.ndarray, spacecraft_velocity_inertial_frame: np.ndarray) -> np.ndarray:
    try:
        dot = x_field_of_view[:, 0] * spacecraft_velocity_inertial_frame[:, 0]
        app_flip = np.array([np.sum(dot) > 1])  # Orbit 3248 is an example of why this can't be 0
    except ValueError:
        app_flip = np.array([])
    return app_flip
