from ctypes import Structure, c_char_p, c_int, c_short

from . import timespec

GSF_MAX_SENSOR_PARAMETERS = 128
SENSOR_PARAMETERS_PARAM_SIZES = c_short * GSF_MAX_SENSOR_PARAMETERS
SENSOR_PARAMETERS_PARAMS = c_char_p * GSF_MAX_SENSOR_PARAMETERS


class c_gsfSensorParameters(Structure):
    _fields_ = [
        ("param_time", timespec.c_timespec),
        ("number_parameters", c_int),
        ("param_size", SENSOR_PARAMETERS_PARAM_SIZES),
        ("param", SENSOR_PARAMETERS_PARAMS),
    ]
