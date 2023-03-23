from astropy.io import fits
from h5py import File
import numpy as np

from data_files.compression import compression, compression_opts
from data_files.helper import catch_empty_arrays
from data_files import iuvs_fits
from data_files import units


path = 'apoapse/spacecraft_geometry'


@catch_empty_arrays
def make_subsolar_latitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subsolar_latitude(f) for f in hduls])


@catch_empty_arrays
def make_subsolar_longitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subsolar_longitude(f) for f in hduls])


@catch_empty_arrays
def make_subspacecraft_latitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subspacecraft_latitude(f) for f in hduls])


@catch_empty_arrays
def make_subspacecraft_longitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subspacecraft_longitude(f) for f in hduls])


@catch_empty_arrays
def make_subspacecraft_altitude(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_subspacecraft_altitude(f) for f in hduls])


@catch_empty_arrays
def make_spacecraft_velocity_inertial_frame(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_spacecraft_velocity_inertial_frame(f) for f in hduls])


def add_subsolar_latitude_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_subsolar_latitude(hduls)
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


def add_subsolar_longitude_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_subsolar_longitude(hduls)
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


def add_subspacecraft_latitude_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_subspacecraft_latitude(hduls)
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


def add_subspacecraft_longitude_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_subspacecraft_longitude(hduls)
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


def add_subspacecraft_altitude_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_subspacecraft_altitude(hduls)
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


def add_spacecraft_velocity_inertial_frame_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_spacecraft_velocity_inertial_frame(hduls)
    name = 'spacecraft_velocity_inertial_frame'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.velocity
