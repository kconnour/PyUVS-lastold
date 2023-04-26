from pathlib import Path

from h5py import File
import matplotlib.pyplot as plt
import numpy as np

import products.graphics as graphics
import pyuvs as pu


def make_histogram_equalized_grid_detector_image(data_block: int, standard=False) -> None:
    fig, axes = plt.subplots(10, 10, figsize=(25, 15))

    def fill_subplot_with_image(orbit: int):
        print(orbit)
        orbit_block = pu.orbit.make_orbit_block(orbit)
        orbit_code = pu.orbit.make_orbit_code(orbit)
        floor = pu.orbit.make_orbit_floor(orbit)

        ax = axes[int(orbit//10 - floor/10), orbit % 10]
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor('k')
        ax.set_title(f'{orbit}', pad=0)

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

        if standard:
            if brightness.shape[2] not in [15, 19, 20]:
                return
            if brightness.shape[2] in [19, 20]:
                brightness = brightness[..., 1:16]

        solar_zenith_angle[tangent_altitude != 0] = np.nan

        mask = np.logical_and(tangent_altitude == 0, solar_zenith_angle <= 102)
        try:
            image = graphics.histogram_equalize_detector_image(brightness, mask=mask) / 255
        except IndexError:
            return

        angular_width = (spatial_bin_edges[-1] - spatial_bin_edges[0]) / 1024 * pu.constants.angular_detector_width
        graphics.plot_rgb_detector_image_in_axis(ax, image, swath_number, field_of_view, angular_width, app_flip)

        ax.set_xlim(0, angular_width * n_swaths)
        ax.set_ylim(pu.constants.minimum_mirror_angle * 2, pu.constants.maximum_mirror_angle * 2)

    for orb in range(data_block, data_block + 100):
        fill_subplot_with_image(orb)

    if standard:
        filename = f'{pu.orbit.make_orbit_block(data_block)}-standard-heq-15bins.png'
    else:
        filename = f'{pu.orbit.make_orbit_block(data_block)}-standard-heq-allbins.png'
    plt.savefig(save_location / filename, dpi=300)
    plt.close(fig)


def make_color_only_grid_detector_image(data_block: int, standard=False) -> None:
    fig, axes = plt.subplots(10, 10, figsize=(25, 15))

    def fill_subplot_with_image(orbit: int):
        print(orbit)
        orbit_block = pu.orbit.make_orbit_block(orbit)
        orbit_code = pu.orbit.make_orbit_code(orbit)
        floor = pu.orbit.make_orbit_floor(orbit)

        ax = axes[int(orbit//10 - floor/10), orbit % 10]
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor('k')
        ax.set_title(f'{orbit}', pad=0)

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

        if standard:
            if brightness.shape[2] not in [15, 19, 20]:
                return
            if brightness.shape[2] in [19, 20]:
                brightness = brightness[..., 1:16]

        solar_zenith_angle[tangent_altitude != 0] = np.nan

        mask = np.logical_and(tangent_altitude == 0, solar_zenith_angle <= 102)
        try:
            image = graphics.histogram_equalize_detector_image_variations(brightness, mask=mask) / 255
        except IndexError:
            return

        angular_width = (spatial_bin_edges[-1] - spatial_bin_edges[0]) / 1024 * pu.constants.angular_detector_width

        graphics.plot_rgb_detector_image_in_axis(ax, image, swath_number, field_of_view, angular_width, app_flip)

        ax.set_xlim(0, angular_width * n_swaths)
        ax.set_ylim(pu.constants.minimum_mirror_angle * 2, pu.constants.maximum_mirror_angle * 2)

    for orb in range(data_block, data_block + 100):
        fill_subplot_with_image(orb)

    if standard:
        filename = f'{pu.orbit.make_orbit_block(data_block)}-coloronly-heq-15bins.png'
    else:
        filename = f'{pu.orbit.make_orbit_block(data_block)}-coloronly-heq-allbins.png'
    plt.savefig(save_location / filename, dpi=300)
    plt.close(fig)


def make_color_only_linear_grid_detector_image(data_block: int, standard=False) -> None:
    fig, axes = plt.subplots(10, 10, figsize=(25, 15))

    def fill_subplot_with_image(orbit: int):
        print(orbit)
        orbit_block = pu.orbit.make_orbit_block(orbit)
        orbit_code = pu.orbit.make_orbit_code(orbit)
        floor = pu.orbit.make_orbit_floor(orbit)

        ax = axes[int(orbit//10 - floor/10), orbit % 10]
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor('k')
        ax.set_title(f'{orbit}', pad=0)

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

        if standard:
            if brightness.shape[2] not in [15, 19, 20]:
                return
            if brightness.shape[2] in [19, 20]:
                brightness = brightness[..., 1:16]

        solar_zenith_angle[tangent_altitude != 0] = np.nan

        mask = np.logical_and(tangent_altitude == 0, solar_zenith_angle <= 102)
        try:
            image = graphics.linear_scale_detector_image_variations(brightness, mask=mask) / 255
        except IndexError:
            return

        angular_width = (spatial_bin_edges[-1] - spatial_bin_edges[0]) / 1024 * pu.constants.angular_detector_width

        graphics.plot_rgb_detector_image_in_axis(ax, image, swath_number, field_of_view, angular_width, app_flip)

        ax.set_xlim(0, angular_width * n_swaths)
        ax.set_ylim(pu.constants.minimum_mirror_angle * 2, pu.constants.maximum_mirror_angle * 2)

    for orb in range(data_block, data_block + 100):
        fill_subplot_with_image(orb)

    if standard:
        filename = f'{pu.orbit.make_orbit_block(data_block)}-coloronly-linear-15bins.png'
    else:
        filename = f'{pu.orbit.make_orbit_block(data_block)}-coloronly-linear-allbins.png'
    plt.savefig(save_location / filename, dpi=300)
    plt.close(fig)


if __name__ == '__main__':
    file_path = Path('/media/kyle/iuvs/data/')
    save_location = Path('/media/kyle/iuvs/apoapse-working-group/')

    for block in range(3000, 17000, 100):
        make_histogram_equalized_grid_detector_image(block, standard=False)
        make_histogram_equalized_grid_detector_image(block, standard=True)
        make_color_only_grid_detector_image(block, standard=False)
        make_color_only_grid_detector_image(block, standard=True)
        make_color_only_linear_grid_detector_image(block, standard=True)
