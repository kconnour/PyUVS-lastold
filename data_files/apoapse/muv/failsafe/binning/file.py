from h5py import File

from data_files import generic
from data_files.compression import compression, compression_opts
from data_files import units
from data_files import apoapse


path = 'apoapse/muv/failsafe/binning'


def add_spatial_bin_edges_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.failsafe.binning.make_spatial_bin_edges(hduls)

    name = 'spatial_bin_edges'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.bin


def add_spectral_bin_edges_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.failsafe.binning.make_spectral_bin_edges(hduls)

    name = 'spectral_bin_edges'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.bin


def add_spatial_bin_width_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.failsafe.binning.make_spatial_bin_width(hduls)

    name = 'spatial_bin_width'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.bin


def add_spectral_bin_width_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.failsafe.binning.make_spectral_bin_width(hduls)

    name = 'spectral_bin_width'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.bin
