import warnings

import numpy as np

from data_files.generic.typing import hdulist
from data_files.generic.miscellaneous import add_leading_axis_if_necessary
import pyuvs as pu


def make_detector_raw(hduls: hdulist) -> np.ndarray:
    return np.vstack([add_leading_axis_if_necessary(f['detector_raw'].data, 3) for f in hduls]) if hduls else np.array([])


def make_detector_dark_subtracted(hduls: hdulist) -> np.ndarray:
    return np.vstack([add_leading_axis_if_necessary(f['detector_dark_subtracted'].data, 3) for f in hduls]) if hduls else np.array([])


def _make_muv_flatfield(spatial_bin_edges: np.ndarray, spectral_bin_edges: np.ndarray) -> np.ndarray:
    original_flatfield = pu.load_muv_flatfield()

    spatial_bins = spatial_bin_edges.shape[0] - 1
    spectral_bins = spectral_bin_edges.shape[0] - 1

    new_flatfield = np.zeros((spatial_bins, spectral_bins))
    for spatial_bin in range(spatial_bins):
        for spectral_bin in range(spectral_bins):
            new_flatfield[spatial_bin, spectral_bin] = np.mean(
                original_flatfield[spatial_bin_edges[spatial_bin]: spatial_bin_edges[spatial_bin + 1],
                spectral_bin_edges[spectral_bin]: spectral_bin_edges[spectral_bin + 1]])
    return new_flatfield


def _make_gain_correction(dark_subtracted, spatial_bin_width, spectral_bin_width, integration_time, mcp_volt, mcp_gain):
    """

    Parameters
    ----------
    dds: np.ndarray
        The detector dark subtacted
    spa_size: int
        The number of detector pixels in a spatial bin
    spe_size: int
        The number of detector pixels in a spectral bin
    integration_time
    mcp_volt
    mcp_gain

    Returns
    -------

    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        volt_array = pu.load_voltage()
        ab = pu.load_voltage_coefficients()
        ref_mcp_gain = 50.909455

        normalized_img = dark_subtracted.T / integration_time / spatial_bin_width / spectral_bin_width

        a = np.interp(mcp_volt, volt_array, ab[:, 0])
        b = np.interp(mcp_volt, volt_array, ab[:, 1])

        norm_img = np.exp(a + b * np.log(normalized_img))
        return (norm_img / normalized_img * mcp_gain / ref_mcp_gain).T


def make_brightness(dark_subtracted: np.ndarray, spatial_bin_edges: np.ndarray, spectral_bin_edges: np.ndarray,
                    spatial_bin_width: int, spectral_bin_width: int, integration_time: np.ndarray,
                    mcp_voltage: np.ndarray, mcp_voltage_gain: np.ndarray) -> np.ndarray:
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        if dark_subtracted.size > 0:
            # Get the flatfield
            flatfield = _make_muv_flatfield(spatial_bin_edges, spectral_bin_edges)

            # The sensitivity curve is currently 512 elements. Make it (1024,) for simplicity
            sensitivity_curve = pu.load_muv_sensitivity_curve()[1]
            sensitivity_curve = np.repeat(sensitivity_curve, 2)

            # Get the sensitivity in each spectral bin
            # For array shape reasons, I spread this out over several lines
            rebinned_sensitivity_curve = np.array([np.mean(sensitivity_curve[spectral_bin_edges[i]:spectral_bin_edges[i + 1]]) for i in range(spectral_bin_edges.shape[0] - 1)])
            partial_corrected_brightness = dark_subtracted / rebinned_sensitivity_curve * 4 * np.pi * 10 ** -9 / pu.pixel_angular_size / spatial_bin_width
            partial_corrected_brightness = (partial_corrected_brightness.T / mcp_voltage_gain / integration_time).T

            # Finally, do the voltage gain and flatfield corrections
            voltage_correction = _make_gain_correction(dark_subtracted, spatial_bin_width, spectral_bin_width, integration_time, mcp_voltage, mcp_voltage_gain)
            data = partial_corrected_brightness / flatfield * voltage_correction

            # If the data have negative DNs, then they become NaNs during the voltage correction
            data[np.isnan(data)] = 0
        else:
            data = np.array([])
        return data
