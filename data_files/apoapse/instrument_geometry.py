from astropy.io import fits
from h5py import File
import numpy as np

from data_files.compression import compression, compression_opts
from data_files.helper import catch_empty_arrays
from data_files import iuvs_fits
from data_files import units


path = 'apoapse/instrument_geometry'


@catch_empty_arrays
def make_instrument_x_field_of_view(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_instrument_x_field_of_view(f) for f in hduls])


@catch_empty_arrays
def make_instrument_sun_angle(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_instrument_sun_angle(f) for f in hduls])


def make_app_flip(x_field_of_view: np.ndarray, spacecraft_velocity_inertial_frame: np.ndarray) -> np.ndarray:
    try:
        dot = x_field_of_view[:, 0] * spacecraft_velocity_inertial_frame[:, 0]
        app_flip = np.array([np.sum(dot) > 1])  # Orbit 3248 is an example of why this can't be 0
    except ValueError:
        app_flip = np.array([])
    return app_flip


def add_instrument_x_field_of_view_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_instrument_x_field_of_view(hduls)
    name = 'instrument_x_field_of_view'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.unit_vector


def add_instrument_sun_angle_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_instrument_sun_angle(hduls)
    name = 'instrument_sun_angle'
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


def add_app_flip_to_file(file: File) -> None:
    data = make_app_flip(file[f'{path}/instrument_x_field_of_view'][:],
                         file[f'apoapse/spacecraft_geometry/spacecraft_velocity_inertial_frame'][:])
    name = 'app_flip'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
