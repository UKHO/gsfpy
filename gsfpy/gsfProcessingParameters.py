from ctypes import POINTER, Structure, c_char, c_int, c_short

from . import timespec

GSF_MAX_PROCESSING_PARAMETERS = 128
PROCESSING_PARAMETERS_PARAM_SIZES = c_short * GSF_MAX_PROCESSING_PARAMETERS
PROCESSING_PARAMETERS_PARAMS = POINTER(c_char) * GSF_MAX_PROCESSING_PARAMETERS


class c_gsfProcessingParameters(Structure):
    _fields_ = [
        ("param_time", timespec.c_timespec),
        ("number_parameters", c_int),
        # array of sizes of param text
        ("param_size", PROCESSING_PARAMETERS_PARAM_SIZES),
        # array of parameter strings in the form: "param_name=param_value"
        ("param", PROCESSING_PARAMETERS_PARAMS),
    ]
