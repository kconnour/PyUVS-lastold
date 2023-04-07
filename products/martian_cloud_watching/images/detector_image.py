import multiprocessing as mp
from pathlib import Path

from h5py import File
import matplotlib.pyplot as plt
import numpy as np

import products.graphics as graphics
import pyuvs as pu
from _filename import make_filename


def setup_figure(n_swaths: int, angular_width: float, height: float) -> tuple[plt.Figure, plt.Axes]:
    field_of_view = (pu.constants.maximum_mirror_angle - pu.constants.minimum_mirror_angle) * 2
    width = n_swaths * angular_width / field_of_view * height
    fig = plt.figure(figsize=(width, height))
    ax = fig.add_axes([0, 0, 1, 1])
    return fig, ax


def make_histogram_equalized_detector_image(orbit: int) -> None:
    orbit_block = pu.orbit.make_orbit_block(orbit)
    orbit_code = pu.orbit.make_orbit_code(orbit)

    f = File(file_path / orbit_block / f'{orbit_code}.hdf5')

    dayside = f['apoapse/muv/integration/dayside_integrations'][:]
    opportunity_swaths = f['apoapse/integration/opportunity_classification'][:]
    dayside_science_integrations = np.logical_and(dayside, ~opportunity_swaths)

    if np.sum(dayside_science_integrations) == 0:
        return

    brightness = f['apoapse/muv/dayside/detector/brightness'][~opportunity_swaths[dayside]]
    swath_number = f['apoapse/integration/swath_number'][:][dayside_science_integrations]
    n_swaths = f['apoapse/integration/number_of_swaths'][:][0]
    tangent_altitude = f['apoapse/muv/dayside/spatial_bin_geometry/tangent_altitude'][:][..., 4]
    field_of_view = f['apoapse/integration/field_of_view'][:][dayside_science_integrations]
    solar_zenith_angle = f['apoapse/muv/dayside/spatial_bin_geometry/solar_zenith_angle'][:]
    spatial_bin_edges = f['apoapse/muv/dayside/binning/spatial_bin_edges'][:]
    app_flip = f['apoapse/instrument_geometry/app_flip'][0]

    solar_zenith_angle[tangent_altitude != 0] = np.nan

    mask = np.logical_and(tangent_altitude == 0, solar_zenith_angle <= 102)
    try:
        image = graphics.histogram_equalize_detector_image(brightness, mask=mask) / 255
    except IndexError:
        return

    angular_width = (spatial_bin_edges[-1] - spatial_bin_edges[0]) / 1024 * pu.constants.angular_detector_width

    fig, ax = setup_figure(n_swaths, angular_width, 6)

    graphics.plot_rgb_detector_image_in_axis(ax, image, swath_number, field_of_view, angular_width, app_flip)
    graphics.add_terminator_contour_line_to_axis(ax, solar_zenith_angle, swath_number, field_of_view, angular_width, app_flip)

    ax.set_xlim(0, angular_width * n_swaths)
    ax.set_ylim(pu.constants.minimum_mirror_angle * 2, pu.constants.maximum_mirror_angle * 2) if app_flip \
        else ax.set_ylim(pu.constants.maximum_mirror_angle * 2, pu.constants.minimum_mirror_angle * 2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('k')

    # Get info I need for the filename
    solar_longitude = f['apoapse/apsis/solar_longitude'][:][0]
    subsolar_subspacecraft_angle = f['apoapse/apsis/subsolar_subspacecraft_angle'][:][0]
    spatial_bin_width = f['apoapse/muv/dayside/binning/spatial_bin_edges'][:].shape[0] - 1
    spectral_bin_width = f['apoapse/muv/dayside/binning/spectral_bin_edges'][:].shape[0] - 1

    filename = make_filename(orbit_code, solar_longitude, subsolar_subspacecraft_angle, spatial_bin_width, spectral_bin_width, 'heq', 'ql')
    save = save_location / pu.make_orbit_block(orbit) / filename
    save.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save)
    plt.close(fig)


