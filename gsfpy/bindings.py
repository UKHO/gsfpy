from ctypes import CDLL, POINTER, c_char, c_char_p, c_double, c_int, c_ubyte, string_at
from os import path

from .enums import FileMode, RecordType, SeekOption
from .gsfDataID import c_gsfDataID
from .gsfMBParams import c_gsfMBParams
from .gsfRecords import c_gsfRecords
from .gsfScaleFactors import c_gsfScaleFactors
from .gsfSwathBathyPing import c_gsfSwathBathyPing

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

_gsf_lib.gsfGetSwathBathyBeamWidths.argtypes = [
    POINTER(c_gsfRecords),
    POINTER(c_double),
    POINTER(c_double),
]
_gsf_lib.gsfGetSwathBathyBeamWidths.restype = c_int

_gsf_lib.gsfGetSwathBathyArrayMinMax.argtypes = [
    POINTER(c_gsfSwathBathyPing),
    c_int,
    POINTER(c_double),
    POINTER(c_double),
]
_gsf_lib.gsfGetSwathBathyArrayMinMax.restype = c_int

_gsf_lib.gsfIsStarboardPing.argtypes = [POINTER(c_gsfRecords)]
_gsf_lib.gsfIsStarboardPing.restype = c_int

_gsf_lib.gsfGetSonarTextName.argtypes = [POINTER(c_gsfSwathBathyPing)]
_gsf_lib.gsfGetSonarTextName.restype = c_char_p

_gsf_lib.gsfFileSupportsRecalculateXYZ.argtypes = [c_int, POINTER(c_int)]
_gsf_lib.gsfFileSupportsRecalculateXYZ.restype = c_int

_gsf_lib.gsfFileSupportsRecalculateTPU.argtypes = [c_int, POINTER(c_int)]
_gsf_lib.gsfFileSupportsRecalculateTPU.restype = c_int

_gsf_lib.gsfFileSupportsRecalculateNominalDepth.argtypes = [c_int, POINTER(c_int)]
_gsf_lib.gsfFileSupportsRecalculateNominalDepth.restype = c_int

_gsf_lib.gsfFileContainsMBAmplitude.argtypes = [c_int, POINTER(c_int)]
_gsf_lib.gsfFileContainsMBAmplitude.restype = c_int

_gsf_lib.gsfFileContainsMBImagery.argtypes = [c_int, POINTER(c_int)]
_gsf_lib.gsfFileContainsMBImagery.restype = c_int

_gsf_lib.gsfIsNewSurveyLine.argtypes = [
    c_int,
    POINTER(c_gsfRecords),
    c_double,
    POINTER(c_double),
]
_gsf_lib.gsfIsNewSurveyLine.restype = c_int

_gsf_lib.gsfInitializeMBParams.argtypes = [POINTER(c_gsfMBParams)]
_gsf_lib.gsfInitializeMBParams.restype = None

_gsf_lib.gsfPutMBParams.argtypes = [
    POINTER(c_gsfMBParams),
    POINTER(c_gsfRecords),
    c_int,
    c_int,
]
_gsf_lib.gsfPutMBParams.restype = c_int

_gsf_lib.gsfGetMBParams.argtypes = [
    POINTER(c_gsfRecords),
    POINTER(c_gsfMBParams),
    POINTER(c_int),
]
_gsf_lib.gsfGetMBParams.restype = c_int

_gsf_lib.gsfLoadScaleFactor.argtypes = [
    POINTER(c_gsfScaleFactors),
    c_int,
    c_char,
    c_double,
    c_int,
]
_gsf_lib.gsfLoadScaleFactor.restype = c_int

_gsf_lib.gsfGetScaleFactor.argtypes = [
    c_int,
    c_int,
    POINTER(c_ubyte),
    POINTER(c_double),
    POINTER(c_double),
]
_gsf_lib.gsfGetScaleFactor.restype = c_int

_gsf_lib.gsfSetDefaultScaleFactor.argtypes = [POINTER(c_gsfSwathBathyPing)]
_gsf_lib.gsfSetDefaultScaleFactor.restype = c_int

_gsf_lib.gsfFree.argtypes = [POINTER(c_gsfRecords)]
_gsf_lib.gsfFree.restype = None


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
) -> int:
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


def gsfPercent(handle: c_int) -> int:
    """
    :param handle: c_int
    :return: The current file position as a percentage of the file size if successful,
             otherwise -1.
    """
    return _gsf_lib.gsfPercent(handle)


