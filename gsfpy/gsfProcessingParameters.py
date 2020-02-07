from ctypes import Structure, c_char_p, c_int, c_short

from . import timespec

GSF_MAX_PROCESSING_PARAMETERS = 128
PROCESSING_PARAMETERS_PARAM_SIZES = c_short * GSF_MAX_PROCESSING_PARAMETERS
PROCESSING_PARAMETERS_PARAMS = c_char_p * GSF_MAX_PROCESSING_PARAMETERS


class c_gsfProcessingParameters(Structure):
    _fields_ = [
        ("param_time", timespec.c_timespec),
        ("number_parameters", c_int),
        ("param_size", PROCESSING_PARAMETERS_PARAM_SIZES),
        ("param", PROCESSING_PARAMETERS_PARAMS),
    ]
