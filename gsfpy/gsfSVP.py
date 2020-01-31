from ctypes import *

from . import timespec

class c_gsfSVP(Structure):
    _fields_ = [('observation_time',    timespec.c_timespec),
                ('application_time',    timespec.c_timespec),
                ('longitude',           c_double),
                ('latitude',            c_double),
                ('number_points',       c_int),
                ('depth',               POINTER(c_double)),
                ('sound_speed',         POINTER(c_double))]