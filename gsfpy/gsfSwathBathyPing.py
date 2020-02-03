from ctypes import *

from . import gsfBRBIntensity
from . import gsfScaleFactors
from . import gsfSensorSpecific
from . import timespec


class c_gsfSwathBathyPing(Structure):
    _fields_ = [('ping_time', timespec.c_timespec),                          # Seconds and nanoseconds. */
                ('longitude', c_double),                                     # Degrees, positive going east. */
                ('latitude', c_double),                                      # Degrees, positive going north. */
                ('height', c_double),                                        # Height above ellipsoid, positive value defines a point above ellipsoid. */
                ('sep', c_double),                                           # Distance from ellipsoid to vertical datum, positive value indicates datum above ellipsoid. */
                ('number_beams', c_short),                                   # In this ping. */
                ('center_beam', c_short),                                    # Offset into array (0 = portmost outer). */
                ('ping_flags', c_ushort),                                    # Flags to mark status of this ping. */
                ('reserved', c_short),                                       # For future use. */
                ('tide_corrector', c_double),                                # Meters. */
                ('gps_tide_corrector', c_double),                            # Meters. */
                ('depth_corrector', c_double),                               # Meters. */
                ('heading', c_double),                                       # Degrees. */
                ('pitch', c_double),                                         # Degrees. */
                ('roll', c_double),                                          # Degrees. */
                ('heave', c_double),                                         # Meters. */
                ('course', c_double),                                        # Degrees. */
                ('speed', c_double),                                         # Knots. */
                ('scaleFactors', gsfScaleFactors.c_gsfScaleFactors),         # The array scale factors for this data. */
                ('depth', POINTER(c_double)),                                # Depth array (meters). */
                ('nominal_depth', POINTER(c_double)),                        # Array of depth relative to 1500 m/s. */
                ('across_track', POINTER(c_double)),                         # Across track array (meters). */
                ('along_track', POINTER(c_double)),                          # Along track array (meters). */
                ('travel_time', POINTER(c_double)),                          # Roundtrip travel time array (seconds). */
                ('beam_angle', POINTER(c_double)),                           # Beam angle array (degrees from vertical). */
                ('mc_amplitude', POINTER(c_double)),                         # Mean, calibrated beam amplitude array (dB re 1V/micro pascal at 1 meter). */
                ('mr_amplitude', POINTER(c_double)),                         # Mean, relative beam amplitude array (dB re 1V/micro pascal at 1 meter). */
                ('echo_width', POINTER(c_double)),                           # Echo width array (seconds). */
                ('quality_factor', POINTER(c_double)),                       # Quality factor array (dimensionless). */
                ('receive_heave', POINTER(c_double)),                        # Array of heave data (meters). */
                ('depth_error', POINTER(c_double)),                          # Array of estimated vertical error (meters). */
                ('across_track_error', POINTER(c_double)),                   # Array of estimated across track error (meters). */
                ('along_track_error', POINTER(c_double)),                    # Array of estimated along track error (meters). */
                ('quality_flags', POINTER(c_ubyte)),                         # Two bit beam detection flags provided by Reson sonar. */
                ('beam_flags', POINTER(c_ubyte)),                            # Array of beam status flags. */
                ('signal_to_noise', POINTER(c_double)),                      # Signal to noise ratio (dB). */
                ('beam_angle_forward', POINTER(c_double)),                   # Beam angle forward array (degrees counterclockwise from stbd.). */
                ('vertical_error', POINTER(c_double)),                       # Array of estimated vertical error (meters, at 95% confidence). */
                ('horizontal_error', POINTER(c_double)),                     # Array of estimated horizontal error (meters, at 95% confidence). */
                ('sector_number', POINTER(c_ushort)),                        # Array of values that specify the transit sector for this beam. */
                ('detection_info', POINTER(c_ushort)),                       # Array of values that specify the method of bottom detection. */
                ('incident_beam_adj', POINTER(c_double)),                    # Array of values that specify incident beam angle adjustment from beam_angle. */
                ('system_cleaning', POINTER(c_ushort)),                      # Array of values that specify data cleaning information from the sensor system. */
                ('doppler_corr', POINTER(c_double)),                         # Array of values used to correct the travel times for Doppler when transmission is FM. */
                ('sonar_vert_uncert', POINTER(c_double)),                    # Vertical uncertainty provided by the sonar. */
                ('sensor_id', c_int),                                        # A definition which specifies the sensor. */
                ('sensor_data', gsfSensorSpecific.c_gsfSensorSpecific),      # Union of known sensor specific data. */
                ('brb_inten', POINTER(gsfBRBIntensity.c_gsfBRBIntensity))]   # Structure containing bathymetric receive beam time series intensities. */