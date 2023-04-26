import numpy as np


def load_muv_flatfield():
    return np.load('/media/kyle/iuvs/instrument/instrument/muv_flatfield_v1.npy')


def load_voltage():
    return np.load('/media/kyle/iuvs/instrument/instrument/voltage.npy')


def load_voltage_coefficients():
    return np.load('/media/kyle/iuvs/instrument/instrument/voltage_fit_coefficients.npy')


def load_muv_sensitivity_curve():
    return np.load('/media/kyle/iuvs/instrument/instrument/muv_sensitivity_curve_observational.npy')


def load_point_spread_function():
    return np.load('/mnt/iuvs/instrument/instrument/muv_point_spread_function.npy')
