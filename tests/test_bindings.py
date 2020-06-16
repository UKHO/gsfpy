import os
from ctypes import (
    addressof,
    byref,
    c_char,
    c_double,
    c_int,
    c_long,
    c_longlong,
    c_ubyte,
    c_ushort,
    create_string_buffer,
    pointer,
    string_at,
)

from assertpy import assert_that, soft_assertions

import gsfpy.bindings
import gsfpy.enums
from gsfpy.constants import GSF_MAX_PING_ARRAY_SUBRECORDS
from gsfpy.enums import (
    FileMode,
    PingFlag,
    RecordType,
    ScaledSwathBathySubRecord,
    SeekOption,
)
from gsfpy.GSF_POSITION import c_GSF_POSITION
from gsfpy.GSF_POSITION_OFFSETS import c_GSF_POSITION_OFFSETS
from gsfpy.gsfDataID import c_gsfDataID
from gsfpy.gsfMBParams import c_gsfMBParams
from gsfpy.gsfRecords import c_gsfRecords
from gsfpy.gsfScaleFactors import c_gsfScaleFactors
from gsfpy.gsfSwathBathyPing import c_gsfSwathBathyPing


def test_gsfOpenClose_success(gsf_test_data_03_06):
    """
    Open the test GSF file, then close.
    """
    file_handle = c_int(0)

    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()


