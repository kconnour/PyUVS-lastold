"""This module contains functions I don't have another place for.
"""
from astropy.io import fits
import numpy as np

from data.iuvs_fits import Level1a


def catch_empty_arrays(func: callable):
    """Return an empty array if an empty list is passed to a function. This is only designed for use as a decorator.

    Parameters
    ----------
    func

    Returns
    -------

    """
    def wrapper(hduls: list[fits.hdu.hdulist.HDUList], *args):
        return func(hduls, *args) if hduls else np.array([])
    return wrapper


def add_leading_axis_if_necessary(data: list[np.ndarray], expected_axes: int) -> list[np.ndarray]:
    """Add a leading axis to a list of arrays such that each array has the expected number of axes.

    Parameters
    ----------
    data
        Any list of arrays.
    expected_axes
        The expected number of axes each array should have.

    Returns
    -------
    list[np.ndarray]
       The original data with dimensions added if necessary.

    Notes
    -----
    I assume the IUVS data can only be smaller than the expected number of dimensions by up to one dimension.

    """
    return [f if np.ndim(f) == expected_axes else f[None, :] for f in data if f.size > 0]


def get_integrations_per_file(hduls: list[Level1a]) -> list[int]:
    et = [f.get_integration_ephemeris_time() for f in hduls]
    return [f.shape[0] for f in et]
