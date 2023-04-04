from h5py import File

from data_files import generic
from data_files.compression import compression, compression_opts
from data_files import units
from data_files import apoapse


path = 'apoapse/muv/nightside/binning'


def add_spatial_bin_edges_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.binning.make_spatial_bin_edges(hduls)

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
    data = apoapse.muv.nightside.binning.make_spectral_bin_edges(hduls)

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


def add_spatial_bin_size_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.binning.make_spatial_bin_size(hduls)

    name = 'spatial_bin_size'
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


def add_spectral_bin_size_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.binning.make_spectral_bin_size(hduls)

    name = 'spectral_bin_size'
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
