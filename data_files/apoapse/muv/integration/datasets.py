import numpy as np

from data_files import generic
import pyuvs as pu


def make_detector_temperature(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_detector_temperature(hduls)


def make_mcp_voltage(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_mcp_voltage(hduls)


def make_mcp_voltage_gain(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_mcp_voltage_gain(hduls)


def make_failsafe_integrations(hduls: generic.hdulist) -> np.ndarray:
    mcp_voltage = make_mcp_voltage(hduls)
    return np.isclose(mcp_voltage, pu.apoapse_muv_failsafe_voltage)


def make_dayside_integrations(hduls: generic.hdulist) -> np.ndarray:
    failsafe_integrations = make_failsafe_integrations(hduls)
    nightside_integrations = make_nightside_integrations(hduls)
    return np.logical_and(~failsafe_integrations, ~nightside_integrations)


def make_nightside_integrations(hduls: generic.hdulist) -> np.ndarray:
    mcp_voltage = make_mcp_voltage(hduls)
    return mcp_voltage > pu.constants.apoapse_muv_day_night_voltage_boundary
