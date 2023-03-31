import numpy as np

from data_files.generic.typing import hdulist


def make_subsolar_latitude(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['sub_solar_lat'] for f in hduls]) if hduls else np.array([])


def make_subsolar_longitude(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['sub_solar_lon'] for f in hduls]) if hduls else np.array([])


def make_subspacecraft_latitude(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['sub_spacecraft_lat'] for f in hduls]) if hduls else np.array([])


def make_subspacecraft_longitude(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['sub_spacecraft_lon'] for f in hduls]) if hduls else np.array([])


def make_subspacecraft_altitude(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['spacecraft_alt'] for f in hduls]) if hduls else np.array([])


def make_spacecraft_velocity_inertial_frame(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['spacecraftgeometry'].data['v_spacecraft_rate_inertial'] for f in hduls]) if hduls else np.array([])
