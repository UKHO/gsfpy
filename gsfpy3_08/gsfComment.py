from ctypes import POINTER, Structure, c_char, c_int

from . import timespec


class c_gsfComment(Structure):
    _fields_ = [
        ("comment_time", timespec.c_timespec),
        ("comment_length", c_int),
        ("comment", POINTER(c_char)),
    ]
