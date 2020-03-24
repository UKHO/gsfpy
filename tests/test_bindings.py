import os
import tempfile
from ctypes import (
    addressof,
    byref,
    c_char,
    c_double,
    c_int,
    c_long,
    c_ubyte,
    c_ushort,
    create_string_buffer,
    pointer,
    string_at,
)
from glob import glob
from os import path

from assertpy import assert_that

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
from tests import ERROR_RET_VAL, GSF_FOPEN_ERROR, SUCCESS_RET_VAL


class TestBindings:
    def setup_method(self, method):
        self.test_data_path = path.join(
            os.fsencode(path.dirname(__file__)), b"gsfpy_test_data.gsf"
        )

    @classmethod
    def teardown_class(cls):
        print("\n")
        for gsf in glob(path.join(tempfile.gettempdir(), "*.gsf")):
            print("cleaning up, removing {0}".format(gsf))
            os.remove(gsf)

    def test_gsfOpenClose_success(self):
        """
        Open the test GSF file, then close.
        """
        # Arrange
        file_handle = c_int(0)

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfOpenBuffered_success(self):
        """
        Open the test GSF file, then close.
        """
        # Arrange
        file_handle = c_int(0)
        buf_size = 100

        # Act
        ret_val_open_buffered = gsfpy.bindings.gsfOpenBuffered(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle), buf_size
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open_buffered).is_equal_to(SUCCESS_RET_VAL)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfSeek_success(self):
        """
        Open the test GSF file, seek to end of file, then close.
        """
        # Arrange
        file_handle = c_int(0)

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        ret_val_seek = gsfpy.bindings.gsfSeek(file_handle, SeekOption.GSF_END_OF_FILE)
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(ret_val_seek).is_equal_to(SUCCESS_RET_VAL)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfError(self):
        """
        Try to open a non-existent GSF file and check that gsfError() returns the
        correct error code and error message.
        """
        # Arrange
        file_handle = c_int(0)

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            b"non-existent.gsf", FileMode.GSF_READONLY, byref(file_handle)
        )
        ret_val_int_error = gsfpy.bindings.gsfIntError()
        ret_val_string_error = gsfpy.bindings.gsfStringError()

        # Assert
        assert_that(ret_val_open).is_equal_to(ERROR_RET_VAL)
        assert_that(ret_val_int_error).is_equal_to(GSF_FOPEN_ERROR)
        assert_that(ret_val_string_error).is_equal_to(
            b"GSF Unable to open requested file"
        )

    def test_gsfRead_success(self):
        """
        Read a comment record from a GSF file.
        """
        # Arrange
        file_handle = c_int(0)
        data_id = c_gsfDataID()
        records = c_gsfRecords()

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        bytes_read = gsfpy.bindings.gsfRead(
            file_handle, RecordType.GSF_RECORD_COMMENT, byref(data_id), byref(records),
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(bytes_read).is_equal_to(168)
        assert_that(string_at(records.comment.comment)).is_equal_to(
            (
                b"Bathy converted from HIPS file: "
                b"M:\\CCOM_Processing\\CARIS_v8\\HIPS\\81\\HDCS_Data\\EX1502L2"
                b"\\Okeanos_March_2011\\2015-081\\0175_20150322_232639_EX1502L2_MB"
            )
        )

        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfWrite_success(self):
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

        tmp_gsf_file_path = path.join(os.fsencode(tempfile.gettempdir()), b"temp.gsf")

        # Act
        ret_val_open_create = gsfpy.bindings.gsfOpen(
            tmp_gsf_file_path, FileMode.GSF_CREATE, byref(file_handle)
        )
        bytes_written = gsfpy.bindings.gsfWrite(
            file_handle, byref(data_id), byref(records)
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open_create).is_equal_to(SUCCESS_RET_VAL)
        assert_that(bytes_written).is_equal_to(36)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

        # Read comment from newly created file to check it is as expected
        data_id = c_gsfDataID()
        data_id.recordID = RecordType.GSF_RECORD_COMMENT

        records = c_gsfRecords()

        ret_val_open_create = gsfpy.bindings.gsfOpen(
            tmp_gsf_file_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        gsfpy.bindings.gsfRead(
            file_handle, RecordType.GSF_RECORD_COMMENT, byref(data_id), byref(records),
        )
        gsfpy.bindings.gsfClose(file_handle)

        assert_that(string_at(records.comment.comment)).is_equal_to(comment)

    def test_gsfGetNumberRecords_success(self):
        """
        Open the test GSF file, count the number of GSF_RECORD_SWATH_BATHYMETRY_PING
        records, then close.
        """
        # Arrange
        file_handle = c_int(0)

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY_INDEX, byref(file_handle)
        )
        ret_val_count = gsfpy.bindings.gsfGetNumberRecords(
            file_handle, RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(ret_val_count).is_equal_to(4)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfIndexTime_success(self):
        """
        Open the test GSF file, get the index time and record number of the last
        multibeam ping record.
        """
        # Arrange
        file_handle = c_int(0)
        sec = c_int(-1)
        nsec = c_long(-1)

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY_INDEX, byref(file_handle)
        )
        ret_val_index_time = gsfpy.bindings.gsfIndexTime(
            file_handle,
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            -1,
            byref(sec),
            byref(nsec),
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(ret_val_index_time).is_equal_to(4)
        assert_that(sec.value).is_equal_to(1427066799)
        assert_that(nsec.value).is_equal_to(766000032)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfPercent_success(self):
        """
        Open the test GSF file, read 4 records, then retrieve the location of the file
        pointer as a percentage of the total file size.
        """
        # Arrange
        file_handle = c_int(0)
        data_id = c_gsfDataID()
        records = c_gsfRecords()

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY_INDEX, byref(file_handle)
        )
        for i in range(4):
            gsfpy.bindings.gsfRead(
                file_handle, RecordType.GSF_NEXT_RECORD, byref(data_id), byref(records)
            )
        ret_val_percent = gsfpy.bindings.gsfPercent(file_handle)
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(ret_val_percent).is_equal_to(6)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfGetSwathBathyBeamWidths_success(self):
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
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        bytes_read = gsfpy.bindings.gsfRead(
            file_handle,
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            byref(data_id),
            byref(records),
        )
        ret_val_beam_widths = gsfpy.bindings.gsfGetSwathBathyBeamWidths(
            byref(records), byref(fore_aft), byref(athwartship),
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(bytes_read).is_equal_to(6552)
        assert_that(ret_val_beam_widths).is_equal_to(SUCCESS_RET_VAL)
        assert_that(fore_aft.value).is_equal_to(1.5)
        assert_that(athwartship.value).is_equal_to(1.5)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfGetSwathBathyArrayMinMax_success(self):
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
        ping = None
        subrecordID = 1

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        bytes_read = gsfpy.bindings.gsfRead(
            file_handle,
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            byref(data_id),
            byref(records),
        )
        ping = records.mb_ping
        ret_val_min_max = gsfpy.bindings.gsfGetSwathBathyArrayMinMax(
            byref(ping), subrecordID, byref(min_value), byref(max_value),
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(bytes_read).is_equal_to(6552)
        assert_that(ret_val_min_max).is_equal_to(SUCCESS_RET_VAL)
        assert_that(min_value.value).is_equal_to(-1636.4)
        assert_that(max_value.value).is_equal_to(1640.35)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfIsStarboardPing_success(self):
        """
        Open the test GSF file, read a multibeam ping record, then find out if
        it is a starboard ping.
        """
        # Arrange
        file_handle = c_int(0)
        data_id = c_gsfDataID()
        records = c_gsfRecords()

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        bytes_read = gsfpy.bindings.gsfRead(
            file_handle,
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            byref(data_id),
            byref(records),
        )
        ret_val_stbd_ping = gsfpy.bindings.gsfIsStarboardPing(byref(records))
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(bytes_read).is_equal_to(6552)
        assert_that(ret_val_stbd_ping).is_equal_to(0)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfGetSonarTextName_success(self):
        """
        Open the test GSF file, read a multibeam ping record, then retrieve
        the name of the sonar equipment used to capture it.
        """
        # Arrange
        file_handle = c_int(0)
        data_id = c_gsfDataID()
        records = c_gsfRecords()
        ping = None

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        bytes_read = gsfpy.bindings.gsfRead(
            file_handle,
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            byref(data_id),
            byref(records),
        )
        ping = records.mb_ping
        ret_val_sonar_name = gsfpy.bindings.gsfGetSonarTextName(byref(ping))
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(bytes_read).is_equal_to(6552)
        assert_that(ret_val_sonar_name).is_equal_to(b"Kongsberg EM3002D")
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfFileSupportsRecalculateXYZ_success(self):
        """
        Open the test GSF file then discover whether it contains enough information
        for platform-relative XYZ values to be recalculated.
        """
        # Arrange
        file_handle = c_int(0)
        status = c_int(0)

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        ret_val_xyz = gsfpy.bindings.gsfFileSupportsRecalculateXYZ(
            file_handle, byref(status)
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(status.value).is_equal_to(0)
        assert_that(ret_val_xyz).is_equal_to(SUCCESS_RET_VAL)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfFileSupportsRecalculateTPU_success(self):
        """
        Open the test GSF file then discover whether it contains enough information
        for Total Propagated Uncertainty (TPU) values to be calculated.
        """
        # Arrange
        file_handle = c_int(0)
        status = c_int(0)

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        ret_val_tpu = gsfpy.bindings.gsfFileSupportsRecalculateTPU(
            file_handle, byref(status)
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(status.value).is_equal_to(1)
        assert_that(ret_val_tpu).is_equal_to(SUCCESS_RET_VAL)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfFileSupportsRecalculateNominalDepth_success(self):
        """
        Open the test GSF file then discover whether it contains enough information
        for the nominal depth array to be calculated.
        """
        # Arrange
        file_handle = c_int(0)
        status = c_int(0)

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        ret_val_nom = gsfpy.bindings.gsfFileSupportsRecalculateNominalDepth(
            file_handle, byref(status)
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(status.value).is_equal_to(1)
        assert_that(ret_val_nom).is_equal_to(SUCCESS_RET_VAL)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfFileContainsMBAmplitude_success(self):
        """
        Open the test GSF file then discover whether it contains amplitude data.
        """
        # Arrange
        file_handle = c_int(0)
        status = c_int(0)

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        ret_val_mb_amp = gsfpy.bindings.gsfFileContainsMBAmplitude(
            file_handle, byref(status)
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(status.value).is_equal_to(1)
        assert_that(ret_val_mb_amp).is_equal_to(SUCCESS_RET_VAL)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfFileContainsMBImagery_success(self):
        """
        Open the test GSF file then discover whether it contains beam imagery.
        """
        # Arrange
        file_handle = c_int(0)
        status = c_int(0)

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        ret_val_img = gsfpy.bindings.gsfFileContainsMBImagery(
            file_handle, byref(status)
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(status.value).is_equal_to(0)
        assert_that(ret_val_img).is_equal_to(SUCCESS_RET_VAL)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfFileIsNewSurveyLine_success(self):
        """
        Open the test GSF file, read a ping, then discover whether it comes
        from a new survey line.
        """
        # Arrange
        file_handle = c_int(0)
        data_id = c_gsfDataID()
        records = c_gsfRecords()
        azimuth_change = c_double(90)
        last_heading = c_double(270)

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        bytes_read = gsfpy.bindings.gsfRead(
            file_handle,
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            byref(data_id),
            byref(records),
        )
        ret_val_survey_line = gsfpy.bindings.gsfIsNewSurveyLine(
            file_handle, byref(records), azimuth_change, byref(last_heading)
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(bytes_read).is_equal_to(6552)
        assert_that(ret_val_survey_line).is_greater_than(0)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfInitializeMBParams_success(self):
        """
        Create a gsfMBParams structure and initialize all fields.
        """
        # Arrange
        mbparams = c_gsfMBParams()

        # Act
        gsfpy.bindings.gsfInitializeMBParams(byref(mbparams))

        # Assert two of the fields here to check they are set to the unknown
        # value.
        assert_that(mbparams.horizontal_datum).is_equal_to(-99)
        assert_that(mbparams.vessel_type).is_equal_to(-99)

    def test_gsfCopyRecords_success(self):
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
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        bytes_read = gsfpy.bindings.gsfRead(
            file_handle,
            RecordType.GSF_RECORD_COMMENT,
            byref(data_id),
            byref(source_records),
        )
        ret_val_cpy = gsfpy.bindings.gsfCopyRecords(
            pointer(target_records), pointer(source_records)
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(bytes_read).is_equal_to(168)
        assert_that(ret_val_cpy).is_equal_to(SUCCESS_RET_VAL)
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
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfPutMBParams_success(self):
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
        num_arrays = 1

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        ret_val_putmbparams = gsfpy.bindings.gsfPutMBParams(
            byref(mbparams), byref(records), file_handle, num_arrays
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(ret_val_putmbparams).is_equal_to(SUCCESS_RET_VAL)
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
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfGetMBParams_success(self):
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
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        ret_val_putmbparams = gsfpy.bindings.gsfPutMBParams(
            byref(mbparams_in), byref(records), file_handle, num_arrays
        )
        bytes_read = gsfpy.bindings.gsfRead(
            file_handle,
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            byref(data_id),
            byref(records),
        )
        ret_val_getmbparams = gsfpy.bindings.gsfGetMBParams(
            byref(records), byref(mbparams_out), byref(num_arrays)
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(ret_val_putmbparams).is_equal_to(SUCCESS_RET_VAL)
        assert_that(bytes_read).is_equal_to(6552)
        assert_that(ret_val_getmbparams).is_equal_to(SUCCESS_RET_VAL)
        assert_that(mbparams_out.horizontal_datum).is_equal_to(
            mbparams_in.horizontal_datum
        )
        assert_that(mbparams_out.number_of_transmitters).is_equal_to(1)
        assert_that(mbparams_out.number_of_receivers).is_equal_to(1)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfLoadScaleFactor_success(self):
        """
        Create a gsfScaleFactors structure and initialize all fields.
        """
        # Arrange
        scaleFactors = c_gsfScaleFactors()
        subrecordID = (
            ScaledSwathBathySubRecord.GSF_SWATH_BATHY_SUBRECORD_SONAR_VERT_UNCERT_ARRAY
        )
        # Save as two byte value after applying scale and offset
        c_flag = c_char(0x20)
        # 1cm precision for depth
        precision = c_double(0.01)
        offset = c_int(4)

        # Act
        ret_val_sf = gsfpy.bindings.gsfLoadScaleFactor(
            byref(scaleFactors), subrecordID, c_flag, precision, offset
        )

        # Assert
        index = subrecordID.value - 1
        assert_that(ret_val_sf).is_equal_to(SUCCESS_RET_VAL)
        assert_that(len(scaleFactors.scaleTable)).is_equal_to(
            GSF_MAX_PING_ARRAY_SUBRECORDS
        )
        assert_that(int(scaleFactors.scaleTable[index].compressionFlag)).is_equal_to(32)
        assert_that(int(scaleFactors.scaleTable[index].multiplier)).is_equal_to(
            (1 / precision.value)
        )
        assert_that(int(scaleFactors.scaleTable[index].offset)).is_equal_to(
            offset.value
        )

    def test_gsfGetScaleFactor_success(self):
        """
        Read a GSF record and get the beam array field size, compression flag,
        multiplier and DC offset applied to it.
        """
        # Arrange
        file_handle = c_int(0)
        records = c_gsfRecords()
        data_id = c_gsfDataID()
        subrecordID = (
            ScaledSwathBathySubRecord.GSF_SWATH_BATHY_SUBRECORD_MEAN_CAL_AMPLITUDE_ARRAY
        )
        c_flag = c_ubyte()
        multiplier = c_double()
        offset = c_double()

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        bytes_read = gsfpy.bindings.gsfRead(
            file_handle,
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            byref(data_id),
            byref(records),
        )
        ret_val_sf = gsfpy.bindings.gsfGetScaleFactor(
            file_handle, subrecordID, byref(c_flag), byref(multiplier), byref(offset)
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(bytes_read).is_equal_to(6552)
        assert_that(ret_val_sf).is_equal_to(SUCCESS_RET_VAL)
        assert_that(c_flag.value).is_equal_to(int(0x10))
        assert_that(multiplier.value).is_equal_to(2)
        assert_that(offset.value).is_equal_to(0)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfSetDefaultScaleFactor_success(self):
        """
        Set estimated scale factors for a gsfSwathBathyPing structure.
        """
        # Arrange
        file_handle = c_int(0)
        records = c_gsfRecords()
        data_id = c_gsfDataID()

        mb_ping = None

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        bytes_read = gsfpy.bindings.gsfRead(
            file_handle,
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            byref(data_id),
            byref(records),
        )
        # Set multibeam ping scale factors to be empty
        mb_ping = records.mb_ping
        mb_ping.scaleFactors = c_gsfScaleFactors()

        ret_val_sf = gsfpy.bindings.gsfSetDefaultScaleFactor(byref(mb_ping))
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        index = 2
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(bytes_read).is_equal_to(6552)
        assert_that(ret_val_sf).is_equal_to(SUCCESS_RET_VAL)
        assert_that(
            int(mb_ping.scaleFactors.scaleTable[index].compressionFlag)
        ).is_equal_to(0x00)
        assert_that(int(mb_ping.scaleFactors.scaleTable[index].multiplier)).is_equal_to(
            50
        )
        assert_that(int(mb_ping.scaleFactors.scaleTable[index].offset)).is_equal_to(0)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfLoadDepthScaleFactorAutoOffset_success(self):
        """
        Load scale factors for the depth subrecords of a gsfSwathBathyPing structure.
        """
        # Arrange
        file_handle = c_int(0)
        records = c_gsfRecords()
        data_id = c_gsfDataID()

        mb_ping = None

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        bytes_read = gsfpy.bindings.gsfRead(
            file_handle,
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            byref(data_id),
            byref(records),
        )
        # Set multibeam ping scale factors to be empty
        mb_ping = records.mb_ping

        ret_val_sf = gsfpy.bindings.gsfSetDefaultScaleFactor(byref(mb_ping))
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        index = 2
        assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
        assert_that(bytes_read).is_equal_to(6552)
        assert_that(ret_val_sf).is_equal_to(SUCCESS_RET_VAL)
        assert_that(
            int(mb_ping.scaleFactors.scaleTable[index].compressionFlag)
        ).is_equal_to(0x00)
        assert_that(int(mb_ping.scaleFactors.scaleTable[index].multiplier)).is_equal_to(
            50
        )
        assert_that(int(mb_ping.scaleFactors.scaleTable[index].offset)).is_equal_to(0)
        assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)

    def test_gsfGetPositionDestination(self):
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
        ret_val_pos = gsfpy.bindings.gsfGetPositionDestination(
            pos_start, offsets, heading, dist_step
        )

        # Assert
        assert_that(ret_val_pos.contents.lon).is_close_to(10.20, 0.01)
        assert_that(ret_val_pos.contents.lat).is_close_to(19.94, 0.01)
        assert_that(ret_val_pos.contents.z).is_close_to(33.0, 0.000001)

    def test_gsfGetPositionOffsets(self):
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
        ret_val_off = gsfpy.bindings.gsfGetPositionOffsets(
            pos_start, pos_end, heading, dist_step
        )

        # Assert
        assert_that(ret_val_off.contents.x).is_close_to(103965, 0.5)
        assert_that(ret_val_off.contents.y).is_close_to(221434, 0.5)
        assert_that(ret_val_off.contents.z).is_close_to(20.0, 0.000001)

    def test_gsfTestPingStatus(self):
        """
        Test the status of a ping flag.
        """
        # Arrange
        mb_ping = c_gsfSwathBathyPing()
        mb_ping.ping_flags = 0x0024

        # Act
        ret_val_status_set = gsfpy.bindings.gsfTestPingStatus(
            c_ushort(mb_ping.ping_flags), c_ushort(PingFlag.GSF_PING_USER_FLAG_05)
        )
        ret_val_status_unset = gsfpy.bindings.gsfTestPingStatus(
            c_ushort(mb_ping.ping_flags), c_ushort(PingFlag.GSF_PING_USER_FLAG_15)
        )

        # Assert
        assert_that(ret_val_status_set).is_equal_to(True)
        assert_that(ret_val_status_unset).is_equal_to(False)

    def test_gsfSetPingStatus(self):
        """
        Set the status of a ping flag.
        """
        # Arrange
        mb_ping = c_gsfSwathBathyPing()
        mb_ping.ping_flags = 0x0024

        # Act
        ret_val_status_set = gsfpy.bindings.gsfSetPingStatus(
            c_ushort(mb_ping.ping_flags), c_ushort(PingFlag.GSF_PING_USER_FLAG_15)
        )

        # Assert
        assert_that(ret_val_status_set.value).is_equal_to(0x8024)

    def test_gsfClearPingStatus(self):
        """
        Clear the status of a ping flag.
        """
        # Arrange
        mb_ping = c_gsfSwathBathyPing()
        mb_ping.ping_flags = 0x0024

        # Act
        ret_val_status_clear = gsfpy.bindings.gsfClearPingStatus(
            c_ushort(mb_ping.ping_flags), c_ushort(PingFlag.GSF_PING_USER_FLAG_02)
        )

        # Assert
        assert_that(ret_val_status_clear.value).is_equal_to(0x0020)

    # TODO - See gsfpy issue #50
    # def test_gsfFree_success(self):
    #     """
    #     Read a gsf record, then free the memory.
    #     """
    #     # Arrange
    #     file_handle = c_int(0)
    #     data_id = c_gsfDataID()
    #     records = c_gsfRecords()

    #     # Act
    #     ret_val_open = gsfpy.bindings.gsfOpen(
    #         self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
    #     )
    #     bytes_read = gsfpy.bindings.gsfRead(
    #         file_handle,
    #         RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
    #         byref(data_id),
    #         byref(records),
    #     )
    #     gsfpy.bindings.gsfFree(byref(records))
    #     ret_val_close = gsfpy.bindings.gsfClose(file_handle)

    #     # Assert
    #     assert_that(ret_val_open).is_equal_to(SUCCESS_RET_VAL)
    #     assert_that(bytes_read).is_equal_to(6552)
    #     assert_that(records).is_none()
    #     assert_that(ret_val_close).is_equal_to(SUCCESS_RET_VAL)
