from ctypes import Structure, c_char, c_char_p, c_double, c_int

from . import timespec

HV_NAVIGATION_ERROR_SPARE_BYTES = c_char * 2


class c_gsfHVNavigationError(Structure):
    _fields_ = [
        ("nav_error_time", timespec.c_timespec),
        ("record_id", c_int),
        ("horizontal_error", c_double),
        ("vertical_error", c_double),
        ("SEP_uncertainty", c_double),
        ("spare", HV_NAVIGATION_ERROR_SPARE_BYTES),
        ("position_type", c_char_p),
    ]
