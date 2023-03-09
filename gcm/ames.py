import numpy as np


class Fixed:
    def __init__(self, dataset):
        self.dataset = dataset

    def _get_latitude(self):
        return self.dataset['lat'][:].data

    def _get_latitude_bounds(self):
        return self.dataset['grid_yt_bnds'][:].data

    def _get_longitude(self):
        return self.dataset['lon'][:].data

    def _get_longitude_bounds(self):
        return self.dataset['grid_xt_bnds'][:].data

    def _get_surface_elevation(self):
        return self.dataset['zsurf'][:].data

    def _get_surface_albedo(self):
        return self.dataset['alb'][:].data

    def _get_pk(self):
        return self.dataset['pk'][:].data

    def _get_bk(self):
        return self.dataset['bk'][:].data

    # To add: thin, emis, gice, phalf

    def get_latitude_centers(self) -> np.ndarray:
        return self._get_latitude()

    def get_latitude_edges(self) -> np.ndarray:
        return np.unique(np.concatenate((self._get_latitude_bounds())))

    def get_longitude_centers(self) -> np.ndarray:
        return self._get_longitude()

    def get_longitude_edges(self) -> np.ndarray:
        return np.unique(np.concatenate((self._get_longitude_bounds())))

    def get_surface_elevation(self) -> np.ndarray:
        return self._get_surface_elevation()

    def get_surface_albedo(self) -> np.ndarray:
        return self._get_surface_albedo()

    def get_ak(self) -> np.ndarray:
        return self._get_pk()  # Evidently ak = pk

    def get_bk(self) -> np.ndarray:
        return self._get_bk()
