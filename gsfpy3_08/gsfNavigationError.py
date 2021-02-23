from ctypes import Structure, c_double, c_int

from . import timespec


class c_gsfNavigationError(Structure):
    _fields_ = [
        ("nav_error_time", timespec.c_timespec),
        ("record_id", c_int),
        ("latitude_error", c_double),
        ("longitude_error", c_double),
    ]
