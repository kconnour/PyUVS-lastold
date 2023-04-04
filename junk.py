from astropy.io import fits
from pathlib import Path
import numpy as np


def add_leading_axis_if_necessary(data: np.ndarray, expected_axes: int) -> list[np.ndarray]:
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
    return data if np.ndim(data) == expected_axes else data[None, :]


p = Path('/media/kyle/iuvs/production/orbit03000')
files = sorted(p.glob('*apoapse*orbit03000*muv*.gz'))
hduls = [fits.open(f) for f in files]

for h in hduls:
    print(h['primary'].shape)
    print(add_leading_axis_if_necessary(h['primary'].data, 3).shape)
    print('~'*30)
'''for file in files:
    hdul = fits.open(file)
    print(hdul['primary'].data.shape)
    foo = add_leading_axis_if_necessary(hdul['primary'].data, 3)
    print(foo[0].shape)'''
