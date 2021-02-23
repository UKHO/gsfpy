"""Types"""
from ctypes import Structure, c_int, c_long


class c_timespec(Structure):
    _fields_ = [
        # NOTE - defined as time_t in gsf.h, but equivalent to int
        ("tv_sec", c_int),
        ("tv_nsec", c_long),
    ]
