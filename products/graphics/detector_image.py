import matplotlib.pyplot as plt
import numpy as np


def make_swath_grid(field_of_view: np.ndarray, n_spatial_bins: int, swath_number: int, angular_size: float) \
        -> tuple[np.ndarray, np.ndarray]:
    """Make a swath grid of mirror angles and spatial bins.

    Parameters
    ----------
    field_of_view
        The instrument's field of view.
    swath_number
        The swath number.
    n_spatial_bins
        The number of spatial bins.
    angular_size
        The angular size of one horizontal element. This is likely the angular detector width or the angular size of the
        observation, but can be any value.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        The swath grid.

    """
    spatial_bin_angular_edges = _make_spatial_bin_angular_edges(angular_size, swath_number, n_spatial_bins)
    field_of_view_edges = _make_field_of_view_edges(field_of_view)
    return np.meshgrid(spatial_bin_angular_edges, field_of_view_edges)


def _make_spatial_bin_angular_edges(angular_size: float, swath_number: int, n_spatial_bins: int) -> np.ndarray:
    """Make the edges of each spatial bin such that they fit into a given angular size

    Parameters
    ----------
    angular_size
    swath_number
    n_spatial_bins

    Returns
    -------

    """
    return np.linspace(angular_size * swath_number, angular_size * (swath_number + 1), num=n_spatial_bins+1)


def _make_field_of_view_edges(field_of_view) -> np.ndarray:
    """Make the edges of the field of view

    Parameters
    ----------
    field_of_view

    Returns
    -------

    Notes
    -----
    The field of view may not necessarily increase at a constant rate so this isn't rigorous. This also assumes all
    pixels are contiguous

    """
    n_integrations = field_of_view.size
    # orbit 4361 requires this check
    if n_integrations == 1:
        return np.linspace(field_of_view[0], field_of_view[0], num=2)
    mean_angle_difference = np.mean(np.diff(field_of_view))
    field_of_view_edges = np.linspace(field_of_view[0] - mean_angle_difference / 2,
                                     field_of_view[-1] + mean_angle_difference / 2,
                                     num=n_integrations + 1)
    return field_of_view_edges


def pcolormesh_detector_image(axis: plt.Axes, image: np.ndarray, horizontal_meshgrid: np.ndarray,
        vertical_meshgrid: np.ndarray, **kwargs) -> None:
    """pcolormesh a single-channel detector image in a given axis. For instance, this could be the local time,
    solar zenith angle, or a linear scaling for one channel of the detector.

    Parameters
    ----------
    axis: plt.Axes
        The axis to place the pcolormeshed image into.
    image: np.ndarray
        The MxNx3 array of rgb values.
    horizontal_meshgrid: np.ndarray
        The horizontal grid of pixel coordinates.
    vertical_meshgrid: np.ndarray
        The vertical grid of pixel coordinates.
    **kwargs
        The matplotlib kwargs.

    Returns
    -------
    None

    See Also
    --------
    pcolormesh_rgb_detector_image: pcolormesh an rgb image

    """

    axis.pcolormesh(
        horizontal_meshgrid, vertical_meshgrid, image,
        linewidth=0,
        edgecolors='none',
        rasterized=True,
        **kwargs)


def pcolormesh_rgb_detector_image(axis: plt.Axes, image: np.ndarray, x: np.ndarray, y: np.ndarray) -> None:
    """pcolormesh an rgb detector image in a given axis.

    Parameters
    ----------
    axis: plt.Axes
        The axis to place the detector image into.
    image: np.ndarray
        An MxNx3 (rgb) or MxNx4 (rgba) array of colors.
    x: np.ndarray
        The horizontal grid of pixel corners.
    y: np.ndarray
        The vertical grid of pixel corners.

    Returns
    -------
    None

    See Also
    --------
    pcolormesh_detector_image: pcolormesh a single-channel detector image.

    """
    axis.pcolormesh(x, y, image, linewidth=0, edgecolors='none', rasterized=True)


def plot_rgb_detector_image_in_axis(axis: plt.Axes, image: np.ndarray, swath_number: np.ndarray,
                                    field_of_view: np.ndarray, angular_size: float, app_flip: bool) -> None:
    """Plot an rgb detector image in a given axis.

    Parameters
    ----------
    axis
    image
    swath_number
    field_of_view
    angular_size
    app_flip

    Returns
    -------

    """
    n_spatial_bins = image.shape[1]
    for swath in np.unique(swath_number):
        swath_indices = swath_number == swath
        fov = field_of_view[swath_indices]
        x, y = make_swath_grid(fov, n_spatial_bins, swath, angular_size)
        rgb_image = image[swath_indices]
        rgb_image = np.fliplr(rgb_image) if app_flip else rgb_image
        pcolormesh_rgb_detector_image(axis, rgb_image, x, y)