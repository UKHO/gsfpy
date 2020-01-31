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
filename: bytestring e.g. b'path/to/file.gsf'
mode: gsfpy.enums.FileMode
handle: Instance of POINTER(c_int)
returns: 0 if successful, otherwise -1
'''
def gsfOpenBuffered(filename, mode, handle, buf_size):
    return gsflib.gsfOpenBuffered(filename, mode, handle, buf_size)

'''
handle: c_int
returns: 0 if successful, otherwise -1
'''
def gsfClose(handle):
    return gsflib.gsfClose(handle)

'''
handle: c_int
option: gsfpy.enums.SeekOption
returns: 0 if successful, otherwise -1
'''
def gsfSeek(handle, option):
    return gsflib.gsfSeek(handle, option)

'''
returns: The last value that the GSF error code was set to (c_int).
'''
def gsfIntError():
    return gsflib.gsfIntError()

'''
returns: The last value that the GSF error message was set to (c_char_p).
'''
def gsfStringError():
    gsfErrorMessage = c_char_p()
    gsfStringErrorC = gsflib.gsfStringError
    gsfStringErrorC.argtypes = []
    gsfStringErrorC.restype = c_char_p
    return gsfStringErrorC()

'''
handle: int
desiredRecord: gsfpy.enums.RecordType
p_dataID: POINTER(gsfpy.gsfDataID.c_gsfDataID)
p_rec: POINTER(gsfpy.gsfRecords.c_gsfRecords)
p_stream: POINTER(c_ubyte)
max_size: int
returns: number of bytes read if successful, otherwise -1. Note that contents of the POINTER parameters
         p_dataID, p_rec and p_stream will be updated upon successful read.
'''
def gsfRead(handle, desiredRecord, p_dataID, p_rec, p_stream, max_size):
    gsfReadC = gsflib.gsfRead
    gsfReadC.argtypes = [c_int, c_int, POINTER(gsfDataID.c_gsfDataID), POINTER(gsfRecords.c_gsfRecords), POINTER(c_ubyte), c_int]
    gsfReadC.resType = c_int
    return gsfReadC(handle, c_int(desiredRecord.value), p_dataID, p_rec, p_stream, max_size)

'''
handle: int
desiredRecord: gsfpy.enums.RecordType
p_dataID: POINTER(gsfpy.gsfDataID.c_gsfDataID)
p_rec: POINTER(gsfpy.gsfRecords.c_gsfRecords)
p_stream: POINTER(c_ubyte)
max_size: int
returns: number of bytes read if successful, otherwise -1. Note that contents of the POINTER parameters
         p_dataID, p_rec and p_stream will be updated upon successful read.
'''
def gsfWrite(handle, p_dataID, p_rec):
    gsfWriteC = gsflib.gsfWrite
    gsfWriteC.argtypes = [c_int, POINTER(gsfDataID.c_gsfDataID), POINTER(gsfRecords.c_gsfRecords)]
    gsfWriteC.resType = c_int
    return gsfWriteC(handle, p_dataID, p_rec)
