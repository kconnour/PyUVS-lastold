import numpy as np

from data_files.generic.typing import hdulist


def make_spatial_bin_edges(hduls: hdulist) -> np.ndarray:
    if not hduls:
        return np.array([])
    spatial_pixel_low = np.array([np.squeeze(f['binning'].data['spapixlo']) for f in hduls])
    spatial_pixel_high = np.array([np.squeeze(f['binning'].data['spapixhi']) for f in hduls])
    if not np.all(spatial_pixel_low == spatial_pixel_low[0]) or not np.all(spatial_pixel_high == spatial_pixel_high[0]):
        raise ValueError('The spatial binning is not the same.')
    return np.append(spatial_pixel_low[0], spatial_pixel_high[0, -1] + 1)


def make_spectral_bin_edges(hduls: hdulist) -> np.ndarray:
    if not hduls:
        return np.array([])
    spectral_pixel_low = np.array([np.squeeze(f['binning'].data['spepixlo']) for f in hduls])
    spectral_pixel_high = np.array([np.squeeze(f['binning'].data['spepixhi']) for f in hduls])
    if not np.all(spectral_pixel_low == spectral_pixel_low[0]) or not np.all(spectral_pixel_high == spectral_pixel_high[0]):
        raise ValueError('The spectral binning is not the same.')
    return np.append(spectral_pixel_low[0], spectral_pixel_high[0, -1] + 1)


def make_spatial_bin_width(hduls: hdulist) -> np.ndarray:
    if not hduls:
        return np.array([])
    bin_size = np.array([f['primary'].header['spa_size'] for f in hduls])
    if not np.all(bin_size == bin_size[0]):
        raise ValueError('The spatial bin width is not the same.')
    return np.array([bin_size[0]])


def make_spectral_bin_width(hduls: hdulist) -> np.ndarray:
    if not hduls:
        return np.array([])
    bin_size = np.array([f['primary'].header['spe_size'] for f in hduls])
    if not np.all(bin_size == bin_size[0]):
        raise ValueError('The spectral bin width is not the same.')
    return np.array([bin_size[0]])


def make_bin_table_name(hduls: hdulist) -> np.ndarray:
    if not hduls:
        return np.array([])
    bin_table_name = np.array([f['binning'].data['bintablename'][0] for f in hduls])
    if not np.all(bin_table_name == bin_table_name[0]):
        raise ValueError('The bin table is not the same.')
    return np.array([bin_table_name[0]])