def gsfGetSwathBathyBeamWidths(p_data, p_fore_aft, p_athwartship) -> int:
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


def gsfGetSwathBathyArrayMinMax(
    p_ping, subrecordID: c_int, p_min_value, p_max_value
) -> int:
    """
    :param p_ping: POINTER(gsfpy.gsfSwathBathyPing.c_gsfSwathBathyPing)
    :param p_min_value: POINTER(double)
    :param p_max_value: POINTER(double)
    :return: 0 if successful, otherwise -1. Note that, in the event of a successful
             call, the p_min_value and p_max_value parameters will be populated with
             the minimum and maximum supportable values for each of the swath
             bathymetry arrays in the given ping.
    """
    return _gsf_lib.gsfGetSwathBathyArrayMinMax(
        p_ping, subrecordID, p_min_value, p_max_value
    )


def gsfIsStarboardPing(p_data) -> int:
    """
    :param p_data: POINTER(gsfpy.gsfRecords.c_gsfRecords)
    :return: Non-zero if the ping contained in the passed data represents a starboard
             looking ping from a dual headed sonar installation. Otherwise, zero. If
             the sonar does not have dual transducers, zero is returned.
    """
    return _gsf_lib.gsfIsStarboardPing(p_data)


def gsfGetSonarTextName(p_ping) -> str:
    """
    :param p_ping: POINTER(gsfpy.gsfSwathBathyPing.c_gsfSwathBathyPing)
    :return: The name of the sensor based on the sensor id contained in the ping
             structure if this is defined, otherwise 'Unknown'.
    """
    p_sonar_name = _gsf_lib.gsfGetSonarTextName(p_ping)
    return string_at(p_sonar_name)


def gsfFileSupportsRecalculateXYZ(handle: c_int, p_status) -> int:
    """
    :param handle: c_int
    :param p_status: POINTER(c_int)
    :return:  0 if successful, otherwise -1. Note that, in the event of a successful
              call, p_status is assigned a value of 1 if the GSF file identified by
              the given handle provides sufficient information to support full
              recalculation of the platform relative XYZ values, otherwise 0.
    """
    return _gsf_lib.gsfFileSupportsRecalculateXYZ(handle, p_status)


def gsfFileSupportsRecalculateTPU(handle: c_int, p_status) -> int:
    """
    :param handle: c_int
    :param p_status: POINTER(c_int)
    :return:  0 if successful, otherwise -1. Note that, in the event of a successful
              call, p_status is assigned a value of 1 if the GSF file identified by
              the given handle contains sufficient information to support calculation
              of total propagated uncertainty (TPU) values, otherwise 0.
    """
    return _gsf_lib.gsfFileSupportsRecalculateTPU(handle, p_status)


def gsfFileSupportsRecalculateNominalDepth(handle: c_int, p_status) -> int:
    """
    :param handle: c_int
    :param p_status: POINTER(c_int)
    :return:  0 if successful, otherwise -1. Note that, in the event of a successful
              call, p_status is assigned a value of 1 if the GSF file identified by
              the given handle contains sufficient information to support calculation
              of the nominal depth array, otherwise 0.
    """
    return _gsf_lib.gsfFileSupportsRecalculateNominalDepth(handle, p_status)


def gsfFileContainsMBAmplitude(handle: c_int, p_status) -> int:
    """
    :param handle: c_int
    :param p_status: POINTER(c_int)
    :return:  0 if successful, otherwise -1. Note that, in the event of a successful
              call, p_status is assigned a value of 1 if the GSF file identified by
              the given handle contains the average per receive beam amplitude data,
              otherwise 0.
    """
    return _gsf_lib.gsfFileContainsMBAmplitude(handle, p_status)


def gsfFileContainsMBImagery(handle: c_int, p_status) -> int:
    """
    :param handle: c_int
    :param p_status: POINTER(c_int)
    :return:  0 if successful, otherwise -1. Note that, in the event of a successful
              call, p_status is assigned a value of 1 if the GSF file identified by
              the given handle contains the per-receive-beam imagery time series data,
              otherwise 0.
    """
    return _gsf_lib.gsfFileContainsMBImagery(handle, p_status)


def gsfIsNewSurveyLine(
    handle: c_int, p_rec, azimuth_change: c_double, p_last_heading
) -> int:
    """
    :param handle: c_int
    :param p_rec: POINTER(gsfpy.gsfRecords.c_gsfRecords)
    :param azimuth_change: c_double
    :param p_last_heading: POINTER(c_double)
    :return:  0 if the last ping in the given ping is not considered to be from a
              new survey line, and nonzero when the ping is considered to be from
              a new survey line, according to the given trigger value in the
              azimuth_change parameter. Note that p_rec must be populated with a
              gsfSwathBathyPing structure.
    """
    return _gsf_lib.gsfIsNewSurveyLine(handle, p_rec, azimuth_change, p_last_heading)


