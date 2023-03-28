from h5py import File

from data.iuvs_fits import Level1b
from data.apoapse import instrument_geometry
from data_files.compression import compression, compression_opts
from data_files import units


path = 'apoapse/instrument_geometry'


def add_instrument_x_field_of_view_to_file(file: File, hduls: list[Level1b]) -> None:
    data = instrument_geometry.make_instrument_x_field_of_view(hduls)

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


def add_instrument_sun_angle_to_file(file: File, hduls: list[Level1b]) -> None:
    data = instrument_geometry.make_instrument_sun_angle(hduls)

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
    instrument_x_field_of_view = file[f'{path}/instrument_x_field_of_view'][:]
    spacecraft_velocity_inertial_frame = file[f'apoapse/spacecraft_geometry/spacecraft_velocity_inertial_frame'][:]
    data = instrument_geometry.make_app_flip(instrument_x_field_of_view, spacecraft_velocity_inertial_frame)

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
