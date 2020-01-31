from ctypes import *

from . import timespec

class c_gsfEchotracSpecific(Structure):
    _fields_ = [('navigation_error',        c_int),
                ('mpp_source',              c_ushort),
                ('tide_source',             c_ushort)]

class c_gsfMGD77Specific(Structure):
    _fields_ = [('time_zone_corr',          c_ushort),
                ('position_type_code',      c_ushort),
                ('correction_code',         c_ushort),
                ('bathy_type_code',         c_ushort),
                ('quality_code',            c_ushort),
                ('travel_time',             c_double)]

class c_gsfBDBSpecific(Structure):
    _fields_ = [('doc_no',                  c_int),
                ('eval',                    c_char),
                ('classification',          c_char),
                ('track_adj_flag',          c_char),
                ('source_flag',             c_char),
                ('pt_or_track_ln',          c_char),
                ('datum_flag',              c_char)]

class c_gsfNOSHDBSpecific(Structure):
    _fields_ = [('type_code',               c_ushort),
                ('carto_code',              c_ushort)]

class c_gsfSensorSpecific(Union):
    _fields_ = [('gsfEchotracSpecific',         c_gsfEchotracSpecific),
                ('gsfBathy2000Specific',        c_gsfEchotracSpecific),
                ('gsfMGD77Specific',            c_gsfMGD77Specific),
                ('gsfBDBSpecific',              c_gsfBDBSpecific),
                ('gsfNOSHDBSpecific',           c_gsfNOSHDBSpecific)]