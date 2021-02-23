from ctypes import (
    CDLL,
    POINTER,
    c_char,
    c_char_p,
    c_double,
    c_int,
    c_longlong,
    c_ubyte,
    c_ushort,
    memmove,
    sizeof,
    string_at,
)
from os import environ
from pathlib import Path

from .enums import FileMode, RecordType, SeekOption
from .GSF_POSITION import c_GSF_POSITION
from .GSF_POSITION_OFFSETS import c_GSF_POSITION_OFFSETS
from .gsfDataID import c_gsfDataID
from .gsfMBParams import c_gsfMBParams
from .gsfRecords import c_gsfRecords
from .gsfScaleFactors import c_gsfScaleFactors
from .gsfSwathBathyPing import c_gsfSwathBathyPing

_libgsf_abs_path = str(Path(__file__).parent / "libgsf" / "libgsf03-09.so")

# Check if the libgsf shared object library location is specified in the environment.
# If so, use the specified library in preference to the bundled version. Handle the
# case where the library cannot be found.
if "GSFPY3_09_LIBGSF_PATH" in environ:
    _libgsf_abs_path = environ["GSFPY3_09_LIBGSF_PATH"]

try:
    _libgsf = CDLL(_libgsf_abs_path)
except OSError as osex:
    raise Exception(
        f"Cannot load shared library from {_libgsf_abs_path}. Set the "
        f"$GSFPY3_09_LIBGSF_PATH environment variable to the correct path, "
        f"or remove it from the environment to use the default version."
    ) from osex

_libgsf.gsfClose.argtypes = [c_int]
_libgsf.gsfClose.restype = c_int

_libgsf.gsfIntError.argtypes = []
_libgsf.gsfIntError.restype = c_int

_libgsf.gsfOpen.argtypes = [c_char_p, c_int, (POINTER(c_int))]
_libgsf.gsfOpen.restype = c_int

_libgsf.gsfOpenBuffered.argtypes = [c_char_p, c_int, (POINTER(c_int)), c_int]
_libgsf.gsfOpenBuffered.restype = c_int

_libgsf.gsfRead.argtypes = [
    c_int,
    c_int,
    POINTER(c_gsfDataID),
    POINTER(c_gsfRecords),
    POINTER(c_ubyte),
    c_int,
]
_libgsf.gsfRead.restype = c_int

_libgsf.gsfSeek.argtypes = [c_int, c_int]
_libgsf.gsfSeek.restype = c_int

_libgsf.gsfStringError.argtypes = []
_libgsf.gsfStringError.restype = c_char_p

_libgsf.gsfWrite.argtypes = [c_int, POINTER(c_gsfDataID), POINTER(c_gsfRecords)]
_libgsf.gsfWrite.restype = c_int

_libgsf.gsfGetNumberRecords.argtypes = [c_int, c_int]
_libgsf.gsfGetNumberRecords.restype = c_int

_libgsf.gsfGetSwathBathyBeamWidths.argtypes = [
    POINTER(c_gsfRecords),
    POINTER(c_double),
    POINTER(c_double),
]
_libgsf.gsfGetSwathBathyBeamWidths.restype = c_int

_libgsf.gsfGetSwathBathyArrayMinMax.argtypes = [
    POINTER(c_gsfSwathBathyPing),
    c_int,
    POINTER(c_double),
    POINTER(c_double),
]
_libgsf.gsfGetSwathBathyArrayMinMax.restype = c_int

_libgsf.gsfIsStarboardPing.argtypes = [POINTER(c_gsfRecords)]
_libgsf.gsfIsStarboardPing.restype = c_int

_libgsf.gsfGetSonarTextName.argtypes = [POINTER(c_gsfSwathBathyPing)]
_libgsf.gsfGetSonarTextName.restype = c_char_p

_libgsf.gsfFileSupportsRecalculateXYZ.argtypes = [c_int, POINTER(c_int)]
_libgsf.gsfFileSupportsRecalculateXYZ.restype = c_int

_libgsf.gsfFileSupportsRecalculateTPU.argtypes = [c_int, POINTER(c_int)]
_libgsf.gsfFileSupportsRecalculateTPU.restype = c_int

