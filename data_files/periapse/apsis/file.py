from h5py import File

from data_files.compression import compression, compression_opts
from data_files import units
from data_files import periapse


path = 'periapse/apsis'


def add_ephemeris_time_to_file(file: File) -> None:
    orbit = file.attrs['orbit']
    data = periapse.apsis.make_ephemeris_time(orbit)

    name = 'ephemeris_time'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.ephemeris_time


def add_mars_year_to_file(file: File) -> None:
    orbit = file.attrs['orbit']
    data = periapse.apsis.make_mars_year(orbit)

    name = 'mars_year'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.mars_year


def add_sol_to_file(file: File) -> None:
    orbit = file.attrs['orbit']
    data = periapse.apsis.make_sol(orbit)

    name = 'sol'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.sol


def add_solar_longitude_to_file(file: File) -> None:
    orbit = file.attrs['orbit']
    data = periapse.apsis.make_solar_longitude(orbit)

    name = 'solar_longitude'
    try:
        dataset = file[path].create_dataset(
            name,
            data=data,
            compression=compression,
            compression_opts=compression_opts)
    except ValueError:
        dataset = file[f'{path}/{name}']
        dataset[...] = data
    dataset.attrs['unit'] = units.solar_longitude


def add_subsolar_latitude_to_file(file: File) -> None:
    orbit = file.attrs['orbit']
    data = periapse.apsis.make_subsolar_latitude(orbit)

    name = 'subsolar_latitude'
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


def add_subsolar_longitude_to_file(file: File) -> None:
    orbit = file.attrs['orbit']
    data = periapse.apsis.make_subsolar_longitude(orbit)

    name = 'subsolar_longitude'
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


def add_subspacecraft_latitude_to_file(file: File) -> None:
    orbit = file.attrs['orbit']
    data = periapse.apsis.make_subspacecraft_latitude(orbit)

    name = 'subspacecraft_latitude'
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


def add_subspacecraft_longitude_to_file(file: File) -> None:
    orbit = file.attrs['orbit']
    data = periapse.apsis.make_subspacecraft_longitude(orbit)

    name = 'subspacecraft_longitude'
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


def add_subspacecraft_altitude_to_file(file: File) -> None:
    orbit = file.attrs['orbit']
    data = periapse.apsis.make_subspacecraft_altitude(orbit)

    name = 'subspacecraft_altitude'
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


def add_subspacecraft_local_time_to_file(file: File) -> None:
    orbit = file.attrs['orbit']
    data = periapse.apsis.make_subspacecraft_local_time(orbit)

    name = 'subspacecraft_local_time'
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


def add_mars_sun_distance_to_file(file: File) -> None:
    orbit = file.attrs['orbit']
    data = periapse.apsis.make_mars_sun_distance(orbit)

    name = 'mars_sun_distance'
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


def add_subsolar_subspacecraft_angle_to_file(file: File) -> None:
    orbit = file.attrs['orbit']
    data = periapse.apsis.make_subsolar_subspacraft_angle(orbit)

    name = 'subsolar_subspacecraft_angle'
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
