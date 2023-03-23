import numpy as np

from data_files.generic.helper import catch_empty_arrays
from data_files.generic.iuvs_fits import get_integration_ephemeris_time


@catch_empty_arrays
def get_ephemeris_time(hduls: list) -> np.ndarray:
    return np.concatenate([get_integration_ephemeris_time(f) for f in hduls])