_libgsf.gsfFileSupportsRecalculateNominalDepth.argtypes = [c_int, POINTER(c_int)]
_libgsf.gsfFileSupportsRecalculateNominalDepth.restype = c_int

_libgsf.gsfFileContainsMBAmplitude.argtypes = [c_int, POINTER(c_int)]
_libgsf.gsfFileContainsMBAmplitude.restype = c_int

_libgsf.gsfFileContainsMBImagery.argtypes = [c_int, POINTER(c_int)]
_libgsf.gsfFileContainsMBImagery.restype = c_int

_libgsf.gsfIsNewSurveyLine.argtypes = [
    c_int,
    POINTER(c_gsfRecords),
    c_double,
    POINTER(c_double),
]
_libgsf.gsfIsNewSurveyLine.restype = c_int

_libgsf.gsfInitializeMBParams.argtypes = [POINTER(c_gsfMBParams)]
_libgsf.gsfInitializeMBParams.restype = None

_libgsf.gsfPutMBParams.argtypes = [
    POINTER(c_gsfMBParams),
    POINTER(c_gsfRecords),
    c_int,
    c_int,
]
_libgsf.gsfPutMBParams.restype = c_int

_libgsf.gsfGetMBParams.argtypes = [
    POINTER(c_gsfRecords),
    POINTER(c_gsfMBParams),
    POINTER(c_int),
]
_libgsf.gsfGetMBParams.restype = c_int

_libgsf.gsfStat.argtypes = [
    POINTER(c_char),
    POINTER(c_longlong),
]
_libgsf.gsfStat.restype = c_int

_libgsf.gsfGetPositionDestination.argtypes = [
    c_GSF_POSITION,
    c_GSF_POSITION_OFFSETS,
    c_double,
    c_double,
]
_libgsf.gsfGetPositionDestination.restype = POINTER(c_GSF_POSITION)

_libgsf.gsfGetPositionOffsets.argtypes = [
    c_GSF_POSITION,
    c_GSF_POSITION,
    c_double,
    c_double,
]
_libgsf.gsfGetPositionOffsets.restype = POINTER(c_GSF_POSITION_OFFSETS)

_libgsf.gsfLoadScaleFactor.argtypes = [
    POINTER(c_gsfScaleFactors),
    c_int,
    c_char,
    c_double,
    c_int,
]
_libgsf.gsfLoadScaleFactor.restype = c_int

_libgsf.gsfGetScaleFactor.argtypes = [
    c_int,
    c_int,
    POINTER(c_ubyte),
    POINTER(c_double),
    POINTER(c_double),
]
_libgsf.gsfGetScaleFactor.restype = c_int

_libgsf.gsfSetDefaultScaleFactor.argtypes = [POINTER(c_gsfSwathBathyPing)]
_libgsf.gsfSetDefaultScaleFactor.restype = c_int

_libgsf.gsfLoadDepthScaleFactorAutoOffset.argtypes = [
    POINTER(c_gsfSwathBathyPing),
    c_int,
    c_int,
    c_double,
    c_double,
    POINTER(c_double),
    POINTER(c_ubyte),
    c_double,
]
_libgsf.gsfLoadDepthScaleFactorAutoOffset.restype = c_int


def gsfOpen(filename: bytes, mode: FileMode, p_handle) -> int:
    """
    :param filename: bytestring e.g. b'path/to/file.gsf'
    :param mode: gsfpy3_09.enums.FileMode
    :param p_handle: Instance of POINTER(c_int)
    :return: 0 if successful, otherwise -1
    """
    return _libgsf.gsfOpen(filename, mode, p_handle)


def gsfOpenBuffered(filename: bytes, mode: FileMode, p_handle, buf_size: int) -> int:
    """
    :param filename: bytestring e.g. b'path/to/file.gsf'
    :param mode: gsfpy3_09.enums.FileMode
    :param p_handle: Instance of POINTER(c_int)
    :param buf_size: c_int
    :return: 0 if successful, otherwise -1
    """
    return _libgsf.gsfOpenBuffered(filename, mode, p_handle, buf_size)


