from ctypes import Structure, c_double

MAX_OFFSETS = 2
GSF_MAX_OFFSETS_ARRAY = c_double * MAX_OFFSETS


class c_gsfMBOffsets(Structure):
    _fields_ = [
        ("draft", GSF_MAX_OFFSETS_ARRAY),
        ("pitch_bias", GSF_MAX_OFFSETS_ARRAY),
        ("roll_bias", GSF_MAX_OFFSETS_ARRAY),
        ("gyro_bias", GSF_MAX_OFFSETS_ARRAY),
        ("position_x_offset", c_double),
        ("position_y_offset", c_double),
        ("position_z_offset", c_double),
        ("antenna_x_offset", c_double),
        ("antenna_y_offset", c_double),
        ("antenna_z_offset", c_double),
        ("transducer_x_offset", GSF_MAX_OFFSETS_ARRAY),
        ("transducer_y_offset", GSF_MAX_OFFSETS_ARRAY),
        ("transducer_z_offset", GSF_MAX_OFFSETS_ARRAY),
        ("transducer_pitch_offset", GSF_MAX_OFFSETS_ARRAY),
        ("transducer_roll_offset", GSF_MAX_OFFSETS_ARRAY),
        ("transducer_heading_offset", GSF_MAX_OFFSETS_ARRAY),
        ("mru_pitch_bias", c_double),
        ("mru_roll_bias", c_double),
        ("mru_heading_bias", c_double),
        ("mru_x_offset", c_double),
        ("mru_y_offset", c_double),
        ("mru_z_offset", c_double),
        ("center_of_rotation_x_offset", c_double),
        ("center_of_rotation_y_offset", c_double),
        ("center_of_rotation_z_offset", c_double),
        ("position_latency", c_double),
        ("attitude_latency", c_double),
        ("depth_sensor_latency", c_double),
        ("depth_sensor_x_offset", c_double),
        ("depth_sensor_y_offset", c_double),
        ("depth_sensor_z_offset", c_double),
        ("rx_transducer_x_offset", GSF_MAX_OFFSETS_ARRAY),
        ("rx_transducer_y_offset", GSF_MAX_OFFSETS_ARRAY),
        ("rx_transducer_z_offset", GSF_MAX_OFFSETS_ARRAY),
        ("rx_transducer_pitch_offset", GSF_MAX_OFFSETS_ARRAY),
        ("rx_transducer_roll_offset", GSF_MAX_OFFSETS_ARRAY),
        ("rx_transducer_heading_offset", GSF_MAX_OFFSETS_ARRAY),
    ]
