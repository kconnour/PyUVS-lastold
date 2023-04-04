import numpy as np

from data_files.generic.miscellaneous import get_integrations_per_file
from data_files.generic.hdulist import hdulist


def make_ephemeris_time(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['et'] for f in hduls]) if hduls else np.array([])


def make_mirror_data_number(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['mirror_dn'] for f in hduls]) if hduls else np.array([])


def make_mirror_angle(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['mirror_deg'] for f in hduls]) if hduls else np.array([])


def make_field_of_view(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['fov_deg']for f in hduls]) if hduls else np.array([])


def make_case_temperature(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['case_temp_c'] for f in hduls]) if hduls else np.array([])


def make_integration_time(hduls: hdulist) -> np.ndarray:
    integrations_per_file = get_integrations_per_file(hduls)
    integration_time = [f['observation'].data['int_time'][0] for f in hduls]
    return np.repeat(integration_time, integrations_per_file)


def make_detector_temperature(hduls: hdulist) -> np.ndarray:
    return np.concatenate([f['integration'].data['det_temp_c'] for f in hduls]) if hduls else np.array([])


def make_mcp_voltage(hduls: hdulist) -> np.ndarray:
    integrations_per_file = get_integrations_per_file(hduls)
    return np.concatenate([np.repeat(f['observation'].data['mcp_volt'][0], integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])


def make_mcp_voltage_gain(hduls: hdulist) -> np.ndarray:
    integrations_per_file = get_integrations_per_file(hduls)
    return np.concatenate([np.repeat(f['observation'].data['mcp_gain'][0], integrations_per_file[c]) for c, f in enumerate(hduls)]) if hduls else np.array([])
