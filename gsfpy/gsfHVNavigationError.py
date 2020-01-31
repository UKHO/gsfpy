from ctypes import *

from . import timespec

HVNAVIGATIONERRORSPAREBYTES = c_char * 2

class c_gsfHVNavigationError(Structure):
    _fields_ = [('nav_error_time',      timespec.c_timespec),
                ('record_id',           c_int),
                ('horizontal_error',    c_double),
                ('vertical_error',      c_double),
                ('SEP_uncertainty',     c_double),
                ('spare',               HVNAVIGATIONERRORSPAREBYTES),
                ('position_type',       c_char_p)]