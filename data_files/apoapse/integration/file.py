from h5py import File

from data_files import generic
from data_files.compression import compression, compression_opts
from data_files import units
from data_files import apoapse


path = 'apoapse/integration'


def add_ephemeris_time_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.integration.make_ephemeris_time(hduls)

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


def add_mirror_data_number_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.integration.make_mirror_data_number(hduls)

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


def add_mirror_angle_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.integration.make_mirror_angle(hduls)

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


def add_field_of_view_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.integration.make_field_of_view(hduls)

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


def add_case_temperature_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.integration.make_case_temperature(hduls)

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


def add_integration_time_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.integration.make_integration_time(hduls)

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


def add_swath_number_to_file(file: File, hduls: generic.hdulist) -> None:
    orbit = file.attrs['orbit']
    data = apoapse.integration.make_swath_number(orbit, hduls)

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


def add_number_of_swaths_to_file(file: File, hduls: generic.hdulist) -> None:
    orbit = file.attrs['orbit']
    data = apoapse.integration.make_number_of_swaths(orbit, hduls)

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


def add_opportunity_classification_to_file(file: File, hduls: generic.hdulist) -> None:
    orbit = file.attrs['orbit']
    data = apoapse.integration.make_opportunity_classification(orbit, hduls)

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
