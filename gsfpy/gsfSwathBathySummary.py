from ctypes import *

from . import timespec

class c_gsfSwathBathySummary(Structure):
    _fields_ = [('start_time', timespec.c_timespec),
                ('end_time', timespec.c_timespec),
                ('min_latitude', c_double),
                ('min_longitude', c_double),
                ('max_latitude', c_double),
                ('max_longitude', c_double),
                ('min_depth', c_double),
                ('max_depth', c_double)]