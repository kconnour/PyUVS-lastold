"""This module contains functions I don't have another place for.
"""
import numpy as np
from data_files.generic.typing import hdulist


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


def get_integrations_per_file(hduls: hdulist) -> list[int]:
    return [f['integration'].data['et'].shape[0] for f in hduls]
