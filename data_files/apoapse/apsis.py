from datetime import datetime
from pathlib import Path

from h5py import File
import mars_time
import numpy as np
import spiceypy

from data_files.compression import compression, compression_opts
from data_files import spice
from data_files import units
import pyuvs as pu


path = 'apoapse/apsis'

# TODO: Remove the need for end datetime
# TODO: Make more accurate ET

spice.clear_existing_kernels()
spice.furnish_standard_kernels(Path('/media/kyle/iuvs/spice'))
print(spiceypy.spkcov)
raise SystemExit(9)
apoapsis_orbits, approximate_apoapsis_ephemeris_times = spice.compute_maven_apsis_et(segment='apoapse', end_time=datetime(2024, 1, 1), step_size=60)
ephemeris_times = approximate_apoapsis_ephemeris_times


def make_ephemeris_time(orbit: int) -> np.ndarray:
    return np.array([ephemeris_times[orbit - 1]])


def make_mars_year(ephemeris_time: float) -> np.ndarray:
    utc = spiceypy.et2datetime(ephemeris_time)[0]
    return np.array([mars_time.datetime_to_mars_time(utc).year])


def make_sol(ephemeris_time: float) -> np.ndarray:
    utc = spiceypy.et2datetime(ephemeris_time)[0]
    return np.array([mars_time.datetime_to_mars_time(utc).sol])


def make_solar_longitude(ephemeris_time: float) -> np.ndarray:
    return np.array([spice.compute_solar_longitude(ephemeris_time)])


def make_subsolar_latitude(ephemeris_time: float) -> np.ndarray:
    return np.array([spice.compute_subsolar_point(ephemeris_time)[0]])


def make_subsolar_longitude(ephemeris_time: float) -> np.ndarray:
    return np.array([spice.compute_subsolar_point(ephemeris_time)[1]])


def make_subspacecraft_latitude(ephemeris_time: float) -> np.ndarray:
    return np.array([spice.compute_subspacecraft_point(ephemeris_time)[0]])


def make_subspacecraft_longitude(ephemeris_time: float) -> np.ndarray:
    return np.array([spice.compute_subspacecraft_point(ephemeris_time)[1]])


def make_subspacecraft_altitude(ephemeris_time: float) -> np.ndarray:
    return np.array([spice.compute_subspacecraft_altitude(ephemeris_time)])


def make_subspacecraft_local_time(ephemeris_time: float, longitude: np.ndarray) -> np.ndarray:
    return np.array([spice.compute_subspacecraft_local_time(ephemeris_time, np.radians(longitude))])


def make_mars_sun_distance(ephemeris_time: float) -> np.ndarray:
    return np.array([spice.compute_mars_sun_distance(ephemeris_time)])


def add_apsis_ephemeris_time_to_file(file: File) -> None:
    data = make_ephemeris_time(file.attrs['orbit'])
    name = 'ephemeris_time'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.ephemeris_time


def add_mars_year_to_file(file: File) -> None:
    data = make_mars_year(file[f'{path}/ephemeris_time'][:])
    name = 'mars_year'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.mars_year


def add_sol_to_file(file: File) -> None:
    data = make_sol(file[f'{path}/ephemeris_time'][:])
    name = 'sol'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.sol


def add_solar_longitude_to_file(file: File) -> None:
    data = make_solar_longitude(file[f'{path}/ephemeris_time'][:])
    name = 'solar_longitude'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.solar_longitude


def add_subsolar_latitude_to_file(file: File) -> None:
    data = make_subsolar_latitude(file[f'{path}/ephemeris_time'][:])
    name = 'subsolar_latitude'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.latitude


def add_subsolar_longitude_to_file(file: File) -> None:
    data = make_subsolar_longitude(file[f'{path}/ephemeris_time'][:])
    name = 'subsolar_longitude'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.longitude


def add_subspacecraft_latitude_to_file(file: File) -> None:
    data = make_subspacecraft_latitude(file[f'{path}/ephemeris_time'][:])
    name = 'subspacecraft_latitude'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.latitude


def add_subspacecraft_longitude_to_file(file: File) -> None:
    data = make_subspacecraft_longitude(file[f'{path}/ephemeris_time'][:])
    name = 'subspacecraft_longitude'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.longitude


def add_subspacecraft_altitude_to_file(file: File) -> None:
    data = make_subsolar_longitude(file[f'{path}/ephemeris_time'][:])
    name = 'subspacecraft_altitude'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.altitude


def add_subspacecraft_local_time_to_file(file: File) -> None:
    data = make_subspacecraft_local_time(file[f'{path}/ephemeris_time'][:], file[f'{path}/subspacecraft_longitude'][:])
    name = 'subspacecraft_local_time'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.local_time


def add_mars_sun_distance_to_file(file: File) -> None:
    data = make_mars_sun_distance(file[f'{path}/ephemeris_time'][:])
    name = 'mars_sun_distance'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.altitude


def add_subsolar_subspacecraft_angle_to_file(file: File) -> None:
    data = pu.haversine(file[f'{path}/subspacecraft_latitude'][:], file[f'{path}/subspacecraft_longitude'][:],
                        file[f'{path}/subsolar_latitude'][:], file[f'{path}/subsolar_longitude'][:])
    name = 'subsolar_subspacecraft_angle'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.angle
