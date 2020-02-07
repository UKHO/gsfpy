from ctypes import CDLL, POINTER, c_char_p, c_int, c_ubyte
from os import path

from . import gsfDataID, gsfRecords

_gsf_lib_rel_path = "libgsf3_06/libgsf3_06.so"
_gsf_lib_abs_path = path.join(path.abspath(path.dirname(__file__)), _gsf_lib_rel_path)
_gsf_lib = CDLL(_gsf_lib_abs_path)


def gsfOpen(filename, mode, handle):
    """
    filename: bytestring e.g. b'path/to/file.gsf'
    mode: gsfpy.enums.FileMode
    handle: Instance of POINTER(c_int)
    returns: 0 if successful, otherwise -1
    """
    return _gsf_lib.gsfOpen(filename, mode, handle)


def gsfOpenBuffered(filename, mode, handle, buf_size):
    """
    filename: bytestring e.g. b'path/to/file.gsf'
    mode: gsfpy.enums.FileMode
    handle: Instance of POINTER(c_int)
    returns: 0 if successful, otherwise -1
    """
    return _gsf_lib.gsfOpenBuffered(filename, mode, handle, buf_size)


def gsfClose(handle):
    """
    handle: c_int
    returns: 0 if successful, otherwise -1
    """
    return _gsf_lib.gsfClose(handle)


def gsfSeek(handle, option):
    """
    handle: c_int
    option: gsfpy.enums.SeekOption
    returns: 0 if successful, otherwise -1
    """
    return _gsf_lib.gsfSeek(handle, option)


def gsfIntError():
    """
    returns: The last value that the GSF error code was set to (c_int).
    """
    return _gsf_lib.gsfIntError()


def gsfStringError():
    """
    returns: The last value that the GSF error message was set to (c_char_p).
    """
    gsfStringErrorC = _gsf_lib.gsfStringError
    gsfStringErrorC.argtypes = []
    gsfStringErrorC.restype = c_char_p
    return gsfStringErrorC()


def gsfRead(handle, desiredRecord, p_dataID, p_rec, p_stream, max_size):
    """
    handle: int
    desiredRecord: gsfpy.enums.RecordType
    p_dataID: POINTER(gsfpy.gsfDataID.c_gsfDataID)
    p_rec: POINTER(gsfpy.gsfRecords.c_gsfRecords)
    p_stream: POINTER(c_ubyte)
    max_size: int
    returns: number of bytes read if successful, otherwise -1. Note that contents of the
             POINTER parameters p_dataID, p_rec and p_stream will be updated upon
             successful read.
    """
    gsfReadC = _gsf_lib.gsfRead
    gsfReadC.argtypes = [
        c_int,
        c_int,
        POINTER(gsfDataID.c_gsfDataID),
        POINTER(gsfRecords.c_gsfRecords),
        POINTER(c_ubyte),
        c_int,
    ]
    gsfReadC.resType = c_int
    return gsfReadC(
        handle, c_int(desiredRecord.value), p_dataID, p_rec, p_stream, max_size
    )


def gsfWrite(handle, p_dataID, p_rec):
    """
    handle: int
    desiredRecord: gsfpy.enums.RecordType
    p_dataID: POINTER(gsfpy.gsfDataID.c_gsfDataID)
    p_rec: POINTER(gsfpy.gsfRecords.c_gsfRecords)
    p_stream: POINTER(c_ubyte)
    max_size: int
    returns: number of bytes read if successful, otherwise -1. Note that contents of the
             POINTER parameters p_dataID, p_rec and p_stream will be updated upon
             successful read.
    """
    gsfWriteC = _gsf_lib.gsfWrite
    gsfWriteC.argtypes = [
        c_int,
        POINTER(gsfDataID.c_gsfDataID),
        POINTER(gsfRecords.c_gsfRecords),
    ]
    gsfWriteC.resType = c_int
    return gsfWriteC(handle, p_dataID, p_rec)
