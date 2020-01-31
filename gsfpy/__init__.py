from ctypes import *
from os import path

from . import enums
from . import gsfDataID
from . import gsfRecords

gsf_libpath = path.join(path.abspath(path.dirname(__file__)), 'libgsf3_06/libgsf3_06.so')
gsflib = CDLL(gsf_libpath)

'''
filename: bytestring e.g. b'path/to/file.gsf'
mode: gsfpy.enums.FileMode
handle: Instance of POINTER(c_int)
returns: 0 if successful, otherwise -1
'''
def gsfOpen(filename, mode, handle):
    return gsflib.gsfOpen(filename, mode, handle)

'''
handle: c_int
returns: 0 if successful, otherwise -1
'''
def gsfClose(handle):
    return gsflib.gsfClose(handle)
