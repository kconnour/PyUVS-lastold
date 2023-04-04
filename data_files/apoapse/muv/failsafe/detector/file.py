from h5py import File

from data_files import generic
from data_files.compression import compression, compression_opts
from data_files import units
from data_files import apoapse


path = 'apoapse/muv/failsafe/detector'


def add_raw_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.failsafe.detector.make_raw(hduls)

    name = 'raw'
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


def add_dark_subtracted_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.failsafe.detector.make_dark_subtracted(hduls)

    name = 'dark_subtracted'
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


def add_brightness_to_file(file: File) -> None:
    data = apoapse.muv.failsafe.detector.make_brightness(file)

    name = 'brightness'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.brightness