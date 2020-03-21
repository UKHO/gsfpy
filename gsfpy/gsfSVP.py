from ctypes import POINTER, Structure, c_double, c_int

from . import timespec


class c_gsfSVP(Structure):
    _fields_ = [
        ("observation_time", timespec.c_timespec),
        ("application_time", timespec.c_timespec),
        ("latitude", c_double),
        ("longitude", c_double),
        ("number_points", c_int),
        ("depth", POINTER(c_double)),
        ("sound_speed", POINTER(c_double)),
    ]