def test_gsfOpenBuffered_success(gsf_test_data_03_06):
    """
    Open the test GSF file, then close.
    """
    file_handle = c_int(0)
    buf_size = 100

    return_value = gsfpy.bindings.gsfOpenBuffered(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
        buf_size,
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()


def test_gsfSeek_success(gsf_test_data_03_06):
    """
    Open the test GSF file, seek to end of file, then close.
    """
    file_handle = c_int(0)

    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfSeek(file_handle, SeekOption.GSF_END_OF_FILE)
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()


def test_gsfError_non_existent_file(gsf_test_data_03_06):
    """
    Try to open a non-existent GSF file and check that gsfError() returns the
    correct error code and error message.
    """
    file_handle = c_int(0)

    return_value = gsfpy.bindings.gsfOpen(
        b"non-existent.gsf", FileMode.GSF_READONLY, byref(file_handle)
    )
    assert_that(return_value).is_not_zero()

    with soft_assertions():
        return_value = gsfpy.bindings.gsfIntError()
        assert_that(return_value).described_as(
            "Error code for 'GSF Unable to open requested file'"
        ).is_equal_to(-1)

        string_error = gsfpy.bindings.gsfStringError()
        assert_that(string_error).is_equal_to(b"GSF Unable to open requested file")


def test_gsfError_operation_in_wrong_file_mode(gsf_test_data_03_06):
    """
    Open a GSF file, try to get the number of GSF  and check that gsfError() returns the
    correct error code and error message.
    """
    file_handle = c_int(0)

    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfGetNumberRecords(
        file_handle, RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
    )
    assert_that(return_value).is_not_zero()

    with soft_assertions():
        return_value = gsfpy.bindings.gsfIntError()
        assert_that(return_value).described_as(
            "Error code for 'GSF Error illegal access mode'"
        ).is_equal_to(-3)

        string_error = gsfpy.bindings.gsfStringError()
        assert_that(string_error).is_equal_to(b"GSF Error illegal access mode")


def test_gsfRead_success(gsf_test_data_03_06):
    """
    Read a comment record from a GSF file.
    """
    file_handle = c_int(0)
    data_id = c_gsfDataID()
    records = c_gsfRecords()

    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy.bindings.gsfRead(
        file_handle, RecordType.GSF_RECORD_COMMENT, byref(data_id), byref(records),
    )
    assert_that(bytes_read).is_equal_to(156)

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    assert_that(string_at(records.comment.comment)).is_equal_to(
        (
            b"Bathy converted from HIPS file: "
            b"M:\\CCOM_Processing\\CARIS_v9\\HIPS\\HDCS_Data\\EX1604"
            b"\\Okeanos_2016\\2016-083\\0029_20160323_185603_EX1604_MB"
        )
    )


def test_gsfWrite_success(tmp_path):
    """
    Write a single comment record to a new GSF file
    """
    # Arrange
    file_handle = c_int(0)

    data_id = c_gsfDataID()
    data_id.recordID = RecordType.GSF_RECORD_COMMENT

    comment = b"My first comment"
    records = c_gsfRecords()
    records.comment.comment_time.tvsec = c_int(1000)
    records.comment.comment_length = c_int(len(comment))
    records.comment.comment = create_string_buffer(comment)

    record_size = 36  # bytes

    tmp_gsf_file_path = os.fsencode(str(tmp_path / "temp.gsf"))

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        tmp_gsf_file_path, FileMode.GSF_CREATE, byref(file_handle)
    )
    assert_that(return_value).is_zero()

    bytes_written = gsfpy.bindings.gsfWrite(file_handle, byref(data_id), byref(records))
    assert_that(bytes_written).is_equal_to(record_size)

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Read comment from newly created file to check it is as expected
    data_id = c_gsfDataID()
    data_id.recordID = RecordType.GSF_RECORD_COMMENT

    records = c_gsfRecords()

    return_value = gsfpy.bindings.gsfOpen(
        tmp_gsf_file_path, FileMode.GSF_READONLY, byref(file_handle)
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy.bindings.gsfRead(
        file_handle, RecordType.GSF_RECORD_COMMENT, byref(data_id), byref(records),
    )
    assert_that(bytes_read).is_equal_to(record_size)

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    assert_that(string_at(records.comment.comment)).is_equal_to(comment)


def test_gsfGetNumberRecords_success(gsf_test_data_03_06):
    """
    Open the test GSF file, count the number of GSF_RECORD_SWATH_BATHYMETRY_PING
    records, then close.
    """
    file_handle = c_int(0)

    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY_INDEX,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    number_of_records = gsfpy.bindings.gsfGetNumberRecords(
        file_handle, RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
    )
    assert_that(number_of_records).is_equal_to(8)

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()


def test_gsfIndexTime_success(gsf_test_data_03_06):
    """
    Open the test GSF file, get the index time and record number of the last
    multibeam ping record.
    """
    file_handle = c_int(0)
    sec = c_int(-1)
    nsec = c_long(-1)

    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY_INDEX,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    index_time = gsfpy.bindings.gsfIndexTime(
        file_handle,
        RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
        c_int(-1),
        byref(sec),
        byref(nsec),
    )

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    with soft_assertions():
        assert_that(index_time).is_equal_to(8)
        assert_that(sec.value).is_equal_to(1458759418)
        assert_that(nsec.value).is_equal_to(332999944)


def test_gsfPercent_success(gsf_test_data_03_06):
    """
    Open the test GSF file, read 4 records, then retrieve the location of the file
    pointer as a percentage of the total file size.
    """
    # Arrange
    file_handle = c_int(0)
    data_id = c_gsfDataID()
    records = c_gsfRecords()

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY_INDEX,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    for i in range(4):
        gsfpy.bindings.gsfRead(
            file_handle, RecordType.GSF_NEXT_RECORD, byref(data_id), byref(records)
        )

    percent = gsfpy.bindings.gsfPercent(file_handle)
    assert_that(percent).is_equal_to(4)

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()


def test_gsfGetSwathBathyBeamWidths_success(gsf_test_data_03_06):
    """
    Open the test GSF file, read a multibeam ping record, then get fore-aft and
    port-starboard beam widths, in degrees, for the given ping.
    """
    # Arrange
    file_handle = c_int(0)
    data_id = c_gsfDataID()
    records = c_gsfRecords()
    fore_aft = c_double()
    athwartship = c_double()

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy.bindings.gsfRead(
        file_handle,
        RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
        byref(data_id),
        byref(records),
    )
    assert_that(bytes_read).is_equal_to(6116)

    return_value = gsfpy.bindings.gsfGetSwathBathyBeamWidths(
        byref(records), byref(fore_aft), byref(athwartship),
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    with soft_assertions():
        assert_that(fore_aft.value).is_equal_to(1.5)
        assert_that(athwartship.value).is_equal_to(1.5)


def test_gsfGetSwathBathyArrayMinMax_success(gsf_test_data_03_06):
    """
    Open the test GSF file, read a multibeam ping record, then get min and
    max supportable values for the swath bathymetry arrays in the given ping.
    """
    # Arrange
    file_handle = c_int(0)
    data_id = c_gsfDataID()
    records = c_gsfRecords()
    min_value = c_double()
    max_value = c_double()
    subrecord_id = c_int(1)

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy.bindings.gsfRead(
        file_handle,
        RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
        byref(data_id),
        byref(records),
    )
    assert_that(bytes_read).is_equal_to(6116)

    return_value = gsfpy.bindings.gsfGetSwathBathyArrayMinMax(
        byref(records.mb_ping), subrecord_id, byref(min_value), byref(max_value),
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    with soft_assertions():
        assert_that(min_value.value).is_equal_to(3562.32)
        assert_that(max_value.value).is_equal_to(4217.67)


def test_gsfIsStarboardPing_success(gsf_test_data_03_06):
    """
    Open the test GSF file, read a multibeam ping record, then find out if
    it is a starboard ping.
    """
    # Arrange
    file_handle = c_int(0)
    data_id = c_gsfDataID()
    records = c_gsfRecords()

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy.bindings.gsfRead(
        file_handle,
        RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
        byref(data_id),
        byref(records),
    )
    assert_that(bytes_read).is_equal_to(6116)

    is_starboard_ping: int = gsfpy.bindings.gsfIsStarboardPing(byref(records))

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    assert_that(is_starboard_ping).is_false()


def test_gsfGetSonarTextName_success(gsf_test_data_03_06):
    """
    Open the test GSF file, read a multibeam ping record, then retrieve
    the name of the sonar equipment used to capture it.
    """
    # Arrange
    file_handle = c_int(0)
    data_id = c_gsfDataID()
    records = c_gsfRecords()

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy.bindings.gsfRead(
        file_handle,
        RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
        byref(data_id),
        byref(records),
    )
    assert_that(bytes_read).is_equal_to(6116)

    sonar_text_name = gsfpy.bindings.gsfGetSonarTextName(byref(records.mb_ping))

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    assert_that(sonar_text_name).is_equal_to("Kongsberg EM3002D")


def test_gsfFileSupportsRecalculateXYZ_success(gsf_test_data_03_06):
    """
    Open the test GSF file then discover whether it contains enough information
    for platform-relative XYZ values to be recalculated.
    """
    # Arrange
    file_handle = c_int(0)
    status = c_int(0)

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfFileSupportsRecalculateXYZ(
        file_handle, byref(status)
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    assert_that(status.value).is_false()


def test_gsfFileSupportsRecalculateTPU_success(gsf_test_data_03_06):
    """
    Open the test GSF file then discover whether it contains enough information
    for Total Propagated Uncertainty (TPU) values to be calculated.
    """
    # Arrange
    file_handle = c_int(0)
    status = c_int(0)

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfFileSupportsRecalculateTPU(
        file_handle, byref(status)
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    assert_that(status.value).is_equal_to(1)


def test_gsfFileSupportsRecalculateNominalDepth_success(gsf_test_data_03_06):
    """
    Open the test GSF file then discover whether it contains enough information
    for the nominal depth array to be calculated.
    """
    # Arrange
    file_handle = c_int(0)
    status = c_int(0)

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfFileSupportsRecalculateNominalDepth(
        file_handle, byref(status)
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    assert_that(status.value).is_equal_to(1)


def test_gsfFileContainsMBAmplitude_success(gsf_test_data_03_06):
    """
    Open the test GSF file then discover whether it contains amplitude data.
    """
    # Arrange
    file_handle = c_int(0)
    status = c_int(0)

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfFileContainsMBAmplitude(file_handle, byref(status))
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    assert_that(status.value).is_equal_to(0)


def test_gsfFileContainsMBImagery_success(gsf_test_data_03_06):
    """
    Open the test GSF file then discover whether it contains beam imagery.
    """
    # Arrange
    file_handle = c_int(0)
    status = c_int(0)

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfFileContainsMBImagery(file_handle, byref(status))
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    assert_that(status.value).is_equal_to(0)


def test_gsfFileIsNewSurveyLine_success(gsf_test_data_03_06):
    """
    Open the test GSF file, read a ping, then discover whether it comes
    from a new survey line.
    """
    # Arrange
    file_handle = c_int(0)
    data_id = c_gsfDataID()
    records = c_gsfRecords()
    azimuth_change = c_double(90)
    last_heading = c_double(180)

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy.bindings.gsfRead(
        file_handle,
        RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
        byref(data_id),
        byref(records),
    )
    assert_that(bytes_read).is_equal_to(6116)

    is_new_survey_line: int = gsfpy.bindings.gsfIsNewSurveyLine(
        file_handle, byref(records), azimuth_change, byref(last_heading)
    )

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    assert_that(is_new_survey_line).is_true()


def test_gsfInitializeMBParams_success(gsf_test_data_03_06):
    """
    Create a gsfMBParams structure and initialize all fields.
    """
    # Arrange
    mbparams = c_gsfMBParams()

    # Act
    gsfpy.bindings.gsfInitializeMBParams(byref(mbparams))

    # Assert two of the fields here to check they are set to the unknown
    # value.
    with soft_assertions():
        assert_that(mbparams.horizontal_datum).is_equal_to(-99)
        assert_that(mbparams.vessel_type).is_equal_to(-99)


def test_gsfCopyRecords_success(gsf_test_data_03_06):
    """
    Open the test GSF file, read a record, then copy the contents to
    a new gsfRecords structure.
    """
    # Arrange
    file_handle = c_int(0)
    data_id = c_gsfDataID()
    source_records = c_gsfRecords()
    target_records = c_gsfRecords()

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy.bindings.gsfRead(
        file_handle,
        RecordType.GSF_RECORD_COMMENT,
        byref(data_id),
        byref(source_records),
    )
    assert_that(bytes_read).is_equal_to(156)

    return_value = gsfpy.bindings.gsfCopyRecords(
        pointer(target_records), pointer(source_records)
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    with soft_assertions():
        assert_that(target_records.comment.comment_time.tv_sec).is_equal_to(
            source_records.comment.comment_time.tv_sec
        )
        assert_that(target_records.comment.comment_time.tv_nsec).is_equal_to(
            source_records.comment.comment_time.tv_nsec
        )
        assert_that(target_records.comment.comment_length).is_equal_to(
            source_records.comment.comment_length
        )
        assert_that(addressof(target_records.comment.comment)).is_not_equal_to(
            addressof(source_records.comment.comment)
        )
        assert_that(string_at(target_records.comment.comment)).is_equal_to(
            string_at(source_records.comment.comment)
        )


def test_gsfPutMBParams_success(gsf_test_data_03_06):
    """
    Create a gsfMBParams structure and copy fields to a gsfRecords
    structure.
    """
    # Arrange
    mbparams = c_gsfMBParams()
    gsfpy.bindings.gsfInitializeMBParams(byref(mbparams))

    # Only WGS-84 (57) and NAD-83 (38) horizontal datum values are
    # supported by GSF - see gsf.h
    mbparams.horizontal_datum = c_int(57)
    # Set number_of_transmitters and number_of_receivers to zero
    # so that num_arrays param is used for these values when
    # setting the params in the gsfRecords structure.
    mbparams.number_of_transmitters = c_int(0)
    mbparams.number_of_receivers = c_int(0)
    mbparams.to_apply.position_x_offset = c_double(1.1)
    mbparams.to_apply.position_y_offset = c_double(2.2)
    mbparams.to_apply.position_z_offset = c_double(3.3)
    mbparams.applied.position_x_offset = c_double(4.4)
    mbparams.applied.position_y_offset = c_double(5.5)
    mbparams.applied.position_z_offset = c_double(6.6)

    records = c_gsfRecords()
    # data_id = c_gsfDataID()

    file_handle = c_int(0)
    num_arrays = c_int(1)

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfPutMBParams(
        byref(mbparams), byref(records), file_handle, num_arrays
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    with soft_assertions():
        assert_that(records.process_parameters.number_parameters).is_equal_to(63)
        # param zero is always epoch start time
        assert_that(string_at(records.process_parameters.param[0])).is_equal_to(
            b"REFERENCE TIME=1970/001 00:00:00"
        )
        # params 7 (NUMBER_OF_RECEIVERS) & 8 (NUMBER_OF_TRANSMITTERS) should have
        # a value equal to num_arrays
        assert_that(string_at(records.process_parameters.param[7])).is_equal_to(
            b"NUMBER_OF_RECEIVERS=1"
        )
        assert_that(string_at(records.process_parameters.param[8])).is_equal_to(
            b"NUMBER_OF_TRANSMITTERS=1"
        )
        # param 9 (DEPTH_CALCULATION) should have a value of 'UNKNOWN' as it
        # has not been updated since being initialized
        assert_that(string_at(records.process_parameters.param[9])).is_equal_to(
            b"DEPTH_CALCULATION=UNKNOWN"
        )
        # param 19 (POSITION_OFFSET_TO_APPLY) should have values x,y,z equal to
        # corresponding values in mbparams.to_apply
        assert_that(string_at(records.process_parameters.param[19])).is_equal_to(
            b"POSITION_OFFSET_TO_APPLY=+01.10,+02.20,+03.30"
        )
        # param 42 (APPLIED_POSITION_OFFSET) should have values x,y,z equal to
        # corresponding values in mbparams.to_apply
        assert_that(string_at(records.process_parameters.param[42])).is_equal_to(
            b"APPLIED_POSITION_OFFSET=+04.40,+05.50,+06.60"
        )
        # param 61 (GEOID) should have a value equal to WGS-84, corresponding to
        # mbparams.horizontal_datum value of 57
        assert_that(string_at(records.process_parameters.param[61])).is_equal_to(
            b"GEOID=WGS-84"
        )


def test_gsfGetMBParams_success(gsf_test_data_03_06):
    """
    Set MB params, read a GSF record and copy fields to a gsfMBParams
    structure.
    """
    # Arrange
    mbparams_in = c_gsfMBParams()
    gsfpy.bindings.gsfInitializeMBParams(byref(mbparams_in))
    mbparams_in.horizontal_datum = c_int(57)

    mbparams_out = c_gsfMBParams()
    gsfpy.bindings.gsfInitializeMBParams(byref(mbparams_out))

    records = c_gsfRecords()
    data_id = c_gsfDataID()

    file_handle = c_int(0)
    num_arrays = c_int(1)

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfPutMBParams(
        byref(mbparams_in), byref(records), file_handle, num_arrays
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy.bindings.gsfRead(
        file_handle,
        RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
        byref(data_id),
        byref(records),
    )
    assert_that(bytes_read).is_equal_to(6116)

    return_value = gsfpy.bindings.gsfGetMBParams(
        byref(records), byref(mbparams_out), byref(num_arrays)
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    with soft_assertions():
        assert_that(mbparams_out.horizontal_datum).is_equal_to(
            mbparams_in.horizontal_datum
        )
        assert_that(mbparams_out.number_of_transmitters).is_equal_to(1)
        assert_that(mbparams_out.number_of_receivers).is_equal_to(1)


def test_gsfStat_success(gsf_test_data_03_06):
    """
    Get the size in bytes of a GSF file.
    """
    # Arrange
    sz = c_longlong(0)

    # Act
    return_value = gsfpy.bindings.gsfStat(
        os.fsencode(str(gsf_test_data_03_06.path)), byref(sz)
    )
    assert_that(return_value).is_zero()

    # Assert
    assert_that(sz.value).is_equal_to(165292)


def test_gsfLoadScaleFactor_success(gsf_test_data_03_06):
    """
    Create a gsfScaleFactors structure and initialize all fields.
    """
    # Arrange
    scaleFactors = c_gsfScaleFactors()
    subrecord_id = (
        ScaledSwathBathySubRecord.GSF_SWATH_BATHY_SUBRECORD_SONAR_VERT_UNCERT_ARRAY
    )
    # Save as two byte value after applying scale and offset
    c_flag = c_char(0x20)
    # 1cm precision for depth
    precision = c_double(0.01)
    offset = c_int(4)

    # Act
    return_value = gsfpy.bindings.gsfLoadScaleFactor(
        byref(scaleFactors), subrecord_id, c_flag, precision, offset
    )
    assert_that(return_value).is_zero()

    # Assert
    with soft_assertions():
        index = subrecord_id.value - 1
        assert_that(len(scaleFactors.scaleTable)).is_equal_to(
            GSF_MAX_PING_ARRAY_SUBRECORDS
        )
        assert_that(int(scaleFactors.scaleTable[index].compressionFlag)).is_equal_to(32)
        assert_that(int(scaleFactors.scaleTable[index].multiplier)).is_equal_to(
            1 / precision.value
        )
        assert_that(int(scaleFactors.scaleTable[index].offset)).is_equal_to(
            offset.value
        )


def test_gsfGetScaleFactor_success(gsf_test_data_03_06):
    """
    Read a GSF record and get the beam array field size, compression flag,
    multiplier and DC offset applied to it.
    """
    # Arrange
    file_handle = c_int(0)
    records = c_gsfRecords()
    data_id = c_gsfDataID()
    subrecord_id = (
        ScaledSwathBathySubRecord.GSF_SWATH_BATHY_SUBRECORD_MEAN_CAL_AMPLITUDE_ARRAY
    )

    c_flag = c_ubyte()
    multiplier = c_double()
    offset = c_double()

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy.bindings.gsfRead(
        file_handle,
        RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
        byref(data_id),
        byref(records),
    )
    assert_that(bytes_read).is_equal_to(6116)

    return_value = gsfpy.bindings.gsfGetScaleFactor(
        file_handle, subrecord_id, byref(c_flag), byref(multiplier), byref(offset)
    )
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    with soft_assertions():
        assert_that(c_flag.value).is_equal_to(0)
        assert_that(multiplier.value).is_equal_to(2)
        assert_that(offset.value).is_equal_to(0)


def test_gsfSetDefaultScaleFactor_success(gsf_test_data_03_06):
    """
    Set estimated scale factors for a gsfSwathBathyPing structure.
    """
    # Arrange
    file_handle = c_int(0)
    records = c_gsfRecords()
    data_id = c_gsfDataID()

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy.bindings.gsfRead(
        file_handle,
        RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
        byref(data_id),
        byref(records),
    )
    assert_that(bytes_read).is_equal_to(6116)

    # Set multibeam ping scale factors to be empty
    records.mb_ping.scaleFactors = c_gsfScaleFactors()

    return_value = gsfpy.bindings.gsfSetDefaultScaleFactor(byref(records.mb_ping))
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    with soft_assertions():
        index = 2
        assert_that(
            records.mb_ping.scaleFactors.scaleTable[index].compressionFlag
        ).is_equal_to(0x00)
        assert_that(
            records.mb_ping.scaleFactors.scaleTable[index].multiplier
        ).is_equal_to(25)
        assert_that(records.mb_ping.scaleFactors.scaleTable[index].offset).is_equal_to(
            0
        )


def test_gsfLoadDepthScaleFactorAutoOffset_success(gsf_test_data_03_06):
    """
    Load scale factors for the depth subrecords of a gsfSwathBathyPing structure.
    """
    # Arrange
    file_handle = c_int(0)
    records = c_gsfRecords()
    data_id = c_gsfDataID()

    # Act
    return_value = gsfpy.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_06.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy.bindings.gsfRead(
        file_handle,
        RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
        byref(data_id),
        byref(records),
    )
    assert_that(bytes_read).is_equal_to(6116)

    # Set multibeam ping scale factors to be empty
    return_value = gsfpy.bindings.gsfSetDefaultScaleFactor(byref(records.mb_ping))
    assert_that(return_value).is_zero()

    return_value = gsfpy.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Assert
    with soft_assertions():
        index = 2
        assert_that(
            records.mb_ping.scaleFactors.scaleTable[index].compressionFlag
        ).is_equal_to(0x00)
        assert_that(
            records.mb_ping.scaleFactors.scaleTable[index].multiplier
        ).is_equal_to(25)
        assert_that(records.mb_ping.scaleFactors.scaleTable[index].offset).is_equal_to(
            0
        )


def test_gsfGetPositionDestination(gsf_test_data_03_06):
    """
    Get a destination position (in degrees) given a starting position (in degrees)
    and a set of offsets (in m).
    """
    # Arrange
    pos_start = c_GSF_POSITION()
    pos_start.lon = c_double(10.0)
    pos_start.lat = c_double(20.0)
    pos_start.z = c_double(30.0)

    offsets = c_GSF_POSITION_OFFSETS()
    offsets.x = c_double(10000.0)
    offsets.y = c_double(20000.0)
    offsets.z = c_double(3.0)

    heading = c_double(45.0)
    dist_step = c_double(1)

    # Act
    position_destination = gsfpy.bindings.gsfGetPositionDestination(
        pos_start, offsets, heading, dist_step
    )

    # Assert
    with soft_assertions():
        assert_that(position_destination.contents.lon).is_close_to(10.20, 0.01)
        assert_that(position_destination.contents.lat).is_close_to(19.94, 0.01)
        assert_that(position_destination.contents.z).is_close_to(33.0, 0.000001)


def test_gsfGetPositionOffsets(gsf_test_data_03_06):
    """
    Get offsets (in m) between given a starting position and a destination
    position (measured in degrees).
    """
    # Arrange
    pos_start = c_GSF_POSITION()
    pos_start.lon = c_double(10.0)
    pos_start.lat = c_double(20.0)
    pos_start.z = c_double(30.0)

    pos_end = c_GSF_POSITION()
    pos_end.lon = c_double(9.0)
    pos_end.lat = c_double(22.0)
    pos_end.z = c_double(40.0)

    heading = c_double(90.0)
    dist_step = c_double(1)

    # Act
    position_offsets = gsfpy.bindings.gsfGetPositionOffsets(
        pos_start, pos_end, heading, dist_step
    )

    # Assert
    with soft_assertions():
        assert_that(position_offsets.contents.x).is_close_to(103965, 0.5)
        assert_that(position_offsets.contents.y).is_close_to(221434, 0.5)
        assert_that(position_offsets.contents.z).is_close_to(20.0, 0.000001)


def test_gsfTestPingStatus(gsf_test_data_03_06):
    """
    Test the status of a ping flag.
    """
    # Arrange
    mb_ping = c_gsfSwathBathyPing()
    mb_ping.ping_flags = 0x0024

    # Act
    set_ping_status = gsfpy.bindings.gsfTestPingStatus(
        c_ushort(mb_ping.ping_flags), c_ushort(PingFlag.GSF_PING_USER_FLAG_05)
    )
    unset_ping_status = gsfpy.bindings.gsfTestPingStatus(
        c_ushort(mb_ping.ping_flags), c_ushort(PingFlag.GSF_PING_USER_FLAG_15)
    )

    # Assert
    assert_that(set_ping_status).is_true()
    assert_that(unset_ping_status).is_false()


def test_gsfSetPingStatus(gsf_test_data_03_06):
    """
    Set the status of a ping flag.
    """
    # Arrange
    mb_ping = c_gsfSwathBathyPing()
    mb_ping.ping_flags = 0x0024

    # Act
    new_ping_status = gsfpy.bindings.gsfSetPingStatus(
        c_ushort(mb_ping.ping_flags), c_ushort(PingFlag.GSF_PING_USER_FLAG_15)
    )

    # Assert
    assert_that(new_ping_status.value).is_equal_to(0x8024)


def test_gsfClearPingStatus(gsf_test_data_03_06):
    """
    Clear the status of a ping flag.
    """
    # Arrange
    mb_ping = c_gsfSwathBathyPing()
    mb_ping.ping_flags = 0x0024

    # Act
    new_ping_status = gsfpy.bindings.gsfClearPingStatus(
        c_ushort(mb_ping.ping_flags), c_ushort(PingFlag.GSF_PING_USER_FLAG_02)
    )

    # Assert
    assert_that(new_ping_status.value).is_equal_to(0x0020)
