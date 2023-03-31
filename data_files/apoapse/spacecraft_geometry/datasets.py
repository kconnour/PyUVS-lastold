import numpy as np

from data_files import generic


def make_subsolar_latitude(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_subsolar_latitude(hduls)


def make_subsolar_longitude(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_subsolar_longitude(hduls)


def make_subspacecraft_latitude(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_subspacecraft_latitude(hduls)


def make_subspacecraft_longitude(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_subspacecraft_longitude(hduls)


def make_subspacecraft_altitude(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_subspacecraft_altitude(hduls)


def make_spacecraft_velocity_inertial_frame(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spacecraft_velocity_inertial_frame(hduls)
