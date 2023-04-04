from h5py import File
import numpy as np

from data_files import generic


def make_raw(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_detector_raw(hduls)


def make_dark_subtracted(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_detector_dark_subtracted(hduls)


def make_brightness(file: File) -> np.ndarray:
    good_integrations = file['apoapse/muv/integration/failsafe_integrations'][:]

    dark_subtracted = file['apoapse/muv/failsafe/detector/dark_subtracted'][:]
    spatial_bin_edges = file['apoapse/muv/failsafe/binning/spatial_bin_edges'][:]
    spectral_bin_edges = file['apoapse/muv/failsafe/binning/spectral_bin_edges'][:]
    spatial_bin_width = file['apoapse/muv/failsafe/binning/spatial_bin_width'][:]
    spectral_bin_width = file['apoapse/muv/failsafe/binning/spectral_bin_width'][:]
    integration_time = file['apoapse/integration/integration_time'][good_integrations]
    mcp_voltage = file['apoapse/muv/integration/mcp_voltage'][good_integrations]
    mcp_voltage_gain = file['apoapse/muv/integration/mcp_voltage_gain'][good_integrations]

    return generic.make_brightness(dark_subtracted, spatial_bin_edges, spectral_bin_edges, spatial_bin_width,
                                   spectral_bin_width, integration_time, mcp_voltage, mcp_voltage_gain)
