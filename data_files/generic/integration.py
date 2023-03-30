import numpy as np

from data_files.generic.miscellaneous import catch_empty_arrays, get_integrations_per_file
from data_files.generic.typing import hdulist


@catch_empty_arrays
def make_ephemeris_time(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['et'] for f in hduls])


@catch_empty_arrays
def make_mirror_data_number(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['mirror_dn'] for f in hduls])


@catch_empty_arrays
def make_mirror_angle(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['mirror_deg'] for f in hduls])


@catch_empty_arrays
def make_field_of_view(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['fov_deg']for f in hduls])


@catch_empty_arrays
def make_case_temperature(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['case_temp_c'] for f in hduls])


@catch_empty_arrays
def make_integration_time(hduls: hdulist) -> np.ndarray:
    integrations_per_file = get_integrations_per_file(hduls)
    integration_time = [f['observation'].data['int_time'][0] for f in hduls]
    return np.repeat(integration_time, integrations_per_file)
