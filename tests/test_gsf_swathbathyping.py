import os
import shutil
import tempfile
import unittest
from ctypes import *
from os import path

import assertpy

import gsfpy
from gsfpy.enums import FileMode, RecordType, SeekOption
from gsfpy.gsfDataID import c_gsfDataID
from gsfpy.gsfRecords import c_gsfRecords


class TestGsfSwathBathyPing(unittest.TestCase):

    def setUp(self):
        test_data_306_path = path.join(os.fsencode(path.dirname(__file__)),
                                       b"0029_20160323_185603_EX1604_MB.gsf.mb121")
        self.test_data_306_path = test_data_306_path
        self.test_data_306 = (test_data_306_path, 432)

    def tearDown(self):
        temp_gsf_files = [f for f in os.listdir(tempfile.gettempdir()) if f.startswith('temp_gsf')]
        for gsf_file in temp_gsf_files:
            try:
                os.remove(path.join(tempfile.gettempdir(), gsf_file))
            except IOError as io_err:
                print(f'Unable to delete temp file {gsf_file} : {str(io_err)}')

    def test_gsf_swathbathyping_read(self):
        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))
        # Read the SwathBathyPing records
        open_ret_val = gsfpy.gsfOpen(self.test_data_306_path, FileMode.GSF_READONLY, p_gsf_fileref)
        self.assertEqual(open_ret_val, 0)

        gsf_data_id = c_gsfDataID()
        gsf_data_id.recordID = c_uint(RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING.value)

        c_gsfDataID_ptr = POINTER(c_gsfDataID)
        p_dataID = c_gsfDataID_ptr(gsf_data_id)

        c_gsfRecords_ptr = POINTER(c_gsfRecords)
        p_records = c_gsfRecords_ptr(c_gsfRecords())

        bytes_read = gsfpy.gsfRead(
                                    c_int(p_gsf_fileref[0]),
                                    RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
                                    p_dataID,
                                    p_records
                                    )
        close_ret_val = gsfpy.gsfClose(c_int(p_gsf_fileref[0]))
        assertpy.assert_that(close_ret_val).is_equal_to(0)

        swath_bathymetry_ping_record = p_records.contents.mb_ping

        num_beams = swath_bathymetry_ping_record.number_beams

        assertpy.assert_that(bytes_read).is_greater_than(0)
        assertpy.assert_that(num_beams).is_equal_to(self.test_data_306[1])
        beam_angles = swath_bathymetry_ping_record.beam_angle[:num_beams]

        beam_angles_in_range = [180 >= x >= -180 for x in beam_angles]
        assertpy.assert_that(False).is_not_in(beam_angles_in_range)

    def test_gsf_swathbathyping_write_update(self):
        tmp_file_path = '/tmp/temp_gsf_306_test_data_update.gsf'
        shutil.copyfile(self.test_data_306_path, tmp_file_path)

        c_int_ptr = POINTER(c_int)
        p_gsf_fileref = c_int_ptr(c_int(0))

        open_ret_val = gsfpy.gsfOpen(self.test_data_306_path, FileMode.GSF_UPDATE, p_gsf_fileref)
        self.assertEqual(open_ret_val, 0)

        gsf_data_id = c_gsfDataID()
        gsf_data_id.recordID = c_uint(RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING.value)

        c_gsfDataID_ptr = POINTER(c_gsfDataID)
        p_data_id = c_gsfDataID_ptr(gsf_data_id)

        c_gsfRecords_ptr = POINTER(c_gsfRecords)
        p_records = c_gsfRecords_ptr(c_gsfRecords())

        bytes_read = gsfpy.gsfRead(
                                    c_int(p_gsf_fileref[0]),
                                    RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
                                    p_data_id,
                                    p_records
                                    )
        self.assertTrue(bytes_read > 0)

        swath_bathymetry_ping_record = p_records.contents.mb_ping
        num_beams = swath_bathymetry_ping_record.number_beams

        assertpy.assert_that(num_beams).is_equal_to(self.test_data_306[1])

        original_values = swath_bathymetry_ping_record.beam_flags[:num_beams]

        update_beams = {'3': 1, '4': 9, '5': 9, '6': 9}
        for i in update_beams.keys():
            swath_bathymetry_ping_record.beam_flags[int(i)] = c_ubyte(update_beams[i])

        seek_return_value = gsfpy.bindings.gsfSeek(c_int(p_gsf_fileref[0]), SeekOption.GSF_PREVIOUS_RECORD)
        bytes_written = gsfpy.bindings.gsfWrite(c_int(p_gsf_fileref[0]), p_data_id, p_records)
        close_return_value = gsfpy.bindings.gsfClose(c_int(p_gsf_fileref[0]))
        assertpy.assert_that(seek_return_value).is_equal_to(0)
        assertpy.assert_that(close_return_value).is_equal_to(0)
        assertpy.assert_that(bytes_written).is_greater_than(0)

        p_gsf_read_file_ref = c_int_ptr(c_int(0))
        open_ret_val = gsfpy.gsfOpen(self.test_data_306_path, FileMode.GSF_READONLY, p_gsf_read_file_ref)
        gsf_read_data_id = c_gsfDataID()
        gsf_read_data_id.recordID = c_uint(RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING.value)
        p_read_data_id = c_gsfDataID_ptr(gsf_read_data_id)
        p_read_records = c_gsfRecords_ptr(c_gsfRecords())

        bytes_read = gsfpy.gsfRead(
                                    c_int(p_gsf_read_file_ref[0]),
                                    RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
                                    p_read_data_id,
                                    p_read_records)
        close_return_value = gsfpy.bindings.gsfClose(c_int(p_gsf_read_file_ref[0]))

        assertpy.assert_that(open_ret_val).is_equal_to(0)
        assertpy.assert_that(bytes_written).is_equal_to(bytes_read)
        assertpy.assert_that(close_return_value).is_equal_to(0)

        read_ping_record = p_read_records.contents.mb_ping

        for i in range(read_ping_record.number_beams):
            if str(i) in update_beams.keys():
                self.assertEqual(update_beams[str(i)], read_ping_record.beam_flags[i])
            else:
                self.assertEqual(original_values[i], read_ping_record.beam_flags[i])
