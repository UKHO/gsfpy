import gsfpy
import os
import tempfile

from ctypes import *
from datetime import datetime
from gsfpy.enums import FileMode, RecordType, SeekOption
from gsfpy.gsfSwathBathySummary import c_gsfSwathBathySummary
from gsfpy.gsfDataID import c_gsfDataID
from gsfpy.gsfRecords import c_gsfRecords
from gsfpy.timespec import c_timespec
from gsfpy import bindings
from os import path
import unittest
import assertpy
import shutil

class TestGsfpySwathBathyRecords(unittest.TestCase):

    def setUp(self):
       # self.test_data_306_path = path.join(os.fsencode(path.dirname(__file__)), b"0175_20150322_232639_EX1502L2_MB.gsf.mb121")
        self.test_data_306_path = path.join(os.fsencode(path.dirname(__file__)), b"0008_20160515_142608_-_0003.gsf.mb121")
        test_data_306_path = path.join(os.fsencode(path.dirname(__file__)), b"0008_20160515_142608_-_0003.gsf.mb121")
        self.test_data_306 = (test_data_306_path, 511)

    def tearDown(self):
        return
        temp_gsf_files = [f for f in os.listdir(tempfile.gettempdir()) if f.startswith('temp_gsf')]
        for gsf_file in temp_gsf_files:
            try:
                os.remove(path.join(tempfile.gettempdir(), gsf_file))
            except IOError as io_err:
                print(f'Unable to delete temp file {gsf_file} : {str(io_err)}')

    def test_gsf_swath_summary(self):
        mode = FileMode.GSF_READONLY
        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))

        swath_summary_id = c_gsfDataID()
        swath_summary_id.recordID = c_uint(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value)

        c_gsfDataID_ptr = POINTER(c_gsfDataID)
        p_dataID = c_gsfDataID_ptr(swath_summary_id)

        c_gsfRecords_ptr = POINTER(c_gsfRecords)
        p_record = c_gsfRecords_ptr(c_gsfRecords())

        c_ubyte_ptr = POINTER(c_ubyte)
        p_stream = c_ubyte_ptr()

        expected_start = datetime(year=2016, month=5, day=15, hour=14, minute=26, second=8)
        expected_end = datetime(year=2016, month=5, day=15, hour=14, minute=26, second=30)

        # Read from file
        retValOpen = gsfpy.bindings.gsfOpen(self.test_data_306_path, mode, p_gsf_fileref)
        bytesRead = gsfpy.bindings.gsfRead(p_gsf_fileref[0], c_int(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value),
                                            p_dataID, p_record, p_stream, 0)
        retValClose = gsfpy.bindings.gsfClose(p_gsf_fileref[0])

        self.assertEqual(0, retValOpen)
        self.assertEqual(48, bytesRead)
        swath_bathy_summary = p_record.contents.summary

        # stat and end times
        start_timespec = swath_bathy_summary.start_time
        start_time = datetime.utcfromtimestamp(start_timespec.tv_sec)

        end_timespec = swath_bathy_summary.end_time
        end_time = datetime.utcfromtimestamp(end_timespec.tv_sec)

        self.assertEqual(expected_start, start_time)
        self.assertEqual(expected_end, end_time)

        self.assertEqual(-6.1044486, swath_bathy_summary.min_longitude)
        self.assertEqual(53.243588, swath_bathy_summary.min_latitude)
        self.assertEqual(9.05, swath_bathy_summary.min_depth)
        self.assertEqual(11.49, swath_bathy_summary.max_depth)
        self.assertEqual(-6.1042584, swath_bathy_summary.max_longitude)
        self.assertEqual(53.2441394, swath_bathy_summary.max_latitude)


        self.assertEqual(0, retValClose)

    def test_gsf_swathbathyping_read(self):
        mode = FileMode.GSF_READONLY
        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))

        gsf_data_id = c_gsfDataID()
        gsf_data_id.recordID = c_uint(RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING.value)

        c_gsfDataID_ptr = POINTER(c_gsfDataID)
        p_dataID = c_gsfDataID_ptr(gsf_data_id)

        c_gsfRecords_ptr = POINTER(c_gsfRecords)
        p_record = c_gsfRecords_ptr(c_gsfRecords())

        c_ubyte_ptr = POINTER(c_ubyte)
        p_stream = c_ubyte_ptr()

        open_return_value = gsfpy.bindings.gsfOpen(self.test_data_306_path, mode, p_gsf_fileref)
        bytes_read = gsfpy.bindings.gsfRead(p_gsf_fileref[0], c_int(RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING.value),
                                            p_dataID, p_record, p_stream, 0)
        close_return_value = gsfpy.bindings.gsfClose(p_gsf_fileref[0])

        assertpy.assert_that(open_return_value).is_equal_to(0)
        assertpy.assert_that(close_return_value).is_equal_to(0)

        swath_bathy_record = p_record.contents.mb_ping

        num_beams = swath_bathy_record.number_beams

        assertpy.assert_that(bytes_read).is_greater_than(0)
        assertpy.assert_that(num_beams).is_equal_to(self.test_data_306[1])
        beam_angles = swath_bathy_record.beam_angle[:num_beams]
        assertpy.assert_that(beam_angles).is_sorted()
        assertpy.assert_that(beam_angles)
        beam_angles_in_range = [180 >= x >= -180 for x in beam_angles]
        assertpy.assert_that(False).is_not_in(beam_angles_in_range)

    def test_gsf_swathsummary_save_update(self):
        tmp_file_path = '/tmp/temp_gsf_306_test_data_update.gsf'
        shutil.copyfile(self.test_data_306_path, tmp_file_path)
        file_mode = FileMode.GSF_UPDATE

        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))

        swath_summary_id = c_gsfDataID()
        swath_summary_id.recordID = c_uint(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value)

        c_gsfDataID_ptr = POINTER(c_gsfDataID)
        p_dataID = c_gsfDataID_ptr(swath_summary_id)

        c_gsfRecords_ptr = POINTER(c_gsfRecords)
        p_record = c_gsfRecords_ptr(c_gsfRecords())

        c_ubyte_ptr = POINTER(c_ubyte)
        p_stream = c_ubyte_ptr()

        # Act
        retValOpen = gsfpy.bindings.gsfOpen(os.fsencode(tmp_file_path), file_mode, p_gsf_fileref)
        bytesRead = gsfpy.bindings.gsfRead(p_gsf_fileref[0], c_int(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value),
                                            p_dataID, p_record, p_stream)


        end_time = int(datetime.timestamp(datetime.utcnow()))
        start_time = end_time - 60

        p_record.contents.summary.start_time = c_timespec(tv_sec=c_int32(start_time), tv_nsec=c_long(506))
        p_record.contents.summary.end_time = c_timespec(tv_sec=c_int32(end_time), tv_nsec=c_long(509))
        p_record.contents.summary.max_depth = c_double(789)
        p_record.contents.summary.min_depth = c_double(345)
        p_record.contents.summary.min_latitude = c_double(4)
        p_record.contents.summary.max_latitude = c_double(5)
        p_record.contents.summary.min_longitude = c_double(4)
        p_record.contents.summary.max_longitude = c_double(5)
        # Go back to the first record so it doesn't write the updated first summary over the top of the second one
        seek_return_value = gsfpy.bindings.gsfSeek(c_int(p_gsf_fileref[0]), SeekOption.GSF_PREVIOUS_RECORD)

        bytes_written = gsfpy.bindings.gsfWrite(c_int(p_gsf_fileref[0]), p_dataID, p_record)

        retValClose = gsfpy.bindings.gsfClose(c_int(p_gsf_fileref[0]))

        self.assertTrue(bytes_written == 48)
        self.assertTrue(retValClose == 0)
        self.assertTrue(seek_return_value == 0)

        # Read it back out and check it was saved correctly

        c_int_ptr_read = POINTER(c_int)
        p_gsf_file_ref = c_int_ptr_read(c_int(0))
        gsf_read_data_id = c_gsfDataID()
        gsf_read_data_id.recordID = c_uint(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value)

        c_gsf_data_id_ptr = POINTER(c_gsfDataID)
        p_data_id = c_gsf_data_id_ptr(gsf_read_data_id)

        c_gsf_records_ptr = POINTER(c_gsfRecords)
        p_read_record = c_gsf_records_ptr(c_gsfRecords())

        c_ubyte_ptr = POINTER(c_ubyte)
        p_rstream = c_ubyte_ptr()

        open_read_return_value = gsfpy.bindings.gsfOpen(os.fsencode(tmp_file_path), FileMode.GSF_READONLY, p_gsf_file_ref)

        bytes_read = gsfpy.bindings.gsfRead(p_gsf_file_ref[0], c_int(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value),
                                            p_data_id, p_read_record, p_rstream, 0)

        read_summary = p_read_record.contents.summary

        close_return_value = gsfpy.bindings.gsfClose(p_gsf_file_ref[0])

        # Assert
        self.assertEqual(0, open_read_return_value)
        self.assertEqual(48, bytes_read)
        self.assertEqual(read_summary.min_depth, 345)
        self.assertEqual(read_summary.max_depth, 789)
        self.assertEqual(read_summary.min_latitude, 4)
        self.assertEqual(read_summary.max_latitude, 5)
        self.assertEqual(read_summary.min_longitude, 4)
        self.assertEqual(read_summary.max_longitude, 5)
        self.assertEqual(start_time, read_summary.start_time.tv_sec)
        self.assertEqual(end_time, read_summary.end_time.tv_sec)
        self.assertEqual(read_summary.end_time.tv_nsec, 509)
        self.assertEqual(read_summary.start_time.tv_nsec, 506)

    def test_gsf_swathsummary_save_create(self):
        tmp_file_path = path.join(tempfile.gettempdir(), 'temp_gsf_306_test_data_create.gsf')

        file_mode = FileMode.GSF_CREATE

        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))

        swath_summary_id = c_gsfDataID()
        swath_summary_id.recordID = c_uint(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value)

        c_gsfDataID_ptr = POINTER(c_gsfDataID)
        p_dataID = c_gsfDataID_ptr(swath_summary_id)

        c_gsfRecords_ptr = POINTER(c_gsfRecords)
        p_record = c_gsfRecords_ptr(c_gsfRecords())

        c_ubyte_ptr = POINTER(c_ubyte)
        p_stream = c_ubyte_ptr()

        current_time = datetime.utcnow()

        end_time = int(datetime.timestamp(current_time))
        start_time = end_time - 10

        ts_start = c_timespec()
        ts_start.tv_sec  = c_int32(start_time)
        ts_start.tv_nsec = c_long(456)  # TODO: This should be c_int according to filespec. Check.

        ts_end = c_timespec()
        ts_end.tv_sec = c_int32(end_time)
        ts_end.tv_nsec = c_long(3233)  # TODO: This should be c_int according to filespec. Check.

        summary = c_gsfSwathBathySummary()
        summary.start_time = ts_start
        summary.end_time = ts_end
        summary.min_latitude = 23.90411
        summary.max_latitude = 41.30234
        summary.min_longitude = 2.23904
        summary.max_longitude = 9.923044
        summary.min_depth = 59.30
        summary.max_depth = 85.902

        p_record.contents.summary = summary

        open_create_return_value = gsfpy.bindings.gsfOpen(os.fsencode(tmp_file_path), file_mode, p_gsf_fileref)
        bytes_written = gsfpy.bindings.gsfWrite(p_gsf_fileref[0], p_dataID, p_record)
        close_return_value = gsfpy.bindings.gsfClose(p_gsf_fileref[0])

        self.assertEqual(0, open_create_return_value)
        self.assertEqual(48, bytes_written)
        self.assertEqual(0, close_return_value)

        c_int_ptr_read = POINTER(c_int)
        p_gsf_file_ref = c_int_ptr_read(c_int(0))
        gsf_read_data_id = c_gsfDataID()
        gsf_read_data_id.recordID = c_uint(RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING.value)

        c_gsf_data_id_ptr = POINTER(c_gsfDataID)
        p_data_id = c_gsf_data_id_ptr(gsf_read_data_id)

        c_gsf_records_ptr = POINTER(c_gsfRecords)
        p_read_record = c_gsf_records_ptr(c_gsfRecords())

        c_ubyte_ptr = POINTER(c_ubyte)
        p_stream = c_ubyte_ptr()

        open_read_return_value = gsfpy.bindings.gsfOpen(os.fsencode(tmp_file_path), FileMode.GSF_READONLY, p_gsf_file_ref)
        bytes_read = gsfpy.bindings.gsfRead(p_gsf_file_ref[0], c_int(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value),
                                            p_data_id, p_read_record, p_stream, 0)
        close_return_value = gsfpy.bindings.gsfClose(p_gsf_file_ref[0])

        # Assert
        self.assertEqual(0, open_read_return_value)
        self.assertEqual(48, bytes_read)
        read_summary = p_read_record.contents.summary

        start_timespec = read_summary.start_time
        read_start_time = start_timespec.tv_sec

        #endtime
        end_timespec = read_summary.end_time
        read_end_time = end_timespec.tv_sec

        self.assertEqual(start_time, read_start_time)
        self.assertEqual(end_time, read_end_time)
