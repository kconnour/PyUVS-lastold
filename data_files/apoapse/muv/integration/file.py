from h5py import File

from data_files import generic
from data_files.compression import compression, compression_opts
from data_files import units
from data_files import apoapse


path = 'apoapse/muv/integration'


def add_detector_temperature_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.integration.make_detector_temperature(hduls)

    name = 'detector_temperature'
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


def add_mcp_voltage_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.integration.make_mcp_voltage(hduls)

    name = 'mcp_voltage'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.voltage


def add_mcp_voltage_gain_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.integration.make_mcp_voltage_gain(hduls)

    name = 'mcp_voltage_gain'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.voltage


def add_failsafe_integrations_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.integration.make_failsafe_integrations(hduls)

    name = 'failsafe_integrations'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data


def add_dayside_integrations_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.integration.make_dayside_integrations(hduls)

    name = 'dayside_integrations'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data


def add_nightside_integrations_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.integration.make_nightside_integrations(hduls)

    name = 'nightside_integrations'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
