import gsfpy
import os
import tempfile

from ctypes import c_double, c_int, c_int32, c_long, c_ubyte, c_uint, POINTER
from datetime import datetime
from gsfpy.enums import FileMode, RecordType, SeekOption
from gsfpy.gsfSwathBathySummary import c_gsfSwathBathySummary
from gsfpy.gsfDataID import c_gsfDataID
from gsfpy.gsfRecords import c_gsfRecords
from gsfpy.timespec import c_timespec
from os import path
import unittest
import assertpy
import shutil


class TestGsfpySwathBathyRecords(unittest.TestCase):

    def setUp(self):

        test_data_306_path = path.join(os.fsencode(path.dirname(__file__)),
                                     b"0029_20160323_185603_EX1604_MB.gsf.mb121")

        self.test_data_306_path = test_data_306_path
        self.test_data_306 = (test_data_306_path, 432)

        end_time = int(datetime.timestamp(datetime.utcnow()))
        start_time = end_time - 60
        start_ts = c_timespec(tv_sec=c_int32(start_time), tv_nsec=c_long(506))
        end_ts = c_timespec(tv_sec=c_int32(end_time), tv_nsec=c_long(509))
        # TODO: tv_nsec should be c_int according to filespec. Check.

        self.summary_to_save = {'min_lat': -14.02349, 'max_lat': 34.089,
                                'min_long': 3.089234, 'max_long': 3.235,
                                'min_depth': 3.23, 'max_depth': 93.23,
                                'start_time': start_ts, 'end_time': end_ts
                                }

    def tearDown(self):
        temp_files = os.listdir(tempfile.gettempdir())
        temp_gsf_files = [f for f in temp_files if f.startswith('temp_gsf')]
        for gsf_file in temp_gsf_files:
            try:
                os.remove(path.join(tempfile.gettempdir(), gsf_file))
            except IOError as io_err:
                print(f'Unable to delete temp file {gsf_file} : {str(io_err)}')

    def test_gsf_swath_summary(self):
        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))

        swath_summary_id = c_gsfDataID()
        swath_summary_id.recordID = \
            c_uint(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value)

        c_gsfDataID_ptr = POINTER(c_gsfDataID)
        p_dataID = c_gsfDataID_ptr(swath_summary_id)

        c_gsfRecords_ptr = POINTER(c_gsfRecords)
        p_record = c_gsfRecords_ptr(c_gsfRecords())

        c_ubyte_ptr = POINTER(c_ubyte)
        p_stream = c_ubyte_ptr()

        expected_start = datetime(year=2016, month=3, day=23,
                                  hour=18, minute=56, second=3)
        expected_end = datetime(year=2016, month=3, day=23,
                                hour=18, minute=57, second=16)

        # Read from file
        open_return_value = gsfpy.bindings.gsfOpen(self.test_data_306_path,
                                                   FileMode.GSF_READONLY,
                                                   p_gsf_fileref
                                                   )
        bytes_read = gsfpy.bindings.gsfRead(
            c_int(p_gsf_fileref[0]),
            c_int(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value),
            p_dataID,
            p_record,
            p_stream,
            0
        )
        close_return_value = gsfpy.bindings.gsfClose(c_int(p_gsf_fileref[0]))

        assertpy.assert_that(open_return_value).is_equal_to(0)
        assertpy.assert_that(bytes_read).is_equal_to(48)

        swath_bathy_summary = p_record.contents.summary

        # stat and end times
        start_timespec = swath_bathy_summary.start_time
        start_time = datetime.utcfromtimestamp(start_timespec.tv_sec)

        end_timespec = swath_bathy_summary.end_time
        end_time = datetime.utcfromtimestamp(end_timespec.tv_sec)

        self.assertEqual(expected_start, start_time)
        self.assertEqual(expected_end, end_time)

        self.assertEqual(167.4759106, swath_bathy_summary.min_longitude)
        self.assertEqual(8.7118203, swath_bathy_summary.min_latitude)
        self.assertEqual(3862.43, swath_bathy_summary.min_depth)
        self.assertEqual(4145.0, swath_bathy_summary.max_depth)
        self.assertEqual(167.477003, swath_bathy_summary.max_longitude)
        self.assertEqual(8.713543, swath_bathy_summary.max_latitude)

        assertpy.assert_that(close_return_value).is_equal_to(0)

    def test_gsf_swathbathyping_read(self):
        mode = FileMode.GSF_READONLY
        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))

        gsf_data_id = c_gsfDataID()
        gsf_data_id.recordID = \
            c_uint(RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING.value)

        c_gsfDataID_ptr = POINTER(c_gsfDataID)
        p_dataID = c_gsfDataID_ptr(gsf_data_id)

        c_gsfRecords_ptr = POINTER(c_gsfRecords)
        p_record = c_gsfRecords_ptr(c_gsfRecords())

        c_ubyte_ptr = POINTER(c_ubyte)
        p_stream = c_ubyte_ptr()

        open_return_value = gsfpy.bindings.gsfOpen(self.test_data_306_path,
                                                   mode,
                                                   p_gsf_fileref
                                                   )
        bytes_read = gsfpy.bindings.gsfRead(
            c_int(p_gsf_fileref[0]),
            c_int(RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING.value),
            p_dataID,
            p_record,
            p_stream,
            0
        )
        close_return_value = gsfpy.bindings.gsfClose(c_int(p_gsf_fileref[0]))

        assertpy.assert_that(open_return_value).is_equal_to(0)
        assertpy.assert_that(close_return_value).is_equal_to(0)

        swath_bathy_record = p_record.contents.mb_ping

        num_beams = swath_bathy_record.number_beams

        assertpy.assert_that(bytes_read).is_greater_than(0)
        assertpy.assert_that(num_beams).is_equal_to(self.test_data_306[1])
        beam_angles = swath_bathy_record.beam_angle[:num_beams]

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
        swath_summary_id.recordID = \
            c_uint(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value)

        c_gsfDataID_ptr = POINTER(c_gsfDataID)
        p_dataID = c_gsfDataID_ptr(swath_summary_id)

        c_gsfRecords_ptr = POINTER(c_gsfRecords)
        p_record = c_gsfRecords_ptr(c_gsfRecords())

        c_ubyte_ptr = POINTER(c_ubyte)
        p_stream = c_ubyte_ptr()

        # Read the record that will be amended
        open_return_value = gsfpy.bindings.gsfOpen(os.fsencode(tmp_file_path),
                                                   file_mode,
                                                   p_gsf_fileref
                                                   )
        bytes_read = gsfpy.bindings.gsfRead(
            c_int(p_gsf_fileref[0]),
            c_int(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value),
            p_dataID,
            p_record,
            p_stream
        )

        assertpy.assert_that(bytes_read).is_equal_to(48)

        summary = p_record.contents.summary
        summary.start_time = self.summary_to_save['start_time']
        summary.end_time = self.summary_to_save['end_time']
        summary.max_depth = c_double(self.summary_to_save['max_depth'])
        summary.min_depth = c_double(self.summary_to_save['min_depth'])
        summary.min_latitude = c_double(self.summary_to_save['min_lat'])
        summary.max_latitude = c_double(self.summary_to_save['max_lat'])
        summary.min_longitude = c_double(self.summary_to_save['min_long'])
        summary.max_longitude = c_double(self.summary_to_save['max_long'])
        # Go back to the first record so it doesn't write
        # the updated first summary over the top of the second one
        seek_return_value = gsfpy.bindings.gsfSeek(c_int(p_gsf_fileref[0]),
                                                   SeekOption.GSF_PREVIOUS_RECORD)
        bytes_written = gsfpy.bindings.gsfWrite(c_int(p_gsf_fileref[0]),
                                                p_dataID, p_record)
        close_return_value = gsfpy.bindings.gsfClose(c_int(p_gsf_fileref[0]))

        assertpy.assert_that(seek_return_value).is_equal_to(0)
        assertpy.assert_that(bytes_written).is_equal_to(48)
        assertpy.assert_that(close_return_value).is_equal_to(0)

        # Read it back out and check it was saved correctly

        c_int_ptr_read = POINTER(c_int)
        p_gsf_file_ref = c_int_ptr_read(c_int(0))
        gsf_read_data_id = c_gsfDataID()
        gsf_read_data_id.recordID = c_uint(
            RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value)

        c_gsf_data_id_ptr = POINTER(c_gsfDataID)
        p_data_id = c_gsf_data_id_ptr(gsf_read_data_id)

        c_gsf_records_ptr = POINTER(c_gsfRecords)
        p_read_record = c_gsf_records_ptr(c_gsfRecords())

        c_ubyte_ptr = POINTER(c_ubyte)
        p_rstream = c_ubyte_ptr()

        open_read_return_value = gsfpy.bindings.gsfOpen(
            os.fsencode(tmp_file_path),
            FileMode.GSF_READONLY,
            p_gsf_file_ref)

        bytes_read = gsfpy.bindings.gsfRead(
            c_int(p_gsf_file_ref[0]),
            c_int(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value),
            p_data_id,
            p_read_record,
            p_rstream,
            0
        )

        read_summary = p_read_record.contents.summary

        close_return_value = gsfpy.bindings.gsfClose(c_int(p_gsf_file_ref[0]))

        start_time = self.summary_to_save['start_time']
        end_time = self.summary_to_save['end_time']

        self.assertEqual(0, open_read_return_value)
        self.assertEqual(48, bytes_read)
        self.assertEqual(read_summary.min_depth, self.summary_to_save['min_depth'])
        self.assertEqual(read_summary.max_depth, self.summary_to_save['max_depth'])
        self.assertEqual(read_summary.min_latitude, self.summary_to_save['min_lat'])
        self.assertEqual(read_summary.max_latitude, self.summary_to_save['max_lat'])
        self.assertEqual(read_summary.min_longitude, self.summary_to_save['min_long'])
        self.assertEqual(read_summary.max_longitude, self.summary_to_save['max_long'])
        self.assertEqual(self.summary_to_save['start_time'].tv_sec,
                         read_summary.start_time.tv_sec)
        self.assertEqual(self.summary_to_save['end_time'].tv_sec,
                         read_summary.end_time.tv_sec)
        self.assertEqual(self.summary_to_save['start_time'].tv_nsec,
                         read_summary.start_time.tv_nsec)
        self.assertEqual(self.summary_to_save['end_time'].tv_nsec,
                         read_summary.end_time.tv_nsec)
        self.assertEqual(0, close_return_value)

    def test_gsf_swathsummary_save_create(self):
        tmp_file_path = path.join(tempfile.gettempdir(),
                                  'temp_gsf_306_test_data_create.gsf')

        file_mode = FileMode.GSF_CREATE

        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))

        swath_summary_id = c_gsfDataID()
        swath_summary_id.recordID = \
            c_uint(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value)

        c_gsfDataID_ptr = POINTER(c_gsfDataID)
        p_dataID = c_gsfDataID_ptr(swath_summary_id)

        c_gsfRecords_ptr = POINTER(c_gsfRecords)
        p_record = c_gsfRecords_ptr(c_gsfRecords())

        ts_start = self.summary_to_save['start_time']
        ts_end = self.summary_to_save['end_time']

        summary = c_gsfSwathBathySummary(
            start_time=ts_start,
            end_time=ts_end,
            min_latitude=c_double(self.summary_to_save['min_lat']),
            max_latitude=c_double(self.summary_to_save['max_lat']),
            min_longitude=c_double(self.summary_to_save['min_long']),
            max_longitude=c_double(self.summary_to_save['max_long']),
            min_depth=c_double(self.summary_to_save['min_depth']),
            max_depth=c_double(self.summary_to_save['max_depth'])
            )

        p_record.contents.summary = summary

        open_create_return_value = gsfpy.bindings.gsfOpen(
            os.fsencode(tmp_file_path),
            file_mode,
            p_gsf_fileref
        )

        bytes_written = gsfpy.bindings.gsfWrite(c_int(p_gsf_fileref[0]),
                                                p_dataID,
                                                p_record)
        close_return_value = gsfpy.bindings.gsfClose(c_int(p_gsf_fileref[0]))

        self.assertEqual(0, open_create_return_value)
        self.assertEqual(48, bytes_written)
        self.assertEqual(0, close_return_value)

        # Read it back out and check that it matches expected values
        c_int_ptr_read = POINTER(c_int)
        p_gsf_file_ref = c_int_ptr_read(c_int(0))
        gsf_read_data_id = c_gsfDataID()
        gsf_read_data_id.recordID = c_uint(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING.value)

        c_gsf_data_id_ptr = POINTER(c_gsfDataID)
        p_data_id = c_gsf_data_id_ptr(gsf_read_data_id)

        c_gsf_records_ptr = POINTER(c_gsfRecords)
        p_read_record = c_gsf_records_ptr(c_gsfRecords())

        c_ubyte_ptr = POINTER(c_ubyte)
        p_stream = c_ubyte_ptr()

        open_read_return_value = gsfpy.bindings.gsfOpen(os.fsencode(tmp_file_path),
                                                        FileMode.GSF_READONLY,
                                                        p_gsf_file_ref)
        bytes_read = gsfpy.bindings.gsfRead(
            c_int(p_gsf_file_ref[0]),
            c_int(RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value),
            p_data_id,
            p_read_record,
            p_stream,
            0
        )
        close_read_return_value = gsfpy.bindings.gsfClose(c_int(p_gsf_file_ref[0]))

        assertpy.assert_that(open_read_return_value).is_equal_to(0)
        assertpy.assert_that(close_read_return_value).is_equal_to(0)
        assertpy.assert_that(bytes_read).is_equal_to(48)
        read_summary = p_read_record.contents.summary

        read_start_time = read_summary.start_time.tv_sec
        read_end_time = read_summary.end_time.tv_sec

        assertpy.assert_that(read_start_time).is_equal_to(ts_start.tv_sec)
        assertpy.assert_that(read_end_time).is_equal_to(ts_end.tv_sec)
        assertpy.assert_that(read_summary.min_depth)\
            .is_equal_to(self.summary_to_save['min_depth'])
        assertpy.assert_that(read_summary.max_depth)\
            .is_equal_to(self.summary_to_save['max_depth'])
        assertpy.assert_that(read_summary.min_latitude)\
            .is_equal_to(self.summary_to_save['min_lat'])
        assertpy.assert_that(read_summary.max_latitude)\
            .is_equal_to(self.summary_to_save['max_lat'])
        assertpy.assert_that(read_summary.min_longitude)\
            .is_equal_to(self.summary_to_save['min_long'])
        assertpy.assert_that(read_summary.max_longitude)\
            .is_equal_to(self.summary_to_save['max_long'])
