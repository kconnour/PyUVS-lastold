from pathlib import Path

from astropy.io import fits
from h5py import File

from radprop import RadpropFile


def process_file(source_filename: str, aerosol: str, version: int) -> None:
    source_data = open_source_radprop(source_filename)
    try:
        file = make_empty_hdf5_file(aerosol, version)
    except FileExistsError:
        print('The file already exists!')
        return

    try:
        add_data_to_file(source_data, file)
        file.close()
    except ValueError:
        print('There was a value error when creating the file')
        Path(file.filename).unlink()


def open_source_radprop(filename: str) -> fits.hdu.hdulist.HDUList:
    path = Path('/media') / 'kyle' / 'iuvs' / 'raw' / 'radiative_properties' / 'wolff' / filename
    return fits.open(path)


def make_empty_hdf5_file(aerosol: str, version: int) -> File:
    filename = f'{aerosol}_v{version:02}.hdf5'
    path = Path('/media') / 'kyle' / 'iuvs' / 'processed' / 'radiative_properties' / 'wolff' / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return File(path, mode='x')   # 'x' means to create the file but fail if it already exists


def add_data_to_file(source_file: fits.hdu.hdulist.HDUList, file: File) -> None:
    radprop = RadpropFile(source_file)

    ds = file.create_dataset('particle_sizes', data=radprop.get_particle_sizes())
    ds.attrs['unit'] = 'Microns'

    ds = file.create_dataset('wavelengths', data=radprop.get_wavelengths())
    ds.attrs['unit'] = 'Microns'

    ds = file.create_dataset('scattering_angle', data=radprop.get_scattering_angle())
    ds.attrs['unit'] = 'Degrees'

    ds = file.create_dataset('scattering_cross_section', data=radprop.get_scattering_cross_section())
    ds.attrs['unit'] = 'Microns^2'

    ds = file.create_dataset('extinction_cross_section', data=radprop.get_extinction_cross_section())
    ds.attrs['unit'] = 'Microns^2'

    ds = file.create_dataset('asymmetry_parameter', data=radprop.get_asymmetry_parameter())
    ds.attrs['unit'] = 'Unitless'

    # This should work when Mike creates the phase function again
    #ds = file.create_dataset('phase_function', data=radprop.get_phase_function())
    #ds.attrs['unit'] = 'Unitless'

    ds = file.create_dataset('reexpanded_phase_function', data=radprop.get_reexpanded_phase_function())
    ds.attrs['unit'] = 'Unitless'
    ds.attrs['comment'] = 'The phase function recreated from the Legendre coefficients.'

    ds = file.create_dataset('legendre_coefficients', data=radprop.get_legendre_coefficients())
    ds.attrs['unit'] = 'Unitless'
    ds.attrs['comment'] = 'The Legendre coefficients created from decomposing the phase function.'

    file.attrs['creation_date'] = radprop.get_file_creation_date()
    file.attrs['history'] = radprop.get_history()


if __name__ == '__main__':
    process_file('dust1-dust_all.fits.gz', 'dust', 1)
    process_file('ice1-droxtal_050_tmat1_reff_v010.fits', 'ice', 1)
