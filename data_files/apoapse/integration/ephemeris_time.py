from h5py import File

import pyuvs as pu
from data_files.generic.ephemeris_time import get_ephemeris_time
from data_files.compression import compression, compression_opts


def add_ephemeris_time_to_file(file: File, hduls: list) -> None:
    data = get_ephemeris_time(hduls)
    try:
        dataset = file['apoapse/integration'].create_dataset(
            'ephemeris_time',
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file['apoapse/integration/ephemeris_time']
        dataset[...] = data
    dataset.attrs['unit'] = pu.units.ephemeris_time
