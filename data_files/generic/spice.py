from datetime import datetime
from pathlib import Path

import numpy as np
import spiceypy


target = 'Mars'
observer = 'MAVEN'
abcorr = 'LT+S'
body = 499  # Mars IAU code
frame = 'IAU_Mars'


def furnish_ck_files():
    location = Path('/media/kyle/iuvs/spice_pds/ck/')
    app_kernels = sorted(location.glob('mvn_app_rel*.bc'))
    for kernel in app_kernels:
        spiceypy.furnsh(str(kernel))
    sc_kernels = sorted(location.glob('mvn_sc_rel*.bc'))
    for kernel in sc_kernels:
        spiceypy.furnsh(str(kernel))


def furnish_lsk_files():
    location = Path('/media/kyle/iuvs/spice_pds/lsk/')
    kernels = sorted(location.glob('naif*.tls'))
    for kernel in kernels:
        spiceypy.furnsh(str(kernel))


def furnish_mars():
    spiceypy.furnsh('/media/kyle/iuvs/spice_pds/mar097.bsp')


def furnish_pck_files():
    location = Path('/media/kyle/iuvs/spice_pds/pck/')
    kernels = sorted(location.glob('pck*.tpc'))
    for kernel in kernels:
        spiceypy.furnsh(str(kernel))


def furnish_sclk_files():
    location = Path('/media/kyle/iuvs/spice_pds/sclk/')
    kernels = sorted(location.glob('mvn_sclkscet_*.tsc'))
    for kernel in kernels:
        spiceypy.furnsh(str(kernel))


def furnish_spk_files():
    location = Path('/media/kyle/iuvs/spice_pds/spk/')
    kernels = sorted(location.glob('maven_orb_rec*.bsp'))
    for kernel in kernels:
        spiceypy.furnsh(str(kernel))


def furnish_standard_kernels():
    spiceypy.kclear()

    furnish_ck_files()
    furnish_lsk_files()
    furnish_pck_files()
    furnish_sclk_files()
    furnish_spk_files()

    furnish_mars()


def compute_maven_apsis_et(
        segment='apoapse',
        start_time: datetime = datetime(2014, 9, 22, 3, 0),
        end_time: datetime = datetime.utcnow(),
        step_size: float = 60):
    """Compute the ephemeris time at MAVEN's apses.

    Parameters
    ----------
    segment : str
        The orbit point at which to calculate the ephemeris time. Must be either
        "apoapse" or "periapse".
    start_time: datetime
        The earliest datetime to include in the search. I use this date because SPICE doesn't think MAVEN arrived
        when JPL/Wikipedia says they did.
    end_time: datetime
        The latest datetime to include in the search.
    step_size: float
        The step size [seconds] to use for the search.

    Returns
    -------
    orbit_numbers : np.ndarray
        Array of MAVEN orbit numbers. If ``start_time`` is not the date of
        orbital insertion, these numbers are the orbit numbers relative to the
        starting time!
    et_array : np.ndarray
        Array of ephemeris times for chosen orbit segment.
    Notes
    -----
    You must have already furnished the kernels between the starting and ending
    datetimes.
    """
    et_start = spiceypy.datetime2et(start_time)
    et_end = spiceypy.datetime2et(end_time)

    abcorr = 'NONE'
    match segment:
        case 'apoapse':
            relate = 'LOCMAX'
            refval = 3396 + 6200
        case 'periapse':
            relate = 'LOCMIN'
            refval = 3396 + 500
        case _:
            print('The segment must either be "apoapse" or "periapse".')
            return
    adjust = 0
    et = [et_start, et_end]
    cnfine = spiceypy.utils.support_types.SPICEDOUBLE_CELL(2)
    spiceypy.wninsd(et[0], et[1], cnfine)
    ninterval = round((et[1] - et[0]) / step_size)
    result = spiceypy.utils.support_types.SPICEDOUBLE_CELL(
        round(1.1 * (et[1] - et[0]) / 4.5))
    spiceypy.gfdist(target, abcorr, observer, relate, refval, adjust, step_size,
                 ninterval, cnfine, result=result)
    count = spiceypy.wncard(result)
    et_array = np.zeros(count)
    if count == 0:
        print('Result window is empty.')
    else:
        for i in range(count):
            lr = spiceypy.wnfetd(result, i)
            left = lr[0]
            right = lr[1]
            if left == right:
                et_array[i] = left

    # make array of orbit numbers
    orbit_numbers = np.arange(1, len(et_array) + 1, 1, dtype=int)

    return orbit_numbers, et_array


