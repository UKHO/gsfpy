from ctypes import *

from . import timespec
from . import gsfSBSensorSpecific

class c_gsfSingleBeamPing(Structure):
    _fields_ = [('ping_time',                   timespec.c_timespec),
                ('latitude',                    c_double),
                ('longitude',                   c_double),
                ('tide_corrector',              c_double),
                ('depth_corrector',             c_double),
                ('heading',                     c_double),
                ('pitch',                       c_double),
                ('roll',                        c_double),
                ('heave',                       c_double),
                ('depth',                       c_double),
                ('sound_speed_correction',      c_double),
                ('positioning_system_type',     c_ushort),
                ('sensor_id',                   c_int),
                ('sensor_data',                 gsfSBSensorSpecific.c_gsfSensorSpecific)]