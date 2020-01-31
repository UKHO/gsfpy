from ctypes import *

GSF_VERSION_SIZE = 12
HEADERVERSION = c_char * (GSF_VERSION_SIZE + 1)

class c_gsfHeader(Structure):
    _fields_ = [('version', HEADERVERSION)]