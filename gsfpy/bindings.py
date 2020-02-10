from ctypes import CDLL, POINTER, c_char_p, c_int, c_ubyte
from os import path

from .enums import FileMode, RecordType, SeekOption
from .gsfDataID import c_gsfDataID
from .gsfRecords import c_gsfRecords

_gsf_lib_rel_path = "libgsf3_06/libgsf3_06.so"
_gsf_lib_abs_path = path.join(path.abspath(path.dirname(__file__)), _gsf_lib_rel_path)
_gsf_lib = CDLL(_gsf_lib_abs_path)

_gsf_lib.gsfOpen.argtypes = [c_char_p, c_int, POINTER(c_int)]
_gsf_lib.gsfOpen.restype = c_int


def gsfOpen(filename: bytes, mode: FileMode, p_handle):
    """
    filename: bytestring e.g. b'path/to/file.gsf'
    mode: gsfpy.enums.FileMode
    p_handle: Instance of POINTER(c_int)
    returns: 0 if successful, otherwise -1
    """
    return _gsf_lib.gsfOpen(filename, mode, p_handle)


_gsf_lib.gsfOpenBuffered.argtypes = [c_char_p, c_int, POINTER(c_int), c_int]
_gsf_lib.gsfOpenBuffered.restype = c_int


def gsfOpenBuffered(filename: bytes, mode: FileMode, p_handle, buf_size: c_int):
    """
    filename: bytestring e.g. b'path/to/file.gsf'
    mode: gsfpy.enums.FileMode
    p_handle: Instance of POINTER(c_int)
    buf_size: c_int
    returns: 0 if successful, otherwise -1
    """
    return _gsf_lib.gsfOpenBuffered(filename, mode, p_handle, buf_size)


_gsf_lib.gsfClose.argtypes = [c_int]
_gsf_lib.gsfClose.restype = c_int


def gsfClose(handle: c_int):
    """
    handle: c_int
    returns: 0 if successful, otherwise -1
    """
    return _gsf_lib.gsfClose(handle)


_gsf_lib.gsfSeek.argtypes = [c_int, c_int]
_gsf_lib.gsfSeek.restype = c_int


def gsfSeek(handle: c_int, option: SeekOption):
    """
    handle: c_int
    option: gsfpy.enums.SeekOption
    returns: 0 if successful, otherwise -1
    """
    return _gsf_lib.gsfSeek(handle, option)


_gsf_lib.gsfIntError.argtypes = []
_gsf_lib.gsfIntError.restype = c_int


def gsfIntError():
    """
    returns: The last value that the GSF error code was set to (c_int).
    """
    return _gsf_lib.gsfIntError()


_gsf_lib.gsfStringError.argtypes = []
_gsf_lib.gsfStringError.restype = c_char_p


def gsfStringError():
    """
    returns: The last value that the GSF error message was set to (c_char_p).
    """
    return _gsf_lib.gsfStringError()


_gsf_lib.gsfRead.argtypes = [
    c_int,
    c_int,
    POINTER(c_gsfDataID),
    POINTER(c_gsfRecords),
    POINTER(c_ubyte),
    c_int,
]
_gsf_lib.gsfRead.restype = c_int


def gsfRead(
    handle: c_int,
    desired_record: RecordType,
    p_data_id,
    p_records,
    p_stream=None,
    max_size=None,
):
    """
    handle : int
    desired_record : gsfpy.enums.RecordType
    p_data_id : POINTER(gsfpy.gsfDataID.c_gsfDataID)
    p_records : POINTER(gsfpy.gsfRecords.c_gsfRecords)
    p_stream : POINTER(c_ubyte)
    max_size : int
    returns: number of bytes read if successful, otherwise -1. Note that contents of the
             POINTER parameters p_data_id, p_records and p_stream will be updated upon
             successful read.
    """
    return _gsf_lib.gsfRead(
        handle, desired_record, p_data_id, p_records, p_stream, max_size,
    )


_gsf_lib.gsfWrite.argtypes = [c_int, POINTER(c_gsfDataID), POINTER(c_gsfRecords)]
_gsf_lib.gsfWrite.restype = c_int


def gsfWrite(handle: c_int, p_data_id, p_records) -> c_int:
    """
    handle: c_int
    p_data_id: POINTER(gsfpy.gsfDataID.c_gsfDataID)
    p_records: POINTER(gsfpy.gsfRecords.c_gsfRecords)
    returns: number of bytes written if successful, otherwise -1. Note that contents of
             the POINTER parameters p_data_id and p_records will be updated upon
             successful read.
    """
    return _gsf_lib.gsfWrite(handle, p_data_id, p_records)