def compute_solar_longitude(et: float) -> float:
    """Compute the solar longitude for a given ephemeris time.
    Parameters
    ----------
    et: float
        The ephemeris time.
    """
    return np.degrees(spiceypy.lspcn(target, et, abcorr))


def compute_subsolar_point(et: float) -> tuple[float, float]:
    """Compute the subsolar point for a given ephemeris time.
    Parameters
    ----------
    et: float
        The ephemeris time.
    Returns
    -------
    tuple[float, float]
        The [latitude, longitude] of the subsolar point.
    """
    spoint, _, _ = spiceypy.subslr(
        'Intercept: ellipsoid', target, et, 'IAU_MARS', abcorr, observer)
    rpoint, colatpoint, lonpoint = spiceypy.recsph(spoint)
    subsolar_lat = 90 - np.degrees(colatpoint)
    subsolar_lon = np.degrees(lonpoint)
    subsolar_lon = subsolar_lon % 360
    return subsolar_lat, subsolar_lon


def compute_subspacecraft_point(et: float) -> tuple[float, float]:
    """Compute the subspacecraft point for a given ephemeris time.
    Parameters
    ----------
    et: float
        The ephemeris time.
    Returns
    -------
    tuple[float, float]
        The [latitude, longitude] of the subspacecraft point.
    """
    spoint, _, _ = spiceypy.subpnt(
        'Intercept: ellipsoid', target, et, 'IAU_MARS', abcorr, observer)
    rpoint, colatpoint, lonpoint = spiceypy.recsph(spoint)
    subsc_lat = 90 - np.degrees(colatpoint)
    subsc_lon = np.degrees(lonpoint)
    subsc_lon = subsc_lon % 360
    return subsc_lat, subsc_lon


def _compute_distance(et: float, observer: str) -> float:
    _, _, srfvec = spiceypy.subpnt(
        'Intercept: ellipsoid', target, et, 'IAU_MARS', abcorr, observer)
    return np.sqrt(np.sum(srfvec ** 2))


def compute_subspacecraft_altitude(et: float) -> float:
    """Compute the subspacecraft altitude [km] for a given ephemeris time.

    Parameters
    ----------
    et: float
        The ephemeris time.
    """
    return _compute_distance(et, observer)


def compute_mars_sun_distance(et: float) -> float:
    """Compute the Mars-sun distance [km] for a given ephemeris time.
    Parameters
    ----------
    et: float
        The ephemeris time.
    """
    return _compute_distance(et, 'SUN')


def compute_subspacecraft_local_time(et: float, lonpoint: float) -> float:
    """ Compute the subspacecraft local time

    Parameters
    ----------
    et
        The ephemeris time.
    lonpoint
        The longitude to ge tthe local time of.

    """
    hr, mn, sc, _, _ = spiceypy.et2lst(et, body, lonpoint, 'planetocentric', timlen=256, ampmlen=256)
    return hr + mn / 60 + sc / 3600


def compute_lat_lon_point(et: float, bin_vector: np.ndarray) -> tuple[float, float]:
    """Compute the subspacecraft point for a given ephemeris time.
    Parameters
    ----------
    et: float
        The ephemeris time.
    bin_vector
        A 1D vector with 3 elements

    Returns
    -------
    tuple[float, float]
        The [latitude, longitude] of the subspacecraft point.
    """
    try:
        spoint, _, _ = spiceypy.sincpt('Ellipsoid', target, et, frame, abcorr, observer, frame, bin_vector)
        rpoint, colatpoint, lonpoint = spiceypy.recsph(spoint)
        lat = 90 - np.degrees(colatpoint)
        lon = np.degrees(lonpoint)
        lon = lon % 360
        return lat, lon
    except spiceypy.utils.exceptions.NotFoundError:
        return np.nan, np.nan
