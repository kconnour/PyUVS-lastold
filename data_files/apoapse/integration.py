from h5py import File

from data.iuvs_fits import Level1b
from data.apoapse import integration
from data_files.compression import compression, compression_opts
from data_files import units


path = 'apoapse/integration'


def add_ephemeris_time_to_file(file: File, hduls: list[Level1b]) -> None:
    data = integration.make_ephemeris_time(hduls)

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


def add_mirror_data_number_to_file(file: File, hduls: list[Level1b]) -> None:
    data = integration.make_mirror_data_number(hduls)

    name = 'mirror_data_number'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.data_number


def add_mirror_angle_to_file(file: File, hduls: list[Level1b]) -> None:
    data = integration.make_mirror_angle(hduls)

    name = 'mirror_angle'
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


def add_field_of_view_to_file(file: File, hduls: list[Level1b]) -> None:
    data = integration.make_field_of_view(hduls)

    name = 'field_of_view'
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


def add_case_temperature_to_file(file: File, hduls: list[Level1b]) -> None:
    data = integration.make_case_temperature(hduls)

    name = 'case_temperature'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.temperature


def add_integration_time_to_file(file: File, hduls: list[Level1b]) -> None:
    data = integration.make_integration_time(hduls)

    name = 'integration_time'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.integration_time


def add_swath_number_to_file(file: File) -> None:
    orbit = file.attrs['orbit']
    mirror_angle = file[f'{path}/mirror_angle'][:]
    data = integration.make_swath_number(orbit, mirror_angle)

    name = 'swath_number'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data


def add_number_of_swaths_to_file(file: File) -> None:
    orbit = file.attrs['orbit']
    swath_number = file[f'{path}/swath_number'][:]
    data = integration.make_number_of_swaths(orbit, swath_number)

    name = 'number_of_swaths'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data


def add_opportunity_classification_to_file(file: File) -> None:
    mirror_angle = file[f'{path}/mirror_angle'][:]
    swath_number = file[f'{path}/swath_number'][:]
    data = integration.make_opportunity_classification(mirror_angle, swath_number)

    name = 'opportunity_classification'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
