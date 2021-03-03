from ctypes import POINTER, Structure, c_double, c_int, c_short, c_ubyte, c_ushort

from . import gsfBRBIntensity, gsfScaleFactors, gsfSensorSpecific, timespec


class c_gsfSwathBathyPing(Structure):
    _fields_ = [
        # Seconds and nanoseconds.
        ("ping_time", timespec.c_timespec),
        # Degrees, positive going east.
        ("longitude", c_double),
        # Degrees, positive going north.
        ("latitude", c_double),
        # Height above ellipsoid, positive value defines a point above ellipsoid.
        ("height", c_double),
        # Distance from ellipsoid to vertical datum, positive value indicates datum
        # above ellipsoid.
        ("sep", c_double),
        # In this ping.
        ("number_beams", c_short),
        # Offset into array (0 = portmost outer).
        ("center_beam", c_short),
        # Flags to mark status of this ping.
        ("ping_flags", c_ushort),
        # For future use.
        ("reserved", c_short),
        # Meters.
        ("tide_corrector", c_double),
        # Meters.
        ("gps_tide_corrector", c_double),
        # Meters.
        ("depth_corrector", c_double),
        # Degrees.
        ("heading", c_double),
        # Degrees.
        ("pitch", c_double),
        # Degrees.
        ("roll", c_double),
        # Meters.
        ("heave", c_double),
        # Degrees.
        ("course", c_double),
        # Knots.
        ("speed", c_double),
        # The array scale factors for this data.
        ("scaleFactors", gsfScaleFactors.c_gsfScaleFactors),
        # Depth array (meters).
        ("depth", POINTER(c_double)),
        # Array of depth relative to 1500 m/s.
        ("nominal_depth", POINTER(c_double)),
        # Across track array (meters).
        ("across_track", POINTER(c_double)),
        # Along track array (meters).
        ("along_track", POINTER(c_double)),
        # Roundtrip travel time array (seconds).
        ("travel_time", POINTER(c_double)),
        # Beam angle array (degrees from vertical).
        ("beam_angle", POINTER(c_double)),
        # Mean, calibrated beam amplitude array (dB re 1V/micro pascal at 1 meter).
        ("mc_amplitude", POINTER(c_double)),
        # Mean, relative beam amplitude array (dB re 1V/micro pascal at 1 meter).
        ("mr_amplitude", POINTER(c_double)),
        # Echo width array (seconds).
        ("echo_width", POINTER(c_double)),
        # Quality factor array (dimensionless).
        ("quality_factor", POINTER(c_double)),
        # Array of heave data (meters).
        ("receive_heave", POINTER(c_double)),
        # Array of estimated vertical error (meters).
        ("depth_error", POINTER(c_double)),
        # Array of estimated across track error (meters).
        ("across_track_error", POINTER(c_double)),
        # Array of estimated along track error (meters).
        ("along_track_error", POINTER(c_double)),
        # Two bit beam detection flags provided by Reson sonar.
        ("quality_flags", POINTER(c_ubyte)),
        # Array of beam status flags.
        ("beam_flags", POINTER(c_ubyte)),
        # Signal to noise ratio (dB).
        ("signal_to_noise", POINTER(c_double)),
        # Beam angle forward array (degrees counterclockwise from stbd.).
        ("beam_angle_forward", POINTER(c_double)),
        # Array of estimated vertical error (meters, at 95% confidence).
        ("vertical_error", POINTER(c_double)),
        # Array of estimated horizontal error (meters, at 95% confidence).
        ("horizontal_error", POINTER(c_double)),
        # Array of values that specify the transit sector for this beam.
        ("sector_number", POINTER(c_ushort)),
        # Array of values that specify the method of bottom detection.
        ("detection_info", POINTER(c_ushort)),
        # Array of values that specify incident beam angle adjustment from beam_angle.
        ("incident_beam_adj", POINTER(c_double)),
        # Array of values that specify data cleaning information from the sensor system.
        ("system_cleaning", POINTER(c_ushort)),
        # Array of values used to correct the travel times for Doppler when
        # transmission is FM.
        ("doppler_corr", POINTER(c_double)),
        # Vertical uncertainty provided by the sonar.
        ("sonar_vert_uncert", POINTER(c_double)),
        # Horizontal uncertainty provided by the sonar (Added in v3.09)
        ("sonar_horz_uncert", POINTER(c_double)),
        # Length of the detection window in seconds provided by the sonar (Added in v3.09)
        ("detection_window", POINTER(c_double)),
        # Mean absolute coefficient provided by the sonar (Added in v3.09)
        ("mean_abs_coeff", POINTER(c_double)),
        # A definition which specifies the sensor.
        ("sensor_id", c_int),
        # Union of known sensor specific data.
        ("sensor_data", gsfSensorSpecific.c_gsfSensorSpecific),
        # Structure containing bathymetric receive beam time series intensities.
        ("brb_inten", POINTER(gsfBRBIntensity.c_gsfBRBIntensity)),
    ]
