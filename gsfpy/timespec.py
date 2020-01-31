from ctypes import *

# Types
class c_timespec(Structure):
    _fields_ = [('tv_sec', c_int),                  # FIXME - defined as time_t in gsf.h, but equivalent to int
                ('tv_nsec', c_long)]