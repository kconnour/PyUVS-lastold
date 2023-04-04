import numpy as np

from data_files import generic


def make_along_slit_lat_lon(bin_vector: np.ndarray, spatial_bin_edges: np.ndarray, ephemeris_time: np.ndarray) -> \
        tuple[np.ndarray, np.ndarray]:
    bin_vector = generic.extrapolate_bin_pixel_vector_to_native_vector(bin_vector, spatial_bin_edges)
    bin_vector = np.moveaxis(np.moveaxis(bin_vector, -1, 0) / np.sum(bin_vector, axis=-1), 0, -1)

    latitude = np.zeros(bin_vector.shape[:-1]) * np.nan
    longitude = np.zeros(bin_vector.shape[:-1]) * np.nan

    for integration in range(bin_vector.shape[0]):
        for spatial_bin in range(bin_vector.shape[1]):
            lat, lon = generic.spice.compute_lat_lon_point(ephemeris_time[integration], bin_vector[integration, spatial_bin, :])
            latitude[integration, spatial_bin] = lat
            longitude[integration, spatial_bin] = lon

    return latitude, longitude
