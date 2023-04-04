from h5py import File
import numpy as np

from data_files.compression import compression, compression_opts
from data_files import units
from data_files import apoapse


path = 'apoapse/spatial_pixel_geometry'


def add_latitude_and_longitude_to_file(file: File) -> None:
    latitude, longitude = _make_along_slit_latitude_and_longitude(file)

    name = 'latitude'
    try:
        dataset = file[path].create_dataset(
            name,
            data=latitude,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = latitude
    dataset.attrs['unit'] = units.latitude

    name = 'longitude'
    try:
        dataset = file[path].create_dataset(
            name,
            data=longitude,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = latitude
    dataset.attrs['unit'] = units.longitude


def _make_along_slit_latitude_and_longitude(file: File) -> tuple[np.ndarray, np.ndarray]:
    et = file['apoapse/integration/ephemeris_time'][:]
    shape = (et.shape[0], 1024)

    latitude = np.zeros(shape)
    longitude = np.zeros(shape)

    for observation in ['dayside', 'failsafe', 'nightside']:
        bin_vector = file[f'apoapse/muv/{observation}/spatial_bin_geometry/bin_vector'][:]
        good_integrations = file[f'apoapse/muv/integration/{observation}_integrations'][:]
        spatial_bin_edges = file[f'apoapse/muv/{observation}/binning/spatial_bin_edges'][:]

        if bin_vector.size == 0:
            continue

        lat, lon = apoapse.pixel_geometry.make_along_slit_lat_lon(bin_vector, spatial_bin_edges, et[good_integrations])
        latitude[good_integrations] = lat
        longitude[good_integrations] = lon
    return latitude, longitude
