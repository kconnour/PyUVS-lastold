from astropy.io import fits
from h5py import File

from data_files.compression import compression, compression_opts
import pyuvs as pu


path = 'apoapse/integration'


def add_ephemeris_time_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = pu.integration.make_ephemeris_time(hduls)
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
    dataset.attrs['unit'] = pu.units.ephemeris_time


def add_mirror_data_number_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = pu.integration.make_mirror_data_number(hduls)
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
    dataset.attrs['unit'] = pu.units.data_number


def add_mirror_angle_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = pu.integration.make_mirror_angle(hduls)
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
    dataset.attrs['unit'] = pu.units.angle


def add_field_of_view_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = pu.integration.make_field_of_view(hduls)
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
    dataset.attrs['unit'] = pu.units.angle


def add_case_temperature_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = pu.integration.make_case_temperature(hduls)
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
    dataset.attrs['unit'] = pu.units.temperature


def add_integration_time_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = pu.integration.make_integration_time(hduls)
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
    dataset.attrs['unit'] = pu.units.integration_time


def add_swath_number_to_file(file: File) -> None:
    data = pu.integration.make_swath_number(file.attrs['orbit'], file[f'{path}/mirror_angle'][:])
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
    data = pu.integration.make_number_of_swaths(file.attrs['orbit'], file[f'{path}/swath_number'][:])
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
    data = pu.integration.make_opportunity_classification(file[f'{path}/mirror_angle'][:], file[f'{path}/swath_number'][:])
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
