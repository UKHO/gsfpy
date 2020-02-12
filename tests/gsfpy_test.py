import os
import tempfile
from ctypes import c_int, create_string_buffer, string_at
from glob import glob
from os import path
from unittest import TestCase

from assertpy import assert_that

from gsfpy import GsfException, open_gsf
from gsfpy.enums import FileMode, RecordType, SeekOption
from gsfpy.gsfDataID import c_gsfDataID
from gsfpy.gsfRecords import c_gsfRecords
from tests import GSF_FOPEN_ERROR


class Test(TestCase):
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
        (_, records) = gsf_file.read(RecordType.GSF_RECORD_COMMENT)
        gsf_file.close()

        # Assert
        assert_that(string_at(records.comment.comment)).is_equal_to(
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

        in_data_id = c_gsfDataID()
        in_data_id.recordID = RecordType.GSF_RECORD_COMMENT

        comment = b"My first comment"

        in_records = c_gsfRecords()
        in_records.comment.comment_time.tvsec = c_int(1000)
        in_records.comment.comment_length = c_int(len(comment))
        in_records.comment.comment = create_string_buffer(comment)

        # Act
        gsf_file = open_gsf(tmp_gsf_file_path, mode=FileMode.GSF_CREATE)
        gsf_file.write(in_data_id, in_records)
        gsf_file.close()

        # Assert
        # Read comment from newly created file to check it is as expected
        gsf_file = open_gsf(tmp_gsf_file_path)
        (out_data_id, out_records) = gsf_file.read(RecordType.GSF_RECORD_COMMENT)
        gsf_file.close()

        assert_that(string_at(out_records.comment.comment)).is_equal_to(comment)