def gsfClose(handle: c_int) -> int:
    """
    :param handle: c_int
    :return: 0 if successful, otherwise -1
    """
    return _libgsf.gsfClose(handle)


def gsfSeek(handle: c_int, option: SeekOption) -> int:
    """
    :param handle: c_int
    :param option: gsfpy3_09.enums.SeekOption
    :return: 0 if successful, otherwise -1
    """
    return _libgsf.gsfSeek(handle, option)


def gsfIntError() -> int:
    """
    :return: The last value that the GSF error code was set to (c_int).
    """
    return _libgsf.gsfIntError()


def gsfStringError() -> bytes:
    """
    :return: The last value that the GSF error message was set to (c_char_p).
    """
    return _libgsf.gsfStringError()


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
    :param desired_record: gsfpy3_09.enums.RecordType
    :param p_data_id: POINTER(gsfpy3_09.gsfDataID.c_gsfDataID)
    :param p_records: POINTER(gsfpy3_09.gsfRecords.c_gsfRecords)
    :param p_stream: POINTER(c_ubyte)
    :param max_size: int
    :return: number of bytes read if successful, otherwise -1. Note that contents of the
             POINTER parameters p_data_id, p_records and p_stream will be updated upon
             successful read.
    """
    return _libgsf.gsfRead(
        handle, desired_record, p_data_id, p_records, p_stream, max_size,
    )


def gsfWrite(handle: c_int, p_data_id, p_records) -> int:
    """
    :param handle: c_int
    :param p_data_id: POINTER(gsfpy3_09.gsfDataID.c_gsfDataID)
    :param p_records: POINTER(gsfpy3_09.gsfRecords.c_gsfRecords)
    :return: number of bytes written if successful, otherwise -1. Note that contents of
             the POINTER parameters p_data_id and p_records will be updated upon
             successful read.
    """
    return _libgsf.gsfWrite(handle, p_data_id, p_records)


def gsfGetNumberRecords(handle: c_int, desired_record: RecordType) -> int:
    """
    File must be open for direct access (GSF_READONLY_INDEX or GSF_UPDATE_INDEX)
    :param handle: c_int
    :param desired_record: gsfpy3_09.enums.RecordType
    :return: number of records of type desired_record, otherwise -1
    """
    return _libgsf.gsfGetNumberRecords(handle, desired_record)


def gsfIndexTime(
    handle: c_int, record_type: RecordType, record_number: c_int, p_sec, p_nsec
) -> int:
    """
    :param handle: c_int
    :param record_type: gsfpy3_09.enums.RecordType
    :param record_number: c_int
    :param p_sec: POINTER(c_int)
    :param p_nsec: POINTER(c_long)
    :return: The record number if successful, otherwise -1. Note that contents of
             the POINTER parameters p_sec and p_nsec will be updated upon
             successful read with seconds since the beginning of the epoch (p_sec)
             and nanoseconds since the beginning of the second (p_nsec).
    """
    return _libgsf.gsfIndexTime(handle, record_type, record_number, p_sec, p_nsec)


def gsfPercent(handle: c_int) -> int:
    """
    :param handle: c_int
    :return: The current file position as a percentage of the file size if successful,
             otherwise -1.
    """
    return _libgsf.gsfPercent(handle)


def gsfGetSwathBathyBeamWidths(p_data, p_fore_aft, p_athwartship) -> int:
    """
    :param p_data: POINTER(gsfpy3_09.gsfRecords.c_gsfRecords)
    :param p_fore_aft: POINTER(double)
    :param p_athwartship: POINTER(double)
    :return: 0 if successful, otherwise -1. Note that, in the event of a successful
             call, the p_fore_aft and p_athwartship parameters will be populated with
             the fore-aft and the port-starboard beam widths in degrees for the given
             gsfRecords data structure containing a populated gsfSwathBathyPing
             structure.
    """
    return _libgsf.gsfGetSwathBathyBeamWidths(p_data, p_fore_aft, p_athwartship)


def gsfGetSwathBathyArrayMinMax(
    p_ping, subrecord_id: c_int, p_min_value, p_max_value
) -> int:
    """
    :param p_ping: POINTER(gsfpy3_09.gsfSwathBathyPing.c_gsfSwathBathyPing)
    :param p_min_value: POINTER(double)
    :param p_max_value: POINTER(double)
    :return: 0 if successful, otherwise -1. Note that, in the event of a successful
             call, the p_min_value and p_max_value parameters will be populated with
             the minimum and maximum supportable values for each of the swath
             bathymetry arrays in the given ping.
    """
    return _libgsf.gsfGetSwathBathyArrayMinMax(
        p_ping, subrecord_id, p_min_value, p_max_value
    )


def gsfIsStarboardPing(p_data) -> int:
    """
    :param p_data: POINTER(gsfpy3_09.gsfRecords.c_gsfRecords)
    :return: Non-zero if the ping contained in the passed data represents a starboard
             looking ping from a dual headed sonar installation. Otherwise, zero. If
             the sonar does not have dual transducers, zero is returned.
    """
    return _libgsf.gsfIsStarboardPing(p_data)


def gsfGetSonarTextName(p_ping) -> str:
    """
    :param p_ping: POINTER(gsfpy3_09.gsfSwathBathyPing.c_gsfSwathBathyPing)
    :return: The name of the sensor based on the sensor id contained in the ping
             structure if this is defined, otherwise 'Unknown'.
    """
    p_sonar_name = _libgsf.gsfGetSonarTextName(p_ping)
    return string_at(p_sonar_name).decode()


def gsfFileSupportsRecalculateXYZ(handle: c_int, p_status) -> int:
    """
    :param handle: c_int
    :param p_status: POINTER(c_int)
    :return:  0 if successful, otherwise -1. Note that, in the event of a successful
              call, p_status is assigned a value of 1 if the GSF file identified by
              the given handle provides sufficient information to support full
              recalculation of the platform relative XYZ values, otherwise 0.
    """
    return _libgsf.gsfFileSupportsRecalculateXYZ(handle, p_status)


def gsfFileSupportsRecalculateTPU(handle: c_int, p_status) -> int:
    """
    :param handle: c_int
    :param p_status: POINTER(c_int)
    :return:  0 if successful, otherwise -1. Note that, in the event of a successful
              call, p_status is assigned a value of 1 if the GSF file identified by
              the given handle contains sufficient information to support calculation
              of total propagated uncertainty (TPU) values, otherwise 0.
    """
    return _libgsf.gsfFileSupportsRecalculateTPU(handle, p_status)


def gsfFileSupportsRecalculateNominalDepth(handle: c_int, p_status) -> int:
    """
    :param handle: c_int
    :param p_status: POINTER(c_int)
    :return:  0 if successful, otherwise -1. Note that, in the event of a successful
              call, p_status is assigned a value of 1 if the GSF file identified by
              the given handle contains sufficient information to support calculation
              of the nominal depth array, otherwise 0.
    """
    return _libgsf.gsfFileSupportsRecalculateNominalDepth(handle, p_status)


def gsfFileContainsMBAmplitude(handle: c_int, p_status) -> int:
    """
    :param handle: c_int
    :param p_status: POINTER(c_int)
    :return:  0 if successful, otherwise -1. Note that, in the event of a successful
              call, p_status is assigned a value of 1 if the GSF file identified by
              the given handle contains the average per receive beam amplitude data,
              otherwise 0.
    """
    return _libgsf.gsfFileContainsMBAmplitude(handle, p_status)


def gsfFileContainsMBImagery(handle: c_int, p_status) -> int:
    """
    :param handle: c_int
    :param p_status: POINTER(c_int)
    :return:  0 if successful, otherwise -1. Note that, in the event of a successful
              call, p_status is assigned a value of 1 if the GSF file identified by
              the given handle contains the per-receive-beam imagery time series data,
              otherwise 0.
    """
    return _libgsf.gsfFileContainsMBImagery(handle, p_status)


def gsfIsNewSurveyLine(
    handle: c_int, p_rec, azimuth_change: c_double, p_last_heading
) -> int:
    """
    :param handle: c_int
    :param p_rec: POINTER(gsfpy3_09.gsfRecords.c_gsfRecords)
    :param azimuth_change: c_double
    :param p_last_heading: POINTER(c_double)
    :return:  0 if the last ping in the given ping is not considered to be from a
              new survey line, and nonzero when the ping is considered to be from
              a new survey line, according to the given trigger value in the
              azimuth_change parameter. Note that p_rec must be populated with a
              gsfSwathBathyPing structure.
    """
    return _libgsf.gsfIsNewSurveyLine(handle, p_rec, azimuth_change, p_last_heading)


def gsfInitializeMBParams(p_mbparams) -> int:
    """
    :param p_mbparams: POINTER(gsfpy3_09.gsfMBParams.c_gsfMBParams)
    :return: None (return value should be ignored). Note that, upon return, all fields
             of the given gsfMBParams structure will be initialized to unknown (-99
             for int fields)
    """
    return _libgsf.gsfInitializeMBParams(p_mbparams)


def gsfCopyRecords(p_target, p_source):
    """
    :param p_target: POINTER(gsfpy3_09.gsfRecords.c_gsfRecords). Note that this parameter
                     must be passed as a pointer() rather than a byref().
    :param p_source: POINTER(gsfpy3_09.gsfRecords.c_gsfRecords). Note that this parameter
                     must be passed as a pointer() rather than a byref().
    :return: 0 if successful, otherwise -1. Note that, in the event of a successful
             call, all content from the source gsfRecords structure is copied to
             the target structure.
    """
    try:
        # Note - implement using memmove() as calling _libgsf.gsfCopyRecords()
        #        results in segfault due to memory ownership clashes between
        #        calling application and library.
        memmove(p_target, p_source, sizeof(p_source.contents))
        ret_val = 0
    except Exception:
        ret_val = -1

    return ret_val


def gsfPutMBParams(p_mbparams, p_rec, handle: c_int, numArrays: c_int) -> int:
    """
    :param p_mbparams: POINTER(gsfpy3_09.gsfMBParams.c_gsfMBParams)
    :param p_rec: POINTER(gsfpy3_09.gsfRecords.c_gsfRecords)
    :param handle: c_int
    :param numArrays: c_int
    :return: 0 if successful, otherwise -1. Note that, in the event of a successful
             call, form parameters from the given gsfMBParams structure are written
             into the gsfProcessingParameters field of the given gsfRecords data
             structure.
    """
    return _libgsf.gsfPutMBParams(p_mbparams, p_rec, handle, numArrays)


def gsfGetMBParams(p_rec, p_mbparams, p_numArrays) -> int:
    """
    :param p_rec: POINTER(gsfpy3_09.gsfRecords.c_gsfRecords)
    :param p_mbparams: POINTER(gsfpy3_09.gsfMBParams.c_gsfMBParams)
    :param p_numArrays: POINTER(c_int)
    :return: 0 if successful, otherwise -1. Note that, in the event of a successful
             call, form parameters from the gsfProcessingParameters field of the
             given gsfRecords data structure are written into the given gsfMBParams
             structure.
    """
    return _libgsf.gsfGetMBParams(p_rec, p_mbparams, p_numArrays)


def gsfStat(p_filename, p_sz) -> int:
    """
    :param p_filename: POINTER(c_char)
    :param p_sz: POINTER(c_longlong)
    :return: 0 if successful, otherwise -1. Note that, in the event of a successful
             call, the contents of the p_sz parameter are updated with the size
             (in bytes) of the file identified by p_filename.
    """
    return _libgsf.gsfStat(p_filename, p_sz)


def gsfLoadScaleFactor(
    p_sf, subrecord_id: c_int, c_flag: c_char, precision: c_double, offset: c_int
) -> int:
    """
    :param p_sf: POINTER(gsfpy3_09.gsfRecords.c_gsfScaleFactors)
    :param subrecord_id: c_int
    :param c_flag: c_char
    :param precision: c_double
    :param offset: c_int
    :return: 0 if successful, otherwise -1. Note that, in the event of a successful
             call, a swath bathymetry ping record scale factor structure is loaded
             into the given gsfScaleFactors structure. See GSF library documentation
             for further details.
    """
    return _libgsf.gsfLoadScaleFactor(p_sf, subrecord_id, c_flag, precision, offset)


def gsfGetScaleFactor(
    handle: c_int, subrecord_id: c_int, p_c_flag, p_multiplier, p_offset
) -> int:
    """
    :param handle: c_int
    :param subrecord_id: c_int
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
    return _libgsf.gsfGetScaleFactor(
        handle, subrecord_id, p_c_flag, p_multiplier, p_offset
    )


