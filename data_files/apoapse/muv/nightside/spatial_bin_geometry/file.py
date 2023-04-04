from h5py import File

from data_files import generic
from data_files.compression import compression, compression_opts
from data_files import units
from data_files import apoapse


path = 'apoapse/muv/nightside/spatial_bin_geometry'


def add_latitude_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.spatial_bin_geometry.make_spatial_bin_latitude(hduls)

    name = 'latitude'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.latitude


def add_longitude_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.spatial_bin_geometry.make_spatial_bin_longitude(hduls)

    name = 'longitude'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.longitude


def add_tangent_altitude_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.spatial_bin_geometry.make_spatial_bin_tangent_altitude(hduls)

    name = 'tangent_altitude'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.altitude


def add_tangent_altitude_rate_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.spatial_bin_geometry.make_spatial_bin_tangent_altitude_rate(hduls)

    name = 'tangent_altitude_rate'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.velocity


def add_line_of_sight_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.spatial_bin_geometry.make_spatial_bin_line_of_sight(hduls)

    name = 'line_of_sight'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data


def add_solar_zenith_angle_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.spatial_bin_geometry.make_spatial_bin_solar_zenith_angle(hduls)

    name = 'solar_zenith_angle'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.angle


def add_emission_angle_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.spatial_bin_geometry.make_spatial_bin_emission_angle(hduls)

    name = 'emission_angle'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.angle


def add_phase_angle_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.spatial_bin_geometry.make_spatial_bin_phase_angle(hduls)

    name = 'phase_angle'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.angle


def add_zenith_angle_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.spatial_bin_geometry.make_spatial_bin_zenith_angle(hduls)

    name = 'zenith_angle'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.angle


def add_local_time_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.spatial_bin_geometry.make_spatial_bin_local_time(hduls)

    name = 'local_time'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.local_time


def add_right_ascension_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.spatial_bin_geometry.make_spatial_bin_right_ascension(hduls)

    name = 'right_ascension'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.angle


def add_declination_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.spatial_bin_geometry.make_spatial_bin_declination(hduls)

    name = 'declination'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.angle


def add_bin_vector_to_file(file: File, hduls: generic.hdulist) -> None:
    data = apoapse.muv.nightside.spatial_bin_geometry.make_spatial_bin_vector(hduls)

    name = 'bin_vector'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.unit_vector
