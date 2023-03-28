from h5py import File

from data.iuvs_fits import Level1b
from data.apoapse import spacecraft_geometry
from data_files.compression import compression, compression_opts
from data_files import units


path = 'apoapse/spacecraft_geometry'


def add_subsolar_latitude_to_file(file: File, hduls: list[Level1b]) -> None:
    data = spacecraft_geometry.make_subsolar_latitude(hduls)
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


def add_subsolar_longitude_to_file(file: File, hduls: list[Level1b]) -> None:
    data = spacecraft_geometry.make_subsolar_longitude(hduls)
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


def add_subspacecraft_latitude_to_file(file: File, hduls: list[Level1b]) -> None:
    data = spacecraft_geometry.make_subspacecraft_latitude(hduls)
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


def add_subspacecraft_longitude_to_file(file: File, hduls: list[Level1b]) -> None:
    data = spacecraft_geometry.make_subspacecraft_longitude(hduls)
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


def add_subspacecraft_altitude_to_file(file: File, hduls: list[Level1b]) -> None:
    data = spacecraft_geometry.make_subspacecraft_altitude(hduls)
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


def add_spacecraft_velocity_inertial_frame_to_file(file: File, hduls: list[Level1b]) -> None:
    data = spacecraft_geometry.make_spacecraft_velocity_inertial_frame(hduls)
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
