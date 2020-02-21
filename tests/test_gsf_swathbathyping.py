import os
import shutil
import tempfile
import unittest
from ctypes import c_ubyte
from os import path

import assertpy

import gsfpy
from gsfpy.enums import FileMode, RecordType, SeekOption


class TestGsfSwathBathyPing(unittest.TestCase):

    def setUp(self):
        test_data_306_path = path.join(path.dirname(__file__),
                                       "0029_20160323_185603_EX1604_MB.gsf.mb121")
        self.test_data_306 = {'path': test_data_306_path, 'num_beams': 432}
        test_data_307_path = path.join(path.dirname(__file__),
                                       "0059_20181102_212138_EX1811_MB_EM302.gsf.mb121")
        self.test_data_307 = {'path': test_data_307_path, 'num_beams': 432}

    def tearDown(self):
        tmp_files = os.listdir(tempfile.gettempdir())
        temp_gsf_files = [f for f in tmp_files if f.startswith('temp_gsf')]
        for gsf_file in temp_gsf_files:
            try:
                os.remove(path.join(tempfile.gettempdir(), gsf_file))
            except IOError as io_err:
                print(f'Unable to delete temp file {gsf_file} : {str(io_err)}')

    def test_gsf_swathbathyping_read(self):
        gsf_file = gsfpy.open_gsf(self.test_data_306['path'], FileMode.GSF_READONLY)
        data_id, gsf_records = gsf_file.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            1
        )
        gsf_file.close()

        swath_bathymetry_ping_record = gsf_records.mb_ping

        num_beams = swath_bathymetry_ping_record.number_beams

        assertpy.assert_that(num_beams).is_equal_to(self.test_data_306['num_beams'])
        beam_angles = swath_bathymetry_ping_record.beam_angle[:num_beams]

        beam_angles_in_range = [180 >= x >= -180 for x in beam_angles]
        assertpy.assert_that(False).is_not_in(beam_angles_in_range)

    def test_gsf_swathbathyping_write_update_sequential(self):
        tmp_file_path = '/tmp/temp_gsf_306_test_data_update.gsf'
        shutil.copyfile(self.test_data_306['path'], tmp_file_path)
        gsf_file = gsfpy.open_gsf(tmp_file_path, FileMode.GSF_UPDATE)
        record_num = 0
        data_id, gsf_records = gsf_file.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            record_num)

        num_beams = gsf_records.mb_ping.number_beams

        assertpy.assert_that(num_beams).is_equal_to(self.test_data_306['num_beams'])

        original_values = gsf_records.mb_ping.beam_flags[:num_beams]

        update_beams = {'3': 1, '4': 1, '5': 1, '6': 1}
        for i in update_beams.keys():
            gsf_records.mb_ping.beam_flags[int(i)] = c_ubyte(update_beams[i])

        gsf_file.seek(SeekOption.GSF_PREVIOUS_RECORD)
        gsf_file.write(gsf_records,
                       RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
                       record_num)
        gsf_file.close()

        reopened_gsf_file = gsfpy.open_gsf(tmp_file_path, FileMode.GSF_READONLY)
        read_data_id, read_gsf_records = reopened_gsf_file.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            record_num
        )
        read_ping_record = read_gsf_records.mb_ping

        for i in range(read_ping_record.number_beams):
            if str(i) in update_beams.keys():
                self.assertEqual(update_beams[str(i)], read_ping_record.beam_flags[i])
            else:
                self.assertEqual(original_values[i], read_ping_record.beam_flags[i])

    def test_gsf_swathbathyping_update_by_index(self):
        tmp_file_path = '/tmp/temp_gsf_306_test_data_update_idx.gsf'
        shutil.copyfile(self.test_data_306['path'], tmp_file_path)
        gsf_file = gsfpy.open_gsf(tmp_file_path, FileMode.GSF_UPDATE_INDEX)
        record_num = 3
        data_id, gsf_records = gsf_file.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            record_num)

        num_beams = gsf_records.mb_ping.number_beams

        assertpy.assert_that(num_beams).is_equal_to(self.test_data_306['num_beams'])

        original_values = gsf_records.mb_ping.beam_flags[:num_beams]

        update_beams = {'3': 1, '4': 1, '5': 1, '6': 1}
        for i in update_beams.keys():
            gsf_records.mb_ping.beam_flags[int(i)] = c_ubyte(update_beams[i])

        gsf_file.write(gsf_records,
                       RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
                       record_num)
        gsf_file.close()

        reopened_gsf_file = gsfpy.open_gsf(tmp_file_path, FileMode.GSF_READONLY_INDEX)
        read_data_id, read_gsf_records = reopened_gsf_file.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            record_num
        )
        read_ping_record = read_gsf_records.mb_ping
        updated_flags = read_ping_record.beam_flags[:num_beams]

        for i in range(read_ping_record.number_beams):
            if str(i) in update_beams.keys():
                self.assertEqual(update_beams[str(i)], read_ping_record.beam_flags[i])
            else:
                self.assertEqual(original_values[i], read_ping_record.beam_flags[i])

        first_data_id, first_gsf_records = reopened_gsf_file.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            1  # 1-indexed
        )
        first_rec_flags = first_gsf_records.mb_ping.beam_flags[:num_beams]
        self.assertNotEqual(first_rec_flags, updated_flags)

    # Reading by index on files created with different GSF versions
    def test_gsf_read_swathbathyping_by_index_306(self):
        self._gsf_swathbathyping_read_by_index(self.test_data_306)

    def test_gsf_read_swathbathyping_by_index_307(self):
        self._gsf_swathbathyping_read_by_index(self.test_data_307)

    def _gsf_swathbathyping_read_by_index(self, test_data_info):
        gsf_file = gsfpy.open_gsf(test_data_info['path'], FileMode.GSF_READONLY)

        # Read a couple of records forwards, so its at position 3.
        # Records are 1-indexed.
        # This is using read because Seek only does start/end/previous not next.
        record_index = 3
        gsf_file.read(RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING)
        gsf_file.read(RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING)

        data_id, gsf_records = gsf_file.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
        )
        gsf_file.close()

        swath_bathymetry_ping_record = gsf_records.mb_ping

        num_beams = swath_bathymetry_ping_record.number_beams

        assertpy.assert_that(num_beams).is_equal_to(test_data_info['num_beams'])
        beam_angles = swath_bathymetry_ping_record.beam_angle[:num_beams]
        beam_flags = swath_bathymetry_ping_record.beam_flags[:num_beams]

        gsf_file_by_index = gsfpy.open_gsf(test_data_info['path'],
                                           FileMode.GSF_READONLY_INDEX)
        index_data_id, gsf_index_records = gsf_file_by_index.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            record_index
        )

        record_by_index = gsf_index_records.mb_ping
        beam_angles_by_index = record_by_index.beam_angle[:num_beams]
        beam_flags_by_index = record_by_index.beam_flags[:num_beams]

        num_beams_from_index = record_by_index.number_beams
        assertpy.assert_that(num_beams).is_equal_to(num_beams_from_index)
        self.assertSequenceEqual(beam_angles, beam_angles_by_index)
        self.assertSequenceEqual(beam_flags, beam_flags_by_index)
