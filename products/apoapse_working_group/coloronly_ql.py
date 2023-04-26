from pathlib import Path

from h5py import File
import matplotlib.pyplot as plt
import numpy as np

import products.graphics as graphics
import pyuvs as pu


def setup_figure(n_swaths: int, angular_width: float, height: float) -> tuple[plt.Figure, plt.Axes]:
    field_of_view = (pu.constants.maximum_mirror_angle - pu.constants.minimum_mirror_angle) * 2
    width = n_swaths * angular_width / field_of_view * height
    fig = plt.figure(figsize=(width, height))
    ax = fig.add_axes([0, 0, 1, 1])
    return fig, ax


def make_color_only_detector_image(orbit: int, standard=False) -> None:
    print(orbit)
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

    fig, ax = setup_figure(n_swaths, angular_width, 6)

    graphics.plot_rgb_detector_image_in_axis(ax, image, swath_number, field_of_view, angular_width, app_flip)
    graphics.add_terminator_contour_line_to_axis(ax, solar_zenith_angle, swath_number, field_of_view, angular_width, app_flip)

    ax.set_xlim(0, angular_width * n_swaths)
    ax.set_ylim(pu.constants.minimum_mirror_angle * 2, pu.constants.maximum_mirror_angle * 2)

    if standard:
        filename = f'{pu.orbit.make_orbit_code(orbit)}-coloronly-15bins.png'
    else:
        filename = f'{pu.orbit.make_orbit_code(orbit)}-coloronly.png'
    plt.savefig(save_location / filename, dpi=300)
    plt.close(fig)


if __name__ == '__main__':
    file_path = Path('/media/kyle/iuvs/data/')
    save_location = Path('/media/kyle/iuvs/apoapse-working-group/')
    make_color_only_detector_image(3568, standard=True)
