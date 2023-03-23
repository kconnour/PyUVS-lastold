import warnings

from astropy.io import fits
from h5py import File
import numpy as np

from data_files.compression import compression, compression_opts
from data_files.helper import catch_empty_arrays, get_integrations_per_file
from data_files import iuvs_fits
from data_files import units
from pyuvs import minimum_mirror_angle, maximum_mirror_angle


path = 'apoapse/integration'


@catch_empty_arrays
def make_ephemeris_time(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_integration_ephemeris_time(f) for f in hduls])


@catch_empty_arrays
def make_mirror_data_number(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_integration_mirror_data_number(f) for f in hduls])


@catch_empty_arrays
def make_mirror_angle(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_integration_mirror_angle(f) for f in hduls])


@catch_empty_arrays
def make_field_of_view(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_integration_field_of_view(f) for f in hduls])


@catch_empty_arrays
def make_case_temperature(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    return np.concatenate([iuvs_fits.get_integration_case_temperature(f) for f in hduls])


@catch_empty_arrays
def make_integration_time(hduls: list[fits.hdu.hdulist.HDUList]) -> np.ndarray:
    integrations_per_file = get_integrations_per_file(hduls)
    integration_time = [iuvs_fits.get_integration_time(f) for f in hduls]
    return np.repeat(integration_time, integrations_per_file)


# TODO: This doesn't account for times when there was a single swath missing in the middle, as with once in Jan 2023 data
def make_swath_number(orbit: int, mirror_angle: np.ndarray) -> np.ndarray:
    """Make the swath number associated with each mirror angle.

    This function assumes the input is all the mirror angles (or, equivalently,
    the field of view) from an orbital segment. Omitting some mirror angles
    may result in nonsensical results. Adding additional mirror angles from
    multiple segments or orbits will certainly result in nonsensical results.

    Returns
    -------
    np.ndarray
        The swath number associated with each mirror angle.

    Notes
    -----
    This algorithm assumes the mirror in roughly constant step sizes except
    when making a swath jump. It finds the median step size and then uses
    this number to find swath discontinuities. It interpolates between these
    indices and takes the floor of these values to get the integer swath
    number.

    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        mirror_change = np.diff(mirror_angle)
        threshold = np.abs(np.median(mirror_change)) * 4
        mirror_discontinuities = np.where(np.abs(mirror_change) > threshold)[0] + 1
        if any(mirror_discontinuities):
            n_swaths = len(mirror_discontinuities) + 1
            integrations = range(len(mirror_angle))
            interp_swaths = np.interp(integrations, mirror_discontinuities, range(1, n_swaths), left=0)
            swath_number = np.floor(interp_swaths).astype('int')
        else:
            swath_number = np.zeros(mirror_angle.shape)

    if orbit in []:
        swath_number += 1
    elif orbit in [3965]:
        swath_number += 4
    return swath_number


def make_number_of_swaths(orbit: int, swath_number: np.ndarray) -> np.ndarray:
    number_of_swaths = np.array([swath_number[-1] + 1]) if swath_number.size > 0 else np.array([])
    if orbit in [3115, 3174, 3211, 3229, 3248, 3375, 3488, 3688, 3692]:
        number_of_swaths += 1
    elif orbit in [3456, 3581]:
        number_of_swaths += 2
    elif orbit in [3721]:
        number_of_swaths += 3
    return number_of_swaths


def make_opportunity_classification(orbit: int, mirror_angle: np.ndarray, swath_number: np.ndarray) -> np.ndarray:
    # I put in orbit as a parameter for future expansion
    opportunity_integrations = np.empty(swath_number.shape, dtype='bool')
    for sn in np.unique(swath_number):
        angles = mirror_angle[swath_number == sn]
        relay = minimum_mirror_angle in angles and maximum_mirror_angle in angles
        opportunity_integrations[swath_number == sn] = relay
    return opportunity_integrations


def add_ephemeris_time_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_ephemeris_time(hduls)
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


def add_mirror_data_number_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_mirror_data_number(hduls)
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


def add_mirror_angle_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_mirror_angle(hduls)
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


def add_field_of_view_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_field_of_view(hduls)
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


def add_case_temperature_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_case_temperature(hduls)
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


def add_integration_time_to_file(file: File, hduls: list[fits.hdu.hdulist.HDUList]) -> None:
    data = make_integration_time(hduls)
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
    data = make_swath_number(file.attrs['orbit'], file[f'{path}/mirror_angle'][:])
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
    data = make_number_of_swaths(file.attrs['orbit'], file[f'{path}/swath_number'][:])
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
    data = make_opportunity_classification(file.attrs['orbit'], file[f'{path}/mirror_angle'][:], file[f'{path}/swath_number'][:])
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
