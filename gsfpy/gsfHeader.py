from ctypes import Structure, c_char

GSF_VERSION_SIZE = 12
HEADER_VERSION = c_char * (GSF_VERSION_SIZE + 1)


class c_gsfHeader(Structure):
    _fields_ = [("version", HEADER_VERSION)]
