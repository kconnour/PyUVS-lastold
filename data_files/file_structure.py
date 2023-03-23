from pathlib import Path

from file_setup import open_latest_file, add_orbit_attribute_to_file


def setup_file(orbit: int) -> None:
    data_file_save_location = Path('/media/kyle/iuvs/data')

    file = open_latest_file(orbit, data_file_save_location)
    add_orbit_attribute_to_file(file, orbit)

    for segment in ['apoapse', 'periapse']:
        file.require_group(f'{segment}')

        match segment:
            case 'apoapse':
                file.require_group(f'{segment}/apsis')
                file.require_group(f'{segment}/integration')
                file.require_group(f'{segment}/spacecraft_geometry')
                file.require_group(f'{segment}/instrument_geometry')
                file.require_group(f'{segment}/spatial_pixel_geometry')

                for channel in ['muv']:
                    file.require_group(f'{segment}/{channel}')

                    match channel:
                        case 'muv':
                            file.require_group(f'{segment}/{channel}/integration')

                            for experiment in ['failsafe', 'dayside', 'nightside']:
                                experiment_path = f'{segment}/{channel}/{experiment}'
                                file.require_group(experiment_path)

                                file.require_group(f'{experiment_path}/binning')
                                file.require_group(f'{experiment_path}/spatial_bin_geometry')
                                file.require_group(f'{experiment_path}/detector')

                                match experiment:
                                    case 'dayside':
                                        file.require_group(f'{experiment_path}/retrievals')
                                    case 'nightside':
                                        file.require_group(f'{experiment_path}/mlr')

            case 'periapse':
                file.require_group(f'{segment}/apsis')
    file.close()
