from datetime import datetime

import h5py
import mars_time as mt
import numpy as np
import spiceypy

from data_files import generic
import pyuvs as pu


generic.spice.furnish_standard_kernels()
orbits, ephemeris_times = generic.spice.compute_maven_apsis_et('apoapse', end_time=datetime(2023, 2, 13))


def make_ephemeris_time(orbit) -> np.ndarray:
    return ephemeris_times[orbits == orbit]


def make_mars_year(orbit: int) -> np.ndarray:
    ephemeris_time = make_ephemeris_time(orbit)
    utc = spiceypy.et2datetime(ephemeris_time)[0]
    return np.array([mt.datetime_to_mars_time(utc).year])


def make_sol(orbit: int) -> np.ndarray:
    ephemeris_time = make_ephemeris_time(orbit)
    utc = spiceypy.et2datetime(ephemeris_time)[0]
    return np.array([mt.datetime_to_mars_time(utc).sol])


def make_solar_longitude(orbit: int) -> np.ndarray:
    ephemeris_time = make_ephemeris_time(orbit)[0]
    return np.array([generic.spice.compute_solar_longitude(ephemeris_time)])


def make_subsolar_latitude(orbit: int) -> np.ndarray:
    ephemeris_time = make_ephemeris_time(orbit)[0]
    return np.array([generic.spice.compute_subsolar_point(ephemeris_time)[0]])


def make_subsolar_longitude(orbit: int) -> np.ndarray:
    ephemeris_time = make_ephemeris_time(orbit)[0]
    return np.array([generic.spice.compute_subsolar_point(ephemeris_time)[1]])


def make_subspacecraft_latitude(orbit: int) -> np.ndarray:
    ephemeris_time = make_ephemeris_time(orbit)[0]
    return np.array([generic.spice.compute_subspacecraft_point(ephemeris_time)[0]])


def make_subspacecraft_longitude(orbit: int) -> np.ndarray:
    ephemeris_time = make_ephemeris_time(orbit)[0]
    return np.array([generic.spice.compute_subspacecraft_point(ephemeris_time)[1]])


def make_subspacecraft_altitude(orbit: int) -> np.ndarray:
    ephemeris_time = make_ephemeris_time(orbit)[0]
    return np.array([generic.spice.compute_subspacecraft_altitude(ephemeris_time)])


def make_subspacecraft_local_time(orbit: int) -> np.ndarray:
    ephemeris_time = make_ephemeris_time(orbit)[0]
    longitude = make_subspacecraft_longitude(orbit)[0]
    return np.array([generic.spice.compute_subspacecraft_local_time(ephemeris_time, np.radians(longitude))])


def make_mars_sun_distance(orbit: int) -> np.ndarray:
    ephemeris_time = make_ephemeris_time(orbit)[0]
    return np.array([generic.spice.compute_mars_sun_distance(ephemeris_time)])


def make_subsolar_subspacraft_angle(orbit: int) -> np.ndarray:
    subsolar_latitude = make_subsolar_latitude(orbit)
    subsolar_longitude = make_subsolar_longitude(orbit)
    subspacecraft_latitude = make_subspacecraft_latitude(orbit)
    subspacecraft_longitude = make_subspacecraft_longitude(orbit)
    return pu.haversine((subsolar_latitude, subsolar_longitude), (subspacecraft_latitude, subspacecraft_longitude))
