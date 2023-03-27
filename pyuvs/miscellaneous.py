from astropy.io import fits
import numpy as np


def catch_empty_arrays(func: callable):
    def wrapper(hduls: list[fits.hdu.hdulist.HDUList], *args):
        return func(hduls, *args) if hduls else np.array([])
    return wrapper


def add_leading_dimension_if_necessary(data: list[np.ndarray], expected_dims: int) -> list[np.ndarray]:
    return [f if np.ndim(f)==expected_dims else f[None, :] for f in data if f.size>0]


def app_flip(data: list[np.ndarray], flip: bool) -> list[np.ndarray]:
    return [np.fliplr(f) if flip else f for f in data]


def get_integrations_per_file(hduls: list[fits.hdu.hdulist.HDUList]) -> list[int]:
    et = [f['integration'].data['et'] for f in hduls]
    return [f.shape[0] for f in et]
