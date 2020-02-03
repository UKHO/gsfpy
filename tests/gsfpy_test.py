import os
import tempfile
from ctypes import *
from glob import glob
from os import path
from unittest import TestCase

import gsfpy
from gsfpy.enums import FileMode, RecordType, SeekOption
from gsfpy.gsfDataID import c_gsfDataID
from gsfpy.gsfRecords import c_gsfRecords


class Test(TestCase):
    def setup_method(self, method):
        self.test_data_path = path.join(os.fsencode(path.dirname(__file__)), b'gsfpy_test_data.gsf')

    @classmethod
    def teardown_class(cls):
        print('\n')
        for gsf in glob(path.join(tempfile.gettempdir(), '*.gsf')):
            print('cleaning up, removing {0}'.format(gsf))
            os.remove(gsf)

    # Open the test GSF file, then close
    def test_gsfOpenClose_success(self):
        # Arrange
        mode = FileMode.GSF_READONLY
        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))

        # Act
        retValOpen = gsfpy.gsfOpen(self.test_data_path, mode, p_gsf_fileref)
        retValClose = gsfpy.gsfClose(p_gsf_fileref[0])

        # Assert
        self.assertEqual(0, retValOpen)         # 0 == success
        self.assertEqual(1, p_gsf_fileref[0])   # 1 == total number of open GSF files
        self.assertEqual(0, retValClose)        # 0 == success

    # Open the test GSF file, then close
    def test_gsfOpenBuffered_success(self):
        # Arrange
        mode = FileMode.GSF_READONLY
        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))
        buf_size = 100

        # Act
        retValOpenBuffered = gsfpy.gsfOpenBuffered(self.test_data_path, mode, p_gsf_fileref, buf_size)
        retValClose = gsfpy.gsfClose(p_gsf_fileref[0])

        # Assert
        self.assertEqual(0, retValOpenBuffered)     # 0 == success
        self.assertEqual(1, p_gsf_fileref[0])       # 1 == total number of open GSF files
        self.assertEqual(0, retValClose)            # 0 == success

    # Open the test GSF file, seek to end of file, then close
    def test_gsfSeek_success(self):
        # Arrange
        mode = FileMode.GSF_READONLY
        seekOption = SeekOption.GSF_END_OF_FILE
        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))

        # Act
        retValOpen = gsfpy.gsfOpen(self.test_data_path, mode, p_gsf_fileref)
        retValSeek = gsfpy.gsfSeek(p_gsf_fileref[0], seekOption)
        retValClose = gsfpy.gsfClose(p_gsf_fileref[0])

        # Assert
        self.assertEqual(0, retValOpen)             # 0 == success
        self.assertEqual(0, retValSeek)             # 0 == success
        self.assertEqual(0, retValClose)            # 0 == success

    # Try to open a non-existent GSF file and check that gsfError() returns the correct error code and error message
    def test_gsfError(self):
        # Arrange
        mode = FileMode.GSF_READONLY
        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))

        # Act
        retValOpen = gsfpy.gsfOpen(b'non-existent.gsf', mode, p_gsf_fileref)
        retValIntError = gsfpy.gsfIntError()
        retValStringError = gsfpy.gsfStringError()

        # Assert
        self.assertEqual(-1, retValOpen)            # -1 == fail
        self.assertEqual(-1, retValIntError)        # -1 == failed to open file
        self.assertEqual(b'GSF Unable to open requested file', retValStringError)

    # Read a comment record from a GSF file
    def test_gsfRead_success(self):
        # Arrange
        mode = FileMode.GSF_READONLY
        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))
        
        commentID = c_gsfDataID()
        commentID.recordID = c_uint(RecordType.GSF_RECORD_COMMENT.value)

        c_gsfDataID_ptr = POINTER(c_gsfDataID)
        p_dataID = c_gsfDataID_ptr(commentID)

        c_gsfRecords_ptr = POINTER(c_gsfRecords)
        p_rec = c_gsfRecords_ptr(c_gsfRecords())

        c_ubyte_ptr = POINTER(c_ubyte)
        p_stream = c_ubyte_ptr()

        expected_comment = b'Bathy converted from HIPS file: M:\\CCOM_Processing\\CARIS_v8\\HIPS\\81\\HDCS_Data\\EX1502L2\\Okeanos_March_2011\\2015-081\\0175_20150322_232639_EX1502L2_MB'

        # Act
        retValOpen = gsfpy.gsfOpen(self.test_data_path, mode, p_gsf_fileref)
        bytesRead = gsfpy.gsfRead(p_gsf_fileref[0], c_int(RecordType.GSF_RECORD_COMMENT.value), p_dataID, p_rec, p_stream, 0)
        retValClose = gsfpy.gsfClose(p_gsf_fileref[0])

        # Assert
        self.assertEqual(0, retValOpen)
        self.assertEqual(168, bytesRead)
        self.assertEqual(expected_comment, string_at(p_rec.contents.comment.comment))
        self.assertEqual(0, retValClose)

    # Write a single comment record to a new GSF file
    def test_gsfWrite_success(self):
        # Arrange
        createMode = FileMode.GSF_CREATE
        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))

        commentID = c_gsfDataID()
        commentID.recordID = c_uint(RecordType.GSF_RECORD_COMMENT.value)

        c_gsfDataID_ptr = POINTER(c_gsfDataID)
        p_dataID = c_gsfDataID_ptr(commentID)

        c_gsfRecords_ptr = POINTER(c_gsfRecords)
        p_rec = c_gsfRecords_ptr(c_gsfRecords())
        p_rec.contents.comment.comment_time.tvsec = c_int(1000)
        p_rec.contents.comment.comment_length = c_int(17)
        p_rec.contents.comment.comment = create_string_buffer(b'My first comment')

        tmpgsffilepath = path.join(os.fsencode(tempfile.gettempdir()), b'temp.gsf')

        # Act
        retValOpenCreate = gsfpy.gsfOpen(tmpgsffilepath, createMode, p_gsf_fileref)
        bytesWritten = gsfpy.gsfWrite(p_gsf_fileref[0], p_dataID, p_rec)
        retValClose = gsfpy.gsfClose(p_gsf_fileref[0])

        # Assert
        self.assertEqual(0, retValOpenCreate)
        self.assertEqual(40, bytesWritten)
        self.assertEqual(0, retValClose)

        # Read comment from newly created file to check it is as expected
        commentID = c_gsfDataID()
        commentID.recordID = c_uint(RecordType.GSF_RECORD_COMMENT.value)

        c_gsfDataID_ptr = POINTER(c_gsfDataID)
        p_dataID = c_gsfDataID_ptr(commentID)

        c_gsfRecords_ptr = POINTER(c_gsfRecords)
        p_rec = c_gsfRecords_ptr(c_gsfRecords())

        c_ubyte_ptr = POINTER(c_ubyte)
        p_stream = c_ubyte_ptr()

        retValOpenCreate = gsfpy.gsfOpen(tmpgsffilepath, FileMode.GSF_READONLY, p_gsf_fileref)
        gsfpy.gsfRead(p_gsf_fileref[0], c_int(RecordType.GSF_RECORD_COMMENT.value), p_dataID, p_rec, p_stream, 0)
        gsfpy.gsfClose(p_gsf_fileref[0])

        self.assertEqual(b'My first comment', string_at(p_rec.contents.comment.comment))