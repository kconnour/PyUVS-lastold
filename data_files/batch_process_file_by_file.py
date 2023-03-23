from pathlib import Path

import apoapse
from data_files.file_structure import setup_file
from data_files.file_setup import open_latest_file
from data_files.fits_sort import get_apoapse_muv_fits_files


if __name__ == '__main__':
    iuvs_fits_file_location = Path('/media/kyle/iuvs/production')
    spice_kernel_location = Path('/media/kyle/iuvs/spice')
    data_file_save_location = Path('/media/kyle/iuvs/data')

    def batch_process_orbit(orbit: int) -> None:
        setup_file(orbit)
        file = open_latest_file(orbit, data_file_save_location)

        for segment in ['apoapse']:
            match segment:
                case 'apoapse':
                    # Get some data to work with. For FUV/MUV independent data, just choose either channel
                    apoapse_hduls = get_apoapse_muv_fits_files(orbit, iuvs_fits_file_location)

                    # Add apsis datasets
                    # Many...

                    # Add integration datasets
                    apoapse.integration.add_ephemeris_time_to_file(file, apoapse_hduls)
                    apoapse.integration.add_mirror_data_number_to_file(file, apoapse_hduls)
                    apoapse.integration.add_mirror_angle_to_file(file, apoapse_hduls)
                    apoapse.integration.add_field_of_view_to_file(file, apoapse_hduls)
                    apoapse.integration.add_case_temperature_to_file(file, apoapse_hduls)
                    apoapse.integration.add_integration_time_to_file(file, apoapse_hduls)
                    apoapse.integration.add_swath_number_to_file(file)
                    apoapse.integration.add_number_of_swaths_to_file(file)
                    apoapse.integration.add_opportunity_classification_to_file(file)

                    # Add spacecraft geometry datasets
                    # subsolar latitude
                    # subsolar longitude
                    # subspacecraft lat
                    # subspacecraft lon
                    # subspacecraft alt
                    # velocity inertial frame

                    # Add instrument geometry datasets
                    # x fov
                    # instrument sun angle
                    # app flip

                case 'periapse':
                    # Add apsis datasets
                    # Many...
                    pass

    for orb in range(3000, 3002):
        print(orb)
        batch_process_orbit(orb)