def make_square_root_scaled_detector_image(orbit: int) -> None:
    orbit_block = pu.orbit.make_orbit_block(orbit)
    orbit_code = pu.orbit.make_orbit_code(orbit)

    f = File(file_path / orbit_block / f'{orbit_code}_v01.hdf5')

    dayside = f['apoapse/muv/integration/dayside'][:]
    brightness = f['apoapse/muv/dayside/detector/brightness'][:]

    if brightness.size == 0:
        return

    print(orbit)
    swath_number = f['apoapse/integration/swath_number'][:][dayside]
    n_swaths = f['apoapse/integration/n_swaths'][:][0]
    tangent_altitude = f['apoapse/muv/dayside/spatial_bin_geometry/tangent_altitude'][:][..., 4]
    field_of_view = f['apoapse/integration/field_of_view'][:][dayside]
    solar_zenith_angle = f['apoapse/muv/dayside/spatial_bin_geometry/solar_zenith_angle'][:]
    spatial_bin_edges = f['apoapse/muv/dayside/binning/spatial_bin_edges'][:]

    solar_zenith_angle[tangent_altitude != 0] = np.nan

    mask = np.logical_and(tangent_altitude == 0, solar_zenith_angle <= 102)
    try:
        image = graphics.square_root_scale_detector_image(brightness, mask=mask) / 255
    except IndexError:
        return

    angular_width = (spatial_bin_edges[-1] - spatial_bin_edges[0]) / 1024 * pu.constants.angular_detector_width

    fig, ax = setup_figure(n_swaths, angular_width, 6)

    graphics.plot_rgb_detector_image_in_axis(ax, image, swath_number, field_of_view, angular_width)
    graphics.add_terminator_contour_line_to_axis(ax, solar_zenith_angle, swath_number, field_of_view, angular_width)

    ax.set_xlim(0, angular_width * n_swaths)
    ax.set_ylim(pu.constants.minimum_mirror_angle * 2, pu.constants.maximum_mirror_angle * 2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('k')

    # Get info I need for the filename
    solar_longitude = f['apoapse/apsis/solar_longitude'][:][0]
    subsolar_subspacecraft_angle = f['apoapse/apsis/subsolar_subspacecraft_angle'][:][0]
    spatial_bin_width = f['apoapse/muv/dayside/binning/spatial_bin_edges'][:].shape[0] - 1
    spectral_bin_width = f['apoapse/muv/dayside/binning/spectral_bin_edges'][:].shape[0] - 1

    filename = make_filename(orbit_code, solar_longitude, subsolar_subspacecraft_angle, spatial_bin_width, spectral_bin_width, 'sqrt', 'ql')
    plt.savefig(save_location / filename)
    plt.close(fig)


def make_geometry_detector_image(orbit: int) -> None:
    orbit_block = pu.orbit.make_orbit_block(orbit)
    orbit_code = pu.orbit.make_orbit_code(orbit)

    f = File(file_path / orbit_block / f'{orbit_code}_v01.hdf5')

    latitude = f['apoapse/pixel_geometry/latitude'][:]
    longitude = f['apoapse/pixel_geometry/longitude'][:]

    if latitude.size == 0:
        return

    print(orbit)
    swath_number = f['apoapse/integration/swath_number'][:]
    field_of_view = f['apoapse/integration/field_of_view'][:]

    mars_map = pu.anc.load_map_mars_surface()

    print(np.nanmin(latitude), np.nanmax(latitude))
    print(np.nanmin(longitude), np.nanmax(longitude))
    print(latitude.shape, mars_map.shape)

    off_disk_mask = np.isnan(latitude)

    latitude[off_disk_mask] = 0
    longitude[off_disk_mask] = 0

    latitude_indices = np.floor((latitude + 90) * 10).astype('int')
    longitude_indices = np.floor(longitude * 10).astype('int')

    rgb_image = mars_map[latitude_indices.flatten(), longitude_indices.flatten(), :]
    rgb_image = np.reshape(rgb_image, latitude.shape + (4,))
    rgb_image[off_disk_mask] = 0

    fig, ax = setup_figure(swath_number[-1] + 1, 6)

    for swath in np.unique(swath_number):
        swath_indices = swath_number == swath
        n_integrations = np.sum(swath_indices)
        fov = field_of_view[swath_indices]
        x, y = pu.detector_image.make_swath_grid(fov, swath, 1024, n_integrations)
        pu.detector_image.pcolormesh_rgb_detector_image(ax, rgb_image[swath_indices], x, y)

    ax.set_xlim(0, pu.constants.angular_slit_width * (swath_number[-1] + 1))
    ax.set_ylim(pu.constants.minimum_mirror_angle * 2, pu.constants.maximum_mirror_angle * 2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('k')

    # Get info I need for the filename
    solar_longitude = f['apoapse/apsis/solar_longitude'][:][0]
    subsolar_subspacecraft_angle = f['apoapse/apsis/subsolar_subspacecraft_angle'][:][0]
    spatial_binning = f['apoapse/muv/dayside/binning/spatial_bin_edges'][:].shape[0] - 1
    spectral_binning = f['apoapse/muv/dayside/binning/spectral_bin_edges'][:].shape[0] - 1

    filename = f'{orbit_code}-Ls{solar_longitude * 10:04.0f}-angle{subsolar_subspacecraft_angle * 10:04.0f}-binning{spatial_binning:04}x{spectral_binning:04}-geometry-ql.png'

    plt.savefig(save_location / filename)
    plt.close()


if __name__ == '__main__':
    file_path = Path('/media/kyle/iuvs/data/')
    save_location = Path('/media/kyle/iuvs/cloudspotting/')

    n_cpus = mp.cpu_count()
    pool = mp.Pool(n_cpus - 5)

    for orb in range(10000, 15000):
        #print(orb)
        #make_histogram_equalized_detector_image(orb)
        #make_square_root_scaled_detector_image(orb)
        pool.apply_async(func=make_histogram_equalized_detector_image, args=(orb,))
        #pool.apply_async(func=make_square_root_scaled_detector_image, args=(orb,))
        #pool.apply_async(func=make_geometry_detector_image, args=(orb,))
    pool.close()
    pool.join()
