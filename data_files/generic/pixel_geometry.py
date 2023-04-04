import numpy as np
from scipy.interpolate import interp1d


def extrapolate_bin_pixel_vector_to_native_vector(pixel_vector: np.ndarray, spatial_bin_edges: np.ndarray) -> np.ndarray:
    # shape: (n_integrations, n_spatial_bins, 5, 3)
    spatial_bin_center = (spatial_bin_edges[:-1] + spatial_bin_edges[1:]) / 2
    f = interp1d(spatial_bin_center, pixel_vector[:, :, 4, :], kind='linear', axis=1, fill_value='extrapolate')
    return f(np.arange(1024) + 0.5)
