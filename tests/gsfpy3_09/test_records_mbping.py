import os
from ctypes import byref, c_int, c_ubyte

from assertpy import assert_that

import gsfpy3_09
from gsfpy3_09 import c_gsfDataID, c_gsfRecords
from gsfpy3_09.enums import FileMode, RecordType, SeekOption
from tests.gsfpy3_09.conftest import GsfDatafile


def test_read(gsf_test_data: GsfDatafile):
    with gsfpy3_09.open_gsf(gsf_test_data.path, FileMode.GSF_READONLY) as gsf_file:
        _, record = gsf_file.read(RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING, 1)

    assert_that(record.mb_ping.number_beams).is_equal_to(gsf_test_data.num_beams)

    for i in range(record.mb_ping.number_beams):
        # fmt: off
        assert_that(record.mb_ping.depth[i]) \
            .described_as(f"depth[{i}]") \
            .is_greater_than(0)
        # fmt: on


def test_write_update_sequential(gsf_test_data: GsfDatafile):
    with gsfpy3_09.open_gsf(gsf_test_data.path, FileMode.GSF_UPDATE) as gsf_file:
        _, record = gsf_file.read(RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING)

        orig_beam_flags = record.mb_ping.beam_flags[: record.mb_ping.number_beams]

        beam_flag_updates = {3: 1, 4: 1, 5: 1, 6: 1}
        for i, value in beam_flag_updates.items():
            record.mb_ping.beam_flags[i] = c_ubyte(value)

        gsf_file.seek(SeekOption.GSF_PREVIOUS_RECORD)
        gsf_file.write(record, RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING)

    with gsfpy3_09.open_gsf(
        gsf_test_data.path, FileMode.GSF_READONLY
    ) as reopened_gsf_file:
        _, updated_record = reopened_gsf_file.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
        )

    for i in range(updated_record.mb_ping.number_beams):
        if i in beam_flag_updates:
            assert_that(updated_record.mb_ping.beam_flags[i]).is_equal_to(
                beam_flag_updates[i]
            )
        else:
            assert_that(updated_record.mb_ping.beam_flags[i]).is_equal_to(
                orig_beam_flags[i]
            )


def test_update_by_index(gsf_test_data: GsfDatafile):
    first_record_index = 1
    third_record_index = 3
    with gsfpy3_09.open_gsf(gsf_test_data.path, FileMode.GSF_UPDATE_INDEX) as gsf_file:
        _, record = gsf_file.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING, third_record_index
        )

        orig_beam_flags = record.mb_ping.beam_flags[: record.mb_ping.number_beams]

        beam_flag_updates = {3: 1, 4: 1, 5: 1, 6: 1}
        for i, value in beam_flag_updates.items():
            record.mb_ping.beam_flags[i] = c_ubyte(value)

        gsf_file.write(
            record, RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING, third_record_index
        )

    with gsfpy3_09.open_gsf(
        gsf_test_data.path, FileMode.GSF_READONLY_INDEX
    ) as reopened_gsf_file:
        _, read_gsf_records = reopened_gsf_file.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING, third_record_index
        )

        read_ping_record = read_gsf_records.mb_ping
        updated_flags = read_ping_record.beam_flags[: record.mb_ping.number_beams]

        for i in range(read_ping_record.number_beams):
            if i in beam_flag_updates:
                assert_that(beam_flag_updates[i]).is_equal_to(
                    read_ping_record.beam_flags[i]
                )
            else:
                assert_that(orig_beam_flags[i]).is_equal_to(
                    read_ping_record.beam_flags[i]
                )

        _, first_gsf_records = reopened_gsf_file.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING, first_record_index
        )

    first_rec_flags = first_gsf_records.mb_ping.beam_flags[
        : record.mb_ping.number_beams
    ]
    assert_that(updated_flags).is_not_equal_to(first_rec_flags)


def test_read_by_index(gsf_test_data: GsfDatafile):
    with gsfpy3_09.open_gsf(
        gsf_test_data.path, FileMode.GSF_READONLY
    ) as gsf_file_by_seq:
        # Read a couple of records forwards, so its at position 3.
        # Records are 1-indexed.
        # This is using read because Seek only does start/end/previous not next.
        gsf_file_by_seq.read(RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING)
        gsf_file_by_seq.read(RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING)
        _, third_record_by_seq = gsf_file_by_seq.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
        )

    with gsfpy3_09.open_gsf(
        gsf_test_data.path, FileMode.GSF_READONLY_INDEX
    ) as gsf_file_by_idx:
        _, third_record_by_idx = gsf_file_by_idx.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING, 3
        )

    number_beams_by_seq = third_record_by_seq.mb_ping.number_beams
    number_beams_by_idx = third_record_by_idx.mb_ping.number_beams
    assert_that(number_beams_by_seq).is_equal_to(number_beams_by_idx)

    depth_by_seq = third_record_by_seq.mb_ping.depth[:number_beams_by_seq]
    depth_by_idx = third_record_by_idx.mb_ping.depth[:number_beams_by_idx]
    assert_that(depth_by_seq).is_equal_to(depth_by_idx)

    beam_flags_by_seq = third_record_by_seq.mb_ping.beam_flags[:number_beams_by_seq]
    beam_flags_by_idx = third_record_by_idx.mb_ping.beam_flags[:number_beams_by_idx]
    assert_that(beam_flags_by_seq).is_equal_to(beam_flags_by_idx)


def test_low_level_read(gsf_test_data: GsfDatafile):
    mode = FileMode.GSF_READONLY
    gsf_file_ref = c_int(0)

    gsf_data_id = c_gsfDataID()
    gsf_data_id.recordID = RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING

    record = c_gsfRecords()

    open_return_value = gsfpy3_09.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data.path)), mode, byref(gsf_file_ref)
    )
    bytes_read = gsfpy3_09.bindings.gsfRead(
        gsf_file_ref,
        RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
        byref(gsf_data_id),
        byref(record),
    )
    close_return_value = gsfpy3_09.bindings.gsfClose(gsf_file_ref)

    assert_that(open_return_value).is_zero()
    assert_that(close_return_value).is_zero()
    assert_that(bytes_read).is_positive()

    for i in range(record.mb_ping.number_beams):
        # fmt: off
        assert_that(record.mb_ping.depth[i]) \
            .described_as(f"depth[{i}]") \
            .is_greater_than(0)
        # fmt: on