def gsfSetDefaultScaleFactor(p_mb_ping) -> int:
    """
    :param p_mb_ping: POINTER(gsfpy3_09.gsfSwathBathyPing.c_gsfSwathBathyPing)

    :return: 0 if successful. Note that, in the event of a successful call, estimated
             scale factors for each of the beam arrays in the ping will be set.
    """
    return _libgsf.gsfSetDefaultScaleFactor(p_mb_ping)


def gsfLoadDepthScaleFactorAutoOffset(
    p_mb_ping,
    subrecord_id: c_int,
    reset: c_int,
    min_depth: c_double,
    max_depth: c_double,
    last_corrector,
    p_c_flag,
    precision: c_double,
) -> int:
    """
    :param p_mb_ping: POINTER(gsfpy3_09.gsfSwathBathyPing.c_gsfSwathBathyPing)
    :param subrecord_id: c_int
    :param reset: c_int
    :param min_depth: c_double
    :param max_depth: c_double
    :param p_c_flag: POINTER(c_uchar)
    :param precision: c_double

    :return: 0 if successful. Note that, in the event of a successful call, estimated
             scale factors for each of the beam arrays in the ping will be set.
    """
    return _libgsf.gsfLoadDepthScaleFactorAutoOffset(
        p_mb_ping,
        subrecord_id,
        reset,
        min_depth,
        max_depth,
        last_corrector,
        p_c_flag,
        precision,
    )


