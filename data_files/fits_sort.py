from pathlib import Path

from astropy.io import fits
import numpy as np

import pyuvs as pu


def _get_segment_orbit_channel_fits_file_paths(iuvs_fits_file_location: Path, segment: str, orbit: int, channel: str) -> list[Path]:
    orbit_block = pu.make_orbit_block(orbit)
    orbit_code = pu.make_orbit_code(orbit)
    return sorted((iuvs_fits_file_location / orbit_block).glob(f'*{segment}*{orbit_code}*{channel}*.gz'))


def _remove_files_with_oulier_obs_id(hduls: list[fits.hdu.hdulist.HDUList], obs_id: list[int]) -> list:
    median_obs_id = np.median(obs_id)
    outlier_files = [f for c, f in enumerate(hduls) if obs_id[c] != median_obs_id]
    for file in outlier_files:
        hduls.remove(file)
    return hduls


def _get_apoapse_fits_files(iuvs_fits_file_location: Path, orbit: int, segment: str) -> list[fits.hdu.hdulist.HDUList]:
    # Test case: orbit 7857 has outbound file as file index 0 with a strange obs id
    data_file_paths = _get_segment_orbit_channel_fits_file_paths(iuvs_fits_file_location, 'apoapse', orbit, segment)
    hduls = [fits.open(f) for f in data_file_paths]
    obs_id = [pu.iuvs_fits.get_observation_id(f) for f in hduls]
    return _remove_files_with_oulier_obs_id(hduls, obs_id)


def get_apoapse_muv_fits_files(orbit: int, iuvs_fits_file_location: Path) -> list[fits.hdu.hdulist.HDUList]:
    return _get_apoapse_fits_files(iuvs_fits_file_location, orbit, 'muv')


def get_apoapse_muv_failsafe_files(orbit: int, iuvs_fits_file_location: Path) -> list[fits.hdu.hdulist.HDUList]:
    apoapse_hduls = get_apoapse_muv_fits_files(orbit, iuvs_fits_file_location)
    mcp_voltage = [pu.iuvs_fits.get_mcp_voltage(f) for f in apoapse_hduls]
    failsafe = [np.isclose(f, pu.apoapse_muv_failsafe_voltage) for f in mcp_voltage]
    return [f for c, f in enumerate(apoapse_hduls) if failsafe[c]]


def get_apoapse_muv_dayside_files(orbit: int, iuvs_fits_file_location: Path) -> list[fits.hdu.hdulist.HDUList]:
    apoapse_hduls = get_apoapse_muv_fits_files(orbit, iuvs_fits_file_location)
    apoapse_failsafe_hduls = get_apoapse_muv_failsafe_files(orbit, iuvs_fits_file_location)
    apoapse_nightside_hduls = get_apoapse_muv_nightside_files(orbit, iuvs_fits_file_location)
    return [f for f in apoapse_hduls if f not in apoapse_failsafe_hduls and f not in apoapse_nightside_hduls]


def get_apoapse_muv_nightside_files(orbit: int, iuvs_fits_file_location: Path) -> list[fits.hdu.hdulist.HDUList]:
    apoapse_hduls = get_apoapse_muv_fits_files(orbit, iuvs_fits_file_location)
    mcp_voltage = [pu.iuvs_fits.get_mcp_voltage(f) for f in apoapse_hduls]
    nightside = [f >= pu.apoapse_muv_day_night_voltage_boundary for f in mcp_voltage]
    return [f for c, f in enumerate(apoapse_hduls) if nightside[c]]