def gsfInitializeMBParams(p_mbparams) -> int:
    """
    :param p_mbparams: POINTER(gsfpy.gsfMBParams.c_gsfMBParams)
    :return: None (return value should be ignored). Note that, upon return, all fields
             of the given gsfMBParams structure will be initialized to unknown (-99
             for int fields)
    """
    return _gsf_lib.gsfInitializeMBParams(p_mbparams)


def gsfPutMBParams(p_mbparams, p_rec, handle: c_int, numArrays: c_int) -> int:
    """
    :param p_mbparams: POINTER(gsfpy.gsfMBParams.c_gsfMBParams)
    :param p_rec: POINTER(gsfpy.gsfRecords.c_gsfRecords)
    :param handle: c_int
    :param numArrays: c_int
    :return: 0 if successful, otherwise -1. Note that, in the event of a successful
             call, form parameters from the given gsfMBParams structure are written
             into the gsfProcessingParameters field of the given gsfRecords data
             structure.
    """
    return _gsf_lib.gsfPutMBParams(p_mbparams, p_rec, handle, numArrays)


def gsfGetMBParams(p_rec, p_mbparams, p_numArrays) -> int:
    """
    :param p_rec: POINTER(gsfpy.gsfRecords.c_gsfRecords)
    :param p_mbparams: POINTER(gsfpy.gsfMBParams.c_gsfMBParams)
    :param p_numArrays: POINTER(c_int)
    :return: 0 if successful, otherwise -1. Note that, in the event of a successful
             call, form parameters from the gsfProcessingParameters field of the
             given gsfRecords data structure are written into the given gsfMBParams
             structure.
    """
    return _gsf_lib.gsfGetMBParams(p_rec, p_mbparams, p_numArrays)


def gsfLoadScaleFactor(
    p_sf, subRecordID: c_int, c_flag: c_char, precision: c_double, offset: c_int
) -> int:
    """
    :param p_sf: POINTER(gsfpy.gsfRecords.c_gsfScaleFactors)
    :param subRecordID: c_int
    :param c_flag: c_char
    :param precision: c_double
    :param offset: c_int
    :return: 0 if successful, otherwise -1. Note that, in the event of a successful
             call, a swath bathymetry ping record scale factor structure is loaded
             into the given gsfScaleFactors structure. See GSF library documentation
             for further details.
    """
    return _gsf_lib.gsfLoadScaleFactor(p_sf, subRecordID, c_flag, precision, offset)


def gsfGetScaleFactor(
    handle: c_int, subRecordID: c_int, p_c_flag, p_multiplier, p_offset
) -> int:
    """
    :param handle: c_int
    :param subRecordID: c_int
    :param p_c_flag: POINTER(c_uchar)
    :param p_multiplier: POINTER(c_double)
    :param p_offset: POINTER(c_double)
    :return: 0 if successful, otherwise -1. Note that, in the event of a successful
             call, beam array field size, compression flag, multiplier and DC offset
             values by which each swath bathymetry ping array subrecord is scaled will
             be loaded into p_c_flag, p_multiplier, and p_offset parameters
             respectively. gsfGetScaleFactor() is called once for each array subrecord
             of interest. At least one swath bathymetry ping record must have been read
             from, or written to, the file specified by handle prior to calling
             gsfGetScaleFactor().
    """
    return _gsf_lib.gsfGetScaleFactor(
        handle, subRecordID, p_c_flag, p_multiplier, p_offset
    )


def gsfSetDefaultScaleFactor(p_mb_ping) -> int:
    """
    :param p_rec: POINTER(gsfpy.gsfSwathBathyPing.c_gsfSwathBathyPing)

    :return: 0 if successful. Note that, in the event of a successful call, estimated
             scale factors for each of the beam arrays in the ping will be set.
    """
    return _gsf_lib.gsfSetDefaultScaleFactor(p_mb_ping)


# TODO - see gsfpy issue #50
# def gsfFree(p_rec):
#     """
#     :param p_mbparams: POINTER(c_gsfRecords)
#     :return: None. Note that, upon return, the memory previously allocated to the
#              given gsfRecords structure will be deallocated.
#     """
#     return _gsf_lib.gsfFree(p_rec)