def gsfGetPositionDestination(gp, offsets, heading: c_double, dist_step: c_double):
    """
    :param gp: gsfpy3_09.GSF_POSTIION.c_GSF_POSITION
    :param offsets: gsfpy3_09.GSF_POSTIION_OFFSETS.c_GSF_POSITION_OFFSETS
    :param heading: c_double
    :param dist_step: c_double

    :return: POINTER(gsfpy3_09.GSF_POSITION.GSF_POSITION) - the destination position.
    """
    return _libgsf.gsfGetPositionDestination(gp, offsets, heading, dist_step)


def gsfGetPositionOffsets(gp_from, gp_to, heading: c_double, dist_step: c_double):
    """
    :param gp_from: gsfpy3_09.GSF_POSTIION.c_GSF_POSITION
    :param gp_to: gsfpy3_09.GSF_POSTIION.c_GSF_POSITION
    :param heading: c_double
    :param dist_step: c_double

    :return: POINTER(gsfpy3_09.c_GSF_POSITION_OFFSETS.c_GSF_POSITION_OFFSETS) -
             the offsets between the two given positions.
    """
    return _libgsf.gsfGetPositionOffsets(gp_from, gp_to, heading, dist_step)


def gsfTestPingStatus(ping_flags: c_ushort, usflag: c_ushort) -> bool:
    """
    :param ping_flags: c_ushort
    :param usflag: c_ushort

    :return: True if the bit within ping_flags, which corresponds to the
             bit set in usflags, is set. Otherwise False.
    """
    return bool(ping_flags.value & usflag.value)


def gsfSetPingStatus(ping_flags: c_ushort, usflag: c_ushort) -> c_ushort:
    """
    :param ping_flags: c_ushort
    :param usflag: c_ushort

    :return: c_ushort. The value of the new ping flags with the bit set in
             usflags set.
    """
    return c_ushort(ping_flags.value | usflag.value)


def gsfClearPingStatus(ping_flags: c_ushort, usflag: c_ushort) -> c_ushort:
    """
    :param ping_flags: c_ushort
    :param usflag: c_ushort

    return: c_ushort. The value of the new ping flags with the bit set in
            usflags cleared.
    """
    return c_ushort(ping_flags.value & ~usflag.value)
