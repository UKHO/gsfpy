import os
import tempfile
from ctypes import byref, c_int, create_string_buffer, string_at
from glob import glob
from os import path
from unittest import TestCase

import gsfpy.bindings
from gsfpy.enums import FileMode, RecordType, SeekOption
from gsfpy.gsfDataID import c_gsfDataID
from gsfpy.gsfRecords import c_gsfRecords


class Test(TestCase):
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
        self.assertEqual(0, ret_val_open)  # 0 == success
        self.assertEqual(1, file_handle.value)  # 1 == total number of open GSF files
        self.assertEqual(0, ret_val_close)  # 0 == success

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
        self.assertEqual(0, ret_val_open_buffered)  # 0 == success
        self.assertEqual(1, file_handle.value)  # 1 == total number of open GSF files
        self.assertEqual(0, ret_val_close)  # 0 == success

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
        self.assertEqual(0, ret_val_open)  # 0 == success
        self.assertEqual(0, ret_val_seek)  # 0 == success
        self.assertEqual(0, ret_val_close)  # 0 == success

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
        self.assertEqual(-1, ret_val_open)  # -1 == fail
        self.assertEqual(-1, ret_val_int_error)  # -1 == failed to open file
        self.assertEqual(b"GSF Unable to open requested file", ret_val_string_error)

    def test_gsfRead_success(self):
        """
        Read a comment record from a GSF file.
        """
        # Arrange
        file_handle = c_int(0)

        data_id = c_gsfDataID()
        data_id.recordID = RecordType.GSF_RECORD_COMMENT

        records = c_gsfRecords()

        expected_comment = (
            b"Bathy converted from HIPS file: "
            b"M:\\CCOM_Processing\\CARIS_v8\\HIPS\\81\\HDCS_Data\\EX1502L2"
            b"\\Okeanos_March_2011\\2015-081\\0175_20150322_232639_EX1502L2_MB"
        )

        # Act
        ret_val_open = gsfpy.bindings.gsfOpen(
            self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
        )
        bytes_read = gsfpy.bindings.gsfRead(
            file_handle, RecordType.GSF_RECORD_COMMENT, byref(data_id), byref(records),
        )
        ret_val_close = gsfpy.bindings.gsfClose(file_handle)

        # Assert
        self.assertEqual(0, ret_val_open)
        self.assertEqual(168, bytes_read)
        self.assertEqual(expected_comment, string_at(records.comment.comment))
        self.assertEqual(0, ret_val_close)

    def test_gsfWrite_success(self):
        """
        Write a single comment record to a new GSF file
        """
        # Arrange
        file_handle = c_int(0)

        data_id = c_gsfDataID()
        data_id.recordID = RecordType.GSF_RECORD_COMMENT

        records = c_gsfRecords()
        records.comment.comment_time.tvsec = c_int(1000)
        records.comment.comment_length = c_int(17)
        records.comment.comment = create_string_buffer(b"My first comment")

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
        self.assertEqual(0, ret_val_open_create)
        self.assertEqual(40, bytes_written)
        self.assertEqual(0, ret_val_close)

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

        self.assertEqual(b"My first comment", string_at(records.comment.comment))
