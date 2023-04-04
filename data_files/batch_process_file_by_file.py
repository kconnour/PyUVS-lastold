from pathlib import Path

import apoapse
import periapse
from data_files.file_structure import setup_file
from data_files.file_setup import open_latest_file
from data_files.fits_sort import get_apoapse_muv_fits_files, get_apoapse_muv_failsafe_files, \
    get_apoapse_muv_dayside_files, get_apoapse_muv_nightside_files


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
                    apoapse.apsis.add_ephemeris_time_to_file(file)
                    apoapse.apsis.add_mars_year_to_file(file)
                    apoapse.apsis.add_sol_to_file(file)
                    apoapse.apsis.add_solar_longitude_to_file(file)
                    apoapse.apsis.add_subsolar_latitude_to_file(file)
                    apoapse.apsis.add_subsolar_longitude_to_file(file)
                    apoapse.apsis.add_subspacecraft_latitude_to_file(file)
                    apoapse.apsis.add_subspacecraft_longitude_to_file(file)
                    apoapse.apsis.add_subspacecraft_altitude_to_file(file)
                    apoapse.apsis.add_subspacecraft_local_time_to_file(file)
                    apoapse.apsis.add_mars_sun_distance_to_file(file)
                    apoapse.apsis.add_subsolar_subspacecraft_angle_to_file(file)

                    # Add integration datasets
                    apoapse.integration.add_ephemeris_time_to_file(file, apoapse_hduls)
                    apoapse.integration.add_mirror_data_number_to_file(file, apoapse_hduls)
                    apoapse.integration.add_mirror_angle_to_file(file, apoapse_hduls)
                    apoapse.integration.add_field_of_view_to_file(file, apoapse_hduls)
                    apoapse.integration.add_case_temperature_to_file(file, apoapse_hduls)
                    apoapse.integration.add_integration_time_to_file(file, apoapse_hduls)
                    apoapse.integration.add_swath_number_to_file(file, apoapse_hduls)
                    apoapse.integration.add_number_of_swaths_to_file(file, apoapse_hduls)
                    apoapse.integration.add_opportunity_classification_to_file(file, apoapse_hduls)

                    # Add spacecraft geometry datasets
                    apoapse.spacecraft_geometry.add_subsolar_latitude_to_file(file, apoapse_hduls)
                    apoapse.spacecraft_geometry.add_subsolar_longitude_to_file(file, apoapse_hduls)
                    apoapse.spacecraft_geometry.add_subspacecraft_latitude_to_file(file, apoapse_hduls)
                    apoapse.spacecraft_geometry.add_subspacecraft_longitude_to_file(file, apoapse_hduls)
                    apoapse.spacecraft_geometry.add_subspacecraft_altitude_to_file(file, apoapse_hduls)
                    apoapse.spacecraft_geometry.add_spacecraft_velocity_inertial_frame_to_file(file, apoapse_hduls)

                    # Add instrument geometry datasets
                    apoapse.instrument_geometry.add_instrument_x_field_of_view_to_file(file, apoapse_hduls)
                    apoapse.instrument_geometry.add_instrument_sun_angle_to_file(file, apoapse_hduls)
                    apoapse.instrument_geometry.add_app_flip_to_file(file, apoapse_hduls)

                    for channel in ['muv']:
                        match channel:
                            case 'muv':
                                muv_hduls = get_apoapse_muv_fits_files(orbit, iuvs_fits_file_location)

                                # Add MUV integration datasets
                                apoapse.muv.integration.add_detector_temperature_to_file(file, muv_hduls)
                                apoapse.muv.integration.add_mcp_voltage_to_file(file, muv_hduls)
                                apoapse.muv.integration.add_mcp_voltage_gain_to_file(file, muv_hduls)
                                apoapse.muv.integration.add_failsafe_integrations_to_file(file, muv_hduls)
                                apoapse.muv.integration.add_dayside_integrations_to_file(file, muv_hduls)
                                apoapse.muv.integration.add_nightside_integrations_to_file(file, muv_hduls)

                                for experiment in ['failsafe', 'dayside', 'nightside']:
                                    match experiment:
                                        case 'failsafe':
                                            failsafe_hduls = get_apoapse_muv_failsafe_files(orbit, iuvs_fits_file_location)

                                            # Add binning datasets
                                            apoapse.muv.failsafe.binning.add_spatial_bin_edges_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.binning.add_spectral_bin_edges_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.binning.add_spatial_bin_width_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.binning.add_spectral_bin_width_to_file(file, failsafe_hduls)

                                            # Add spatial bin geometry datasets
                                            apoapse.muv.failsafe.spatial_bin_geometry.add_latitude_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.spatial_bin_geometry.add_longitude_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.spatial_bin_geometry.add_tangent_altitude_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.spatial_bin_geometry.add_tangent_altitude_rate_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.spatial_bin_geometry.add_line_of_sight_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.spatial_bin_geometry.add_solar_zenith_angle_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.spatial_bin_geometry.add_emission_angle_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.spatial_bin_geometry.add_phase_angle_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.spatial_bin_geometry.add_zenith_angle_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.spatial_bin_geometry.add_local_time_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.spatial_bin_geometry.add_right_ascension_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.spatial_bin_geometry.add_declination_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.spatial_bin_geometry.add_bin_vector_to_file(file, failsafe_hduls)

                                            # Add detector datasets
                                            apoapse.muv.failsafe.detector.add_raw_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.detector.add_dark_subtracted_to_file(file, failsafe_hduls)
                                            apoapse.muv.failsafe.detector.add_brightness_to_file(file)

                                        case 'dayside':
                                            dayside_hduls = get_apoapse_muv_dayside_files(orbit, iuvs_fits_file_location)

                                            # Add binning datasets
                                            apoapse.muv.dayside.binning.add_spatial_bin_edges_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.binning.add_spectral_bin_edges_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.binning.add_spatial_bin_width_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.binning.add_spectral_bin_width_to_file(file, dayside_hduls)

                                            # Add spatial bin geometry datasets
                                            apoapse.muv.dayside.spatial_bin_geometry.add_latitude_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.spatial_bin_geometry.add_longitude_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.spatial_bin_geometry.add_tangent_altitude_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.spatial_bin_geometry.add_tangent_altitude_rate_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.spatial_bin_geometry.add_line_of_sight_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.spatial_bin_geometry.add_solar_zenith_angle_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.spatial_bin_geometry.add_emission_angle_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.spatial_bin_geometry.add_phase_angle_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.spatial_bin_geometry.add_zenith_angle_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.spatial_bin_geometry.add_local_time_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.spatial_bin_geometry.add_right_ascension_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.spatial_bin_geometry.add_declination_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.spatial_bin_geometry.add_bin_vector_to_file(file, dayside_hduls)

                                            # Add detector datasets
                                            apoapse.muv.dayside.detector.add_raw_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.detector.add_dark_subtracted_to_file(file, dayside_hduls)
                                            apoapse.muv.dayside.detector.add_brightness_to_file(file)

                                        case 'nightside':
                                            nightside_hduls = get_apoapse_muv_nightside_files(orbit, iuvs_fits_file_location)

                                            # Add binning datasets
                                            apoapse.muv.nightside.binning.add_spatial_bin_edges_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.binning.add_spectral_bin_edges_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.binning.add_spatial_bin_width_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.binning.add_spectral_bin_width_to_file(file, nightside_hduls)

                                            # Add spatial bin geometry datasets
                                            apoapse.muv.nightside.spatial_bin_geometry.add_latitude_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.spatial_bin_geometry.add_longitude_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.spatial_bin_geometry.add_tangent_altitude_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.spatial_bin_geometry.add_tangent_altitude_rate_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.spatial_bin_geometry.add_line_of_sight_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.spatial_bin_geometry.add_solar_zenith_angle_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.spatial_bin_geometry.add_emission_angle_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.spatial_bin_geometry.add_phase_angle_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.spatial_bin_geometry.add_zenith_angle_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.spatial_bin_geometry.add_local_time_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.spatial_bin_geometry.add_right_ascension_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.spatial_bin_geometry.add_declination_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.spatial_bin_geometry.add_bin_vector_to_file(file, nightside_hduls)

                                            # Add detector datasets
                                            apoapse.muv.nightside.detector.add_raw_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.detector.add_dark_subtracted_to_file(file, nightside_hduls)
                                            apoapse.muv.nightside.detector.add_brightness_to_file(file)

                    # Add pixel geometry datasets
                    #apoapse.pixel_geometry.add_latitude_and_longitude_to_file(file)  # these are only done from orbit 3000--3045

                case 'periapse':

                    # Add apsis datasets
                    periapse.apsis.add_ephemeris_time_to_file(file)
                    periapse.apsis.add_mars_year_to_file(file)
                    periapse.apsis.add_sol_to_file(file)
                    periapse.apsis.add_solar_longitude_to_file(file)
                    periapse.apsis.add_subsolar_latitude_to_file(file)
                    periapse.apsis.add_subsolar_longitude_to_file(file)
                    periapse.apsis.add_subspacecraft_latitude_to_file(file)
                    periapse.apsis.add_subspacecraft_longitude_to_file(file)
                    periapse.apsis.add_subspacecraft_altitude_to_file(file)
                    periapse.apsis.add_subspacecraft_local_time_to_file(file)
                    periapse.apsis.add_mars_sun_distance_to_file(file)
                    periapse.apsis.add_subsolar_subspacecraft_angle_to_file(file)

    for orb in range(8679, 17599):
        print(orb)
        batch_process_orbit(orb)
