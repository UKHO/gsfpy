import os
import tempfile
from ctypes import c_int, create_string_buffer, string_at
from glob import glob
from os import path

from assertpy import assert_that

from gsfpy import GsfException, open_gsf
from gsfpy.enums import FileMode, RecordType, SeekOption
from gsfpy.gsfRecords import c_gsfRecords
from tests import GSF_FOPEN_ERROR


class TestGsfpy:
    def setup_method(self, method):
        self.test_data_path = path.join(path.dirname(__file__), "gsfpy_test_data.gsf")

    @classmethod
    def teardown_class(cls):
        print("\n")
        for gsf in glob(path.join(tempfile.gettempdir(), "*.gsf")):
            print("cleaning up, removing {0}".format(gsf))
            os.remove(gsf)

    def test_open_gsf_success(self):
        """
        Open the test GSF file, then close.
        """
        # Act
        gsf_file = open_gsf(self.test_data_path)
        gsf_file.close()

    def test_open_gsf_buffered_success(self):
        """
        Open the test GSF file in buffered mode, then close.
        """
        # Act
        gsf_file = open_gsf(self.test_data_path, buffer_size=100)
        gsf_file.close()

    def test_seek_success(self):
        """
        Open the test GSF file, seek to end of file, then close.
        """
        # Act
        gsf_file = open_gsf(self.test_data_path)
        gsf_file.seek(SeekOption.GSF_END_OF_FILE)
        gsf_file.close()

    def test_GsfException(self):
        """
        Try to open a non-existent GSF file, ensure a GsfException is raised and check
        that it contains the correct error code and error message.
        """
        # Assert
        assert_that(open_gsf).raises(GsfException).when_called_with(
            "non-existent.gsf"
        ).is_equal_to(f"[{GSF_FOPEN_ERROR}] GSF Unable to open requested file")

    def test_read_success(self):
        """
        Read a comment record from a GSF file.
        """
        # Act
        gsf_file = open_gsf(self.test_data_path)
        _, record = gsf_file.read(RecordType.GSF_RECORD_COMMENT)
        gsf_file.close()

        # Assert
        assert_that(string_at(record.comment.comment)).is_equal_to(
            (
                b"Bathy converted from HIPS file: "
                b"M:\\CCOM_Processing\\CARIS_v8\\HIPS\\81\\HDCS_Data\\EX1502L2"
                b"\\Okeanos_March_2011\\2015-081\\0175_20150322_232639_EX1502L2_MB"
            )
        )

    def test_write_success(self):
        """
        Write a single comment record to a new GSF file
        """
        # Arrange
        tmp_gsf_file_path = path.join(tempfile.gettempdir(), "temp.gsf")

        comment = b"My first comment"
        # Act
        gsf_file = open_gsf(tmp_gsf_file_path, mode=FileMode.GSF_CREATE)
        gsf_file.write(_new_comment_record(comment), RecordType.GSF_RECORD_COMMENT)
        gsf_file.close()

        # Assert
        # Read comment from newly created file to check it is as expected
        gsf_file = open_gsf(tmp_gsf_file_path)
        data_id, record = gsf_file.read(RecordType.GSF_RECORD_COMMENT)
        gsf_file.close()

        assert_that(string_at(record.comment.comment)).is_equal_to(comment)

    def test_direct_access_write_and_read_success(self):
        """
        Create, update and read. First sequentially, then using direct access
        """
        tmp_gsf_file_path = path.join(tempfile.gettempdir(), "temp.gsf")

        # Create a file with 3 records
        comment_1 = b"Comment #1"
        comment_2 = b"Comment #2"
        comment_3 = b"Comment #3"
        comment_4 = b"Comment #4"

        # Write sequentially
        gsf_file = open_gsf(tmp_gsf_file_path, mode=FileMode.GSF_CREATE)
        gsf_file.write(_new_comment_record(comment_1), RecordType.GSF_RECORD_COMMENT)
        gsf_file.write(_new_comment_record(comment_2), RecordType.GSF_RECORD_COMMENT)
        gsf_file.write(_new_comment_record(comment_3), RecordType.GSF_RECORD_COMMENT)
        gsf_file.close()

        # Update using direct access
        gsf_file = open_gsf(tmp_gsf_file_path, mode=FileMode.GSF_UPDATE_INDEX)
        gsf_file.write(_new_comment_record(comment_4), RecordType.GSF_RECORD_COMMENT, 2)
        gsf_file.close()

        # Read sequentially
        gsf_file = open_gsf(tmp_gsf_file_path)

        _, record_1 = gsf_file.read()
        assert_that(string_at(record_1.comment.comment)).is_equal_to(comment_1)

        _, record_2 = gsf_file.read()
        assert_that(string_at(record_2.comment.comment)).is_equal_to(comment_4)

        _, record_3 = gsf_file.read()
        assert_that(string_at(record_3.comment.comment)).is_equal_to(comment_3)

        assert_that(gsf_file.read).raises(GsfException).when_called_with().is_equal_to(
            "[-23] GSF End of File Encountered"
        )

        # Read using direct access
        gsf_file = open_gsf(tmp_gsf_file_path, mode=FileMode.GSF_READONLY_INDEX)

        _, direct_access_record = gsf_file.read(RecordType.GSF_RECORD_COMMENT, 2)
        assert_that(string_at(direct_access_record.comment.comment)).is_equal_to(
            comment_4
        )

        gsf_file.close()

    def test_get_number_records_success(self):
        """
        Open the test GSF file in GSF_READONLY_INDEX mode, count the number of
        GSF_RECORD_SWATH_BATHYMETRY_PING records, then close.
        """
        # Act
        gsf_file = open_gsf(self.test_data_path, FileMode.GSF_READONLY_INDEX)
        number_of_pings = gsf_file.get_number_records(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
        )
        gsf_file.close()

        assert_that(number_of_pings).is_equal_to(4)

    def test_get_number_records_failure(self):
        """
        Open the test GSF file in GSF_READONLY mode, attempt to count the number of
        GSF_RECORD_SWATH_BATHYMETRY_PING records and verify the exception.
        """
        # Act
        gsf_file = open_gsf(self.test_data_path)

        assert_that(gsf_file.get_number_records).raises(GsfException).when_called_with(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
        ).is_equal_to("[-3] GSF Error illegal access mode")

        gsf_file.close()


def _new_comment_record(comment: bytes) -> c_gsfRecords:
    record = c_gsfRecords()
    record.comment.comment_time.tvsec = c_int(1000)
    record.comment.comment_length = c_int(len(comment))
    record.comment.comment = create_string_buffer(comment)
    return record
