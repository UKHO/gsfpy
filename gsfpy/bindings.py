from ctypes import CDLL, POINTER, c_char_p, c_int, c_ubyte
from os import path

from .enums import FileMode, RecordType, SeekOption
from .gsfDataID import c_gsfDataID
from .gsfRecords import c_gsfRecords

_gsf_lib_rel_path = "libgsf/libgsf03-08.so"
_gsf_lib_abs_path = path.join(path.abspath(path.dirname(__file__)), _gsf_lib_rel_path)
_gsf_lib = CDLL(_gsf_lib_abs_path)

_gsf_lib.gsfClose.argtypes = [c_int]
_gsf_lib.gsfClose.restype = c_int

_gsf_lib.gsfIntError.argtypes = []
_gsf_lib.gsfIntError.restype = c_int

_gsf_lib.gsfOpen.argtypes = [c_char_p, c_int, (POINTER(c_int))]
_gsf_lib.gsfOpen.restype = c_int

_gsf_lib.gsfOpenBuffered.argtypes = [c_char_p, c_int, (POINTER(c_int)), c_int]
_gsf_lib.gsfOpenBuffered.restype = c_int

_gsf_lib.gsfRead.argtypes = [
    c_int,
    c_int,
    POINTER(c_gsfDataID),
    POINTER(c_gsfRecords),
    POINTER(c_ubyte),
    c_int,
]
_gsf_lib.gsfRead.restype = c_int

_gsf_lib.gsfSeek.argtypes = [c_int, c_int]
_gsf_lib.gsfSeek.restype = c_int

_gsf_lib.gsfStringError.argtypes = []
_gsf_lib.gsfStringError.restype = c_char_p

_gsf_lib.gsfWrite.argtypes = [c_int, POINTER(c_gsfDataID), POINTER(c_gsfRecords)]
_gsf_lib.gsfWrite.restype = c_int

_gsf_lib.gsfGetNumberRecords.argtypes = [c_int, c_int]
_gsf_lib.gsfGetNumberRecords.restype = c_int


def gsfOpen(filename: bytes, mode: FileMode, p_handle) -> int:
    """
    :param filename: bytestring e.g. b'path/to/file.gsf'
    :param mode: gsfpy.enums.FileMode
    :param p_handle: Instance of POINTER(c_int)
    :return: 0 if successful, otherwise -1
    """
    return _gsf_lib.gsfOpen(filename, mode, p_handle)


def gsfOpenBuffered(filename: bytes, mode: FileMode, p_handle, buf_size: int) -> int:
    """
    :param filename: bytestring e.g. b'path/to/file.gsf'
    :param mode: gsfpy.enums.FileMode
    :param p_handle: Instance of POINTER(c_int)
    :param buf_size: c_int
    :return: 0 if successful, otherwise -1
    """
    return _gsf_lib.gsfOpenBuffered(filename, mode, p_handle, buf_size)


def gsfClose(handle: c_int) -> int:
    """
    :param handle: c_int
    :return: 0 if successful, otherwise -1
    """
    return _gsf_lib.gsfClose(handle)


def gsfSeek(handle: c_int, option: SeekOption) -> int:
    """
    :param handle: c_int
    :param option: gsfpy.enums.SeekOption
    :return: 0 if successful, otherwise -1
    """
    return _gsf_lib.gsfSeek(handle, option)


def gsfIntError() -> int:
    """
    :return: The last value that the GSF error code was set to (c_int).
    """
    return _gsf_lib.gsfIntError()


def gsfStringError() -> bytes:
    """
    :return: The last value that the GSF error message was set to (c_char_p).
    """
    return _gsf_lib.gsfStringError()


def gsfRead(
    handle: c_int,
    desired_record: RecordType,
    p_data_id,
    p_records,
    p_stream=None,
    max_size=0,
) -> int:
    """
    :param handle: int
    :param desired_record: gsfpy.enums.RecordType
    :param p_data_id: POINTER(gsfpy.gsfDataID.c_gsfDataID)
    :param p_records: POINTER(gsfpy.gsfRecords.c_gsfRecords)
    :param p_stream: POINTER(c_ubyte)
    :param max_size: int
    :return: number of bytes read if successful, otherwise -1. Note that contents of the
             POINTER parameters p_data_id, p_records and p_stream will be updated upon
             successful read.
    """
    return _gsf_lib.gsfRead(
        handle, desired_record, p_data_id, p_records, p_stream, max_size,
    )


def gsfWrite(handle: c_int, p_data_id, p_records) -> int:
    """
    :param handle: c_int
    :param p_data_id: POINTER(gsfpy.gsfDataID.c_gsfDataID)
    :param p_records: POINTER(gsfpy.gsfRecords.c_gsfRecords)
    :return: number of bytes written if successful, otherwise -1. Note that contents of
             the POINTER parameters p_data_id and p_records will be updated upon
             successful read.
    """
    return _gsf_lib.gsfWrite(handle, p_data_id, p_records)


def gsfGetNumberRecords(handle: c_int, desired_record: RecordType) -> int:
    """
    File must be open for direct access (GSF_READONLY_INDEX or GSF_UPDATE_INDEX)
    :param handle: c_int
    :param desired_record: gsfpy.enums.RecordType
    :return: number of records of type desired_record, otherwise -1
    """
    return _gsf_lib.gsfGetNumberRecords(handle, desired_record)


def gsfIndexTime(
    handle: c_int, record_type: c_int, record_number: c_int, p_sec, p_nsec
):
    """
    :param handle: c_int
    :param record_type: gsfpy.enums.RecordType
    :param record_number: c_int
    :param p_sec: POINTER(c_int)
    :param p_nsec: POINTER(c_long)
    :return: The record number if successful, otherwise -1. Note that contents of
             the POINTER parameters p_sec and p_nsec will be updated upon
             successful read with seconds since the beginning of the epoch (p_sec)
             and nanoseconds since the beginning of the second (p_nsec).
    """
    return _gsf_lib.gsfIndexTime(handle, record_type, record_number, p_sec, p_nsec)


def gsfPercent(handle: c_int):
    """
    :param handle: c_int
    :return: The current file position as a percentage of the file size if successful,
             otherwise -1.
    """
    return _gsf_lib.gsfPercent(handle)


def gsfGetSwathBathyBeamWidths(p_data, p_fore_aft, p_athwartship):
    """
    :param p_data: POINTER(gsfpy.gsfRecords.c_gsfRecords)
    :param p_fore_aft: POINTER(double)
    :param p_athwartship: POINTER(double)
    :return: 0 if successful, otherwise -1. Note that, in the event of a successful
             call, the p_fore_aft and p_athwartship parameters will be populated with
             the fore-aft and the port-starboard beam widths in degrees for the given
             gsfRecords data structure containing a populated gsfSwathBathyPing
             structure.
    """
    return _gsf_lib.gsfGetSwathBathyBeamWidths(p_data, p_fore_aft, p_athwartship)
