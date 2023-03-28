import numpy as np

from pyuvs import iuvs_fits
from pyuvs.hdulist import hdulist
from pyuvs.miscellaneous import catch_empty_arrays


@catch_empty_arrays
def make_subsolar_latitude(hduls: hdulist) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subsolar_latitude(f) for f in hduls])


@catch_empty_arrays
def make_subsolar_longitude(hduls: hdulist) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subsolar_longitude(f) for f in hduls])


@catch_empty_arrays
def make_subspacecraft_latitude(hduls: hdulist) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subspacecraft_latitude(f) for f in hduls])


@catch_empty_arrays
def make_subspacecraft_longitude(hduls: hdulist) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subspacecraft_longitude(f) for f in hduls])


@catch_empty_arrays
def make_subspacecraft_altitude(hduls: hdulist) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subspacecraft_altitude(f) for f in hduls])


@catch_empty_arrays
def make_spacecraft_velocity_inertial_frame(hduls: hdulist) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_spacecraft_velocity_inertial_frame(f) for f in hduls])
