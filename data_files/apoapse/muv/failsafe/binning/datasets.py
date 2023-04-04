import numpy as np

from data_files import generic


def make_spatial_bin_edges(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_edges(hduls)


def make_spectral_bin_edges(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spectral_bin_edges(hduls)


def make_spatial_bin_width(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spatial_bin_width(hduls)


def make_spectral_bin_width(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_spectral_bin_width(hduls)


def make_bin_table_name(hduls: generic.hdulist) -> np.ndarray:
    return generic.make_bin_table_name(hduls)
