

import numpy as np

from data_files import generic


def make_instrument_x_field_of_view(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_instrument_x_field_of_view(hduls)


def make_instrument_sun_angle(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_instrument_sun_angle(hduls)


def make_app_flip(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_app_flip(hduls)
