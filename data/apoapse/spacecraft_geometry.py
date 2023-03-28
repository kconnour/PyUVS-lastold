import numpy as np

from data.iuvs_fits import Level1b
from data.miscellaneous import catch_empty_arrays


@catch_empty_arrays
def make_subsolar_latitude(hduls: list[Level1b]) -> np.ndarray:
    return np.concatenate([f.get_subsolar_latitude() for f in hduls])


@catch_empty_arrays
def make_subsolar_longitude(hduls: list[Level1b]) -> np.ndarray:
    return np.concatenate([f.get_subsolar_longitude() for f in hduls])


@catch_empty_arrays
def make_subspacecraft_latitude(hduls: list[Level1b]) -> np.ndarray:
    return np.concatenate([f.get_subspacecraft_latitude() for f in hduls])


@catch_empty_arrays
def make_subspacecraft_longitude(hduls: list[Level1b]) -> np.ndarray:
    return np.concatenate([f.get_subspacecraft_longitude() for f in hduls])


@catch_empty_arrays
def make_subspacecraft_altitude(hduls: list[Level1b]) -> np.ndarray:
    return np.concatenate([f.get_subspacecraft_altitude() for f in hduls])


@catch_empty_arrays
def make_spacecraft_velocity_inertial_frame(hduls: list[Level1b]) -> np.ndarray:
    return np.concatenate([f.get_spacecraft_velocity_inertial_frame() for f in hduls])
