from h5py import File

from data_files import generic
from data_files.compression import compression, compression_opts
from data_files import units
from data_files import apoapse


path = 'apoapse/instrument_geometry'


def add_instrument_x_field_of_view_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.instrument_geometry.make_instrument_x_field_of_view(hduls)

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


def add_instrument_sun_angle_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.instrument_geometry.make_instrument_sun_angle(hduls)

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


def add_app_flip_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.instrument_geometry.make_app_flip(hduls)

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
