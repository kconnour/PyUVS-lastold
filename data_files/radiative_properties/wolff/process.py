from pathlib import Path

from astropy.io import fits
from h5py import File

from radprop import RadpropFile


def process_file(source_filename: str, aerosol: str, version: int) -> None:
    # Open the source .fits file
    source_filepath = Path('/media') / 'kyle' / 'iuvs' / 'raw' / 'radiative_properties' / 'wolff' / source_filename
    try:
        source_data_file = fits.open(source_filepath)
    except FileNotFoundError as fnfe:
        raise FileNotFoundError('The source data file does not exist.') from fnfe
    except OSError as ose:
        raise FileExistsError('The source filename exists but is not a valid .fits file.') from ose

    # Open an empty .hdf5 file
    destination_filepath = Path('/media') / 'kyle' / 'iuvs' / 'processed' / 'radiative_properties' / 'wolff' / \
                           f'{aerosol}_v{version:02}.hdf5'
    try:
        file = File(destination_filepath, mode='x')
    except FileExistsError:
        print('The file already exists!')
        return
    except FileNotFoundError:
        destination_filepath.parent.mkdir(parents=True, exist_ok=True)
        file = File(destination_filepath, mode='x')

    # Fill the file with data
    radprop = RadpropFile(source_data_file)

    ds = file.create_dataset('particle_sizes', data=radprop.get_particle_sizes())
    ds.attrs['unit'] = 'Microns'

    ds = file.create_dataset('wavelengths', data=radprop.get_wavelengths())
    ds.attrs['unit'] = 'Microns'

    ds = file.create_dataset('scattering_angles', data=radprop.get_scattering_angles())
    ds.attrs['unit'] = 'Degrees'

    ds = file.create_dataset('scattering_cross_section', data=radprop.get_scattering_cross_section())
    ds.attrs['unit'] = 'Microns^2'

    ds = file.create_dataset('extinction_cross_section', data=radprop.get_extinction_cross_section())
    ds.attrs['unit'] = 'Microns^2'

    ds = file.create_dataset('asymmetry_parameter', data=radprop.get_asymmetry_parameter())
    ds.attrs['unit'] = 'Unitless'

    ds = file.create_dataset('phase_function', data=radprop.get_phase_function())
    ds.attrs['unit'] = 'Unitless'

    ds = file.create_dataset('phase_function_reexpansion', data=radprop.get_phase_function_reexpansion())
    ds.attrs['unit'] = 'Unitless'
    ds.attrs['comment'] = 'The phase function recreated from the Legendre coefficients.'

    ds = file.create_dataset('legendre_coefficients', data=radprop.get_legendre_coefficients())
    ds.attrs['unit'] = 'Unitless'
    ds.attrs['comment'] = 'The Legendre coefficients created from decomposing the phase function.'

    file.attrs['creation_date'] = radprop.get_file_creation_date()
    file.attrs['history'] = radprop.get_history()

    file.close()


if __name__ == '__main__':
    process_file('dust1-mars045i_all_area_s0780.fits.gz', 'dust', 1)
    #process_file('ice1-droxtal_050_tmat1_reff_v010.fits', 'ice', 1)
