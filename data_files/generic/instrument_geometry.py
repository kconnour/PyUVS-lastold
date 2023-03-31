import numpy as np

from data_files.generic.spacecraft_geometry import make_spacecraft_velocity_inertial_frame
from data_files.generic.typing import hdulist


def make_instrument_x_field_of_view(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['vx_instrument_inertial'] for f in hduls]) if hduls else np.array([])


def make_instrument_sun_angle(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['inst_sun_angle'] for f in hduls]) if hduls else np.array([])


def make_app_flip(hduls: hdulist) -> np.ndarray:
    x_field_of_view = make_instrument_x_field_of_view(hduls)
    spacecraft_velocity_inertial_frame = make_spacecraft_velocity_inertial_frame(hduls)
    try:
        dot = x_field_of_view[:, 0] * spacecraft_velocity_inertial_frame[:, 0]
        app_flip = np.array([np.sum(dot) > 1])  # Orbit 3248 is an example of why this can't be 0
    except IndexError:
        app_flip = np.array([])
    return app_flip
