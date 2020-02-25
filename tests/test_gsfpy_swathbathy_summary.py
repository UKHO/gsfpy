import os
import shutil
import tempfile
import unittest
from ctypes import byref, c_int, c_int32, c_long, c_uint
from datetime import datetime
from os import path

from assertpy import assert_that

import gsfpy
from gsfpy.enums import FileMode, RecordType, SeekOption
from gsfpy.gsfDataID import c_gsfDataID
from gsfpy.gsfRecords import c_gsfRecords
from gsfpy.gsfSwathBathySummary import c_gsfSwathBathySummary
from gsfpy.timespec import c_timespec


class TestGsfpySwathBathySummary(unittest.TestCase):
    def setUp(self):
        self.test_data_306 = {
            "path": path.join(
                os.fsencode(path.dirname(__file__)),
                b"0029_20160323_185603_EX1604_MB.gsf.mb121",
            )
        }
        self.summary_record_length = 48  # Length of a summary record in bytes

        end_time = int(datetime.timestamp(datetime.utcnow()))
        start_time = end_time - 60
        start_ts = c_timespec(tv_sec=c_int32(start_time), tv_nsec=c_long(506))
        end_ts = c_timespec(tv_sec=c_int32(end_time), tv_nsec=c_long(509))

        self.summary_to_save = {
            "min_lat": -14.02349,
            "max_lat": 34.089,
            "min_long": 3.089234,
            "max_long": 3.235,
            "min_depth": 3.23,
            "max_depth": 93.23,
            "start_time": start_ts,
            "end_time": end_ts,
        }

    @classmethod
    def setUpClass(cls):
        cls.temp_gsf_dir = tempfile.mkdtemp(prefix="tmp_gsftest_")

    @classmethod
    def tearDownClass(cls):
        temp_gsf_dir = cls.temp_gsf_dir
        temp_gsf_files = os.listdir(temp_gsf_dir)
        for temp_file in temp_gsf_files:
            try:
                os.remove(path.join(temp_gsf_dir, temp_file))
            except (OSError, IOError) as exception:
                print(f"Unable to delete temp file {temp_file} : {str(exception)}")
        try:
            os.rmdir(temp_gsf_dir)
        except (OSError, IOError) as exception:
            print(f"Unable to delete temp dir {temp_gsf_dir} : {str(exception)}")

    def test_gsf_swath_summary(self):
        gsf_fileref = c_int(0)

        swath_summary_id = c_gsfDataID()
        swath_summary_id.recordID = c_uint(
            RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value
        )

        records = c_gsfRecords()

        expected_start = datetime(
            year=2016, month=3, day=23, hour=18, minute=56, second=3
        )
        expected_end = datetime(
            year=2016, month=3, day=23, hour=18, minute=57, second=16
        )

        # Read from file
        open_return_value = gsfpy.bindings.gsfOpen(
            self.test_data_306["path"], FileMode.GSF_READONLY, byref(gsf_fileref)
        )
        bytes_read = gsfpy.bindings.gsfRead(
            gsf_fileref,
            RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY,
            byref(swath_summary_id),
            byref(records),
        )
        close_return_value = gsfpy.bindings.gsfClose(gsf_fileref)

        assert_that(open_return_value).is_equal_to(0)
        assert_that(bytes_read).is_equal_to(self.summary_record_length)

        swath_bathy_summary = records.summary

        # stat and end times
        start_timespec = swath_bathy_summary.start_time
        start_time = datetime.utcfromtimestamp(start_timespec.tv_sec)

        end_timespec = swath_bathy_summary.end_time
        end_time = datetime.utcfromtimestamp(end_timespec.tv_sec)

        assert_that(expected_start).is_equal_to(start_time)
        assert_that(expected_end).is_equal_to(end_time)

        assert_that(167.4759106).is_equal_to(swath_bathy_summary.min_longitude)
        assert_that(8.7118203).is_equal_to(swath_bathy_summary.min_latitude)
        assert_that(3862.43).is_equal_to(swath_bathy_summary.min_depth)
        assert_that(4145.0).is_equal_to(swath_bathy_summary.max_depth)
        assert_that(167.477003).is_equal_to(swath_bathy_summary.max_longitude)
        assert_that(8.713543).is_equal_to(swath_bathy_summary.max_latitude)

        assert_that(close_return_value).is_equal_to(0)

    def test_gsf_swath_summary_save_update(self):
        tmp_file_path = path.join(
            self.temp_gsf_dir, "temp_gsf_306_test_data_update.gsf"
        )
        shutil.copyfile(self.test_data_306["path"], tmp_file_path)
        file_mode = FileMode.GSF_UPDATE

        gsf_fileref = c_int(0)

        swath_summary_data_id = c_gsfDataID()
        swath_summary_data_id.recordID = c_uint(
            RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value
        )

        records = c_gsfRecords()

        # Read the record that will be amended
        open_return_value = gsfpy.bindings.gsfOpen(
            os.fsencode(tmp_file_path), file_mode, byref(gsf_fileref)
        )
        bytes_read = gsfpy.bindings.gsfRead(
            gsf_fileref,
            RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY,
            byref(swath_summary_data_id),
            byref(records),
        )

        summary = records.summary
        summary.start_time = self.summary_to_save["start_time"]
        summary.end_time = self.summary_to_save["end_time"]
        summary.max_depth = self.summary_to_save["max_depth"]
        summary.min_depth = self.summary_to_save["min_depth"]
        summary.min_latitude = self.summary_to_save["min_lat"]
        summary.max_latitude = self.summary_to_save["max_lat"]
        summary.min_longitude = self.summary_to_save["min_long"]
        summary.max_longitude = self.summary_to_save["max_long"]
        # Go back to the first record so it doesn't write
        # the updated first summary over the top of the second one
        seek_return_value = gsfpy.bindings.gsfSeek(
            gsf_fileref, SeekOption.GSF_PREVIOUS_RECORD
        )
        bytes_written = gsfpy.bindings.gsfWrite(
            gsf_fileref, byref(swath_summary_data_id), byref(records)
        )
        close_return_value = gsfpy.bindings.gsfClose(gsf_fileref)

        assert_that(open_return_value).is_equal_to(0)
        assert_that(bytes_read).is_equal_to(self.summary_record_length)
        assert_that(seek_return_value).is_equal_to(0)
        assert_that(bytes_written).is_equal_to(self.summary_record_length)
        assert_that(close_return_value).is_equal_to(0)

        # Read it back out and check it was saved correctly

        read_gsf_file_ref = c_int(0)
        gsf_read_data_id = c_gsfDataID()
        gsf_read_data_id.recordID = c_uint(
            RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value
        )

        read_record = c_gsfRecords()

        open_read_return_value = gsfpy.bindings.gsfOpen(
            os.fsencode(tmp_file_path), FileMode.GSF_READONLY, byref(read_gsf_file_ref)
        )

        bytes_read = gsfpy.bindings.gsfRead(
            read_gsf_file_ref,
            RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY,
            byref(gsf_read_data_id),
            byref(read_record),
        )

        read_summary = read_record.summary

        close_return_value = gsfpy.bindings.gsfClose(read_gsf_file_ref)

        save_start_time = self.summary_to_save["start_time"]
        save_end_time = self.summary_to_save["end_time"]

        assert_that(0).is_equal_to(open_read_return_value)
        assert_that(self.summary_record_length).is_equal_to(bytes_read)
        assert_that(read_summary.min_depth).is_equal_to(
            self.summary_to_save["min_depth"]
        )
        assert_that(read_summary.max_depth).is_equal_to(
            self.summary_to_save["max_depth"]
        )
        assert_that(read_summary.min_latitude).is_equal_to(
            self.summary_to_save["min_lat"]
        )
        assert_that(read_summary.max_latitude).is_equal_to(
            self.summary_to_save["max_lat"]
        )
        assert_that(read_summary.min_longitude).is_equal_to(
            self.summary_to_save["min_long"]
        )
        assert_that(read_summary.max_longitude).is_equal_to(
            self.summary_to_save["max_long"]
        )
        assert_that(save_start_time.tv_sec).is_equal_to(read_summary.start_time.tv_sec)
        assert_that(save_end_time.tv_sec).is_equal_to(read_summary.end_time.tv_sec)
        assert_that(save_start_time.tv_nsec).is_equal_to(
            read_summary.start_time.tv_nsec
        )
        assert_that(save_end_time.tv_nsec).is_equal_to(read_summary.end_time.tv_nsec)
        assert_that(0).is_equal_to(close_return_value)

    def test_gsf_swath_summary_save_create(self):
        tmp_file_path = path.join(
            self.temp_gsf_dir, "temp_gsf_306_test_data_create.gsf"
        )

        file_mode = FileMode.GSF_CREATE

        file_ref = c_int(0)

        swath_summary_id = c_gsfDataID()
        swath_summary_id.recordID = c_uint(
            RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value
        )

        records = c_gsfRecords()

        ts_start = self.summary_to_save["start_time"]
        ts_end = self.summary_to_save["end_time"]

        summary = c_gsfSwathBathySummary(
            start_time=ts_start,
            end_time=ts_end,
            min_latitude=self.summary_to_save["min_lat"],
            max_latitude=self.summary_to_save["max_lat"],
            min_longitude=self.summary_to_save["min_long"],
            max_longitude=self.summary_to_save["max_long"],
            min_depth=self.summary_to_save["min_depth"],
            max_depth=self.summary_to_save["max_depth"],
        )

        records.summary = summary

        open_create_return_value = gsfpy.bindings.gsfOpen(
            os.fsencode(tmp_file_path), file_mode, byref(file_ref)
        )

        bytes_written = gsfpy.bindings.gsfWrite(
            file_ref, byref(swath_summary_id), byref(records)
        )
        close_return_value = gsfpy.bindings.gsfClose(file_ref)

        assert_that(0).is_equal_to(open_create_return_value)
        assert_that(self.summary_record_length).is_equal_to(bytes_written)
        assert_that(0).is_equal_to(close_return_value)

        # Read it back out and check that it matches expected values
        gsf_file_ref = c_int(0)
        gsf_read_data_id = c_gsfDataID()
        gsf_read_data_id.recordID = RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING

        read_records = c_gsfRecords()

        open_read_return_value = gsfpy.bindings.gsfOpen(
            os.fsencode(tmp_file_path), FileMode.GSF_READONLY, byref(gsf_file_ref)
        )
        bytes_read = gsfpy.bindings.gsfRead(
            gsf_file_ref,
            RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY,
            byref(gsf_read_data_id),
            byref(read_records),
        )
        close_read_return_value = gsfpy.bindings.gsfClose(gsf_file_ref)

        assert_that(open_read_return_value).is_equal_to(0)
        assert_that(close_read_return_value).is_equal_to(0)
        assert_that(bytes_read).is_equal_to(self.summary_record_length)
        read_summary = read_records.summary

        read_start_time = read_summary.start_time.tv_sec
        read_end_time = read_summary.end_time.tv_sec

        assert_that(read_start_time).is_equal_to(ts_start.tv_sec)
        assert_that(read_end_time).is_equal_to(ts_end.tv_sec)
        assert_that(read_summary.min_depth).is_equal_to(
            self.summary_to_save["min_depth"]
        )
        assert_that(read_summary.max_depth).is_equal_to(
            self.summary_to_save["max_depth"]
        )
        assert_that(read_summary.min_latitude).is_equal_to(
            self.summary_to_save["min_lat"]
        )
        assert_that(read_summary.max_latitude).is_equal_to(
            self.summary_to_save["max_lat"]
        )
        assert_that(read_summary.min_longitude).is_equal_to(
            self.summary_to_save["min_long"]
        )
        assert_that(read_summary.max_longitude).is_equal_to(
            self.summary_to_save["max_long"]
        )
