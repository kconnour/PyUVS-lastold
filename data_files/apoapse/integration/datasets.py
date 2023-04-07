import warnings

import numpy as np

from data_files import generic
import pyuvs as pu


def make_ephemeris_time(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_ephemeris_time(hduls)


def make_mirror_data_number(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_mirror_data_number(hduls)


def make_mirror_angle(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_mirror_angle(hduls)


def make_field_of_view(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_field_of_view(hduls)


def make_case_temperature(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_case_temperature(hduls)


def make_integration_time(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_integration_time(hduls)


def make_swath_number(orbit: int, hduls: generic.hdulist) -> np.ndarray:
    mirror_angle = make_mirror_angle(hduls)
    swath_number = compute_swath_number(mirror_angle)

    if orbit in []:
        swath_number += 1
    elif orbit in [3965]:
        swath_number += 4

    return swath_number


# TODO: This doesn't account for times when there was a single swath missing in the middle, as with orbit 18150
def compute_swath_number(mirror_angle: np.ndarray) -> np.ndarray:
    """Make the swath number associated with each mirror angle.

    This function assumes the input is all the mirror angles (or, equivalently,
    the field of view) from an orbital segment. Omitting some mirror angles
    may result in nonsensical results. Adding additional mirror angles from
    multiple segments or orbits will certainly result in nonsensical results.

    Parameters
    ----------
    mirror_angle

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

    return swath_number


def make_number_of_swaths(orbit: int, hduls: generic.hdulist) -> np.ndarray:
    swath_number = make_swath_number(orbit, hduls)
    number_of_swaths = np.array([swath_number[-1] + 1]) if swath_number.size > 0 else np.array([])
    if orbit in [3115, 3174, 3211, 3229, 3248, 3375, 3488, 4049, 4122, 4141, 4231, 4780, 6525]:
        number_of_swaths += 1
    elif orbit in [3456, 3581, 3721, 6971, 7241]:
        number_of_swaths += 2
    elif orbit in [7430, 7802, 7876, 8530]:
        number_of_swaths += 4
    return number_of_swaths


def make_opportunity_classification(orbit: int, hduls: generic.hdulist) -> np.ndarray:
    mirror_angle = make_mirror_angle(hduls)
    swath_number = make_swath_number(orbit, hduls)
    return compute_opportunity_classification(mirror_angle, swath_number)


def compute_opportunity_classification(mirror_angle: np.ndarray, swath_number: np.ndarray) -> np.ndarray:
    opportunity_integrations = np.empty(swath_number.shape, dtype='bool')
    for sn in np.unique(swath_number):
        angles = mirror_angle[swath_number == sn]
        relay = pu.minimum_mirror_angle in angles and pu.maximum_mirror_angle in angles
        opportunity_integrations[swath_number == sn] = relay
    return opportunity_integrations
