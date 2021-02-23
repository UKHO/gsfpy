from ctypes import POINTER, Structure, c_double, c_short

from . import timespec


class c_gsfAttitude(Structure):
    _fields_ = [
        ("num_measurements", c_short),
        ("attitude_time", POINTER(timespec.c_timespec)),
        ("pitch", POINTER(c_double)),
        ("roll", POINTER(c_double)),
        ("heave", POINTER(c_double)),
        ("heading", POINTER(c_double)),
    ]
