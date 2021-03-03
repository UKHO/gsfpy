import os
from ctypes import byref, c_int, c_int32, c_long
from dataclasses import dataclass

from assertpy import assert_that

import gsfpy3_08
from gsfpy3_08.enums import FileMode, RecordType, SeekOption
from gsfpy3_08.gsfDataID import c_gsfDataID
from gsfpy3_08.gsfRecords import c_gsfRecords
from gsfpy3_08.gsfSwathBathySummary import c_gsfSwathBathySummary
from gsfpy3_08.timespec import c_timespec
from tests.gsfpy3_08.conftest import GsfDatafile

SUMMARY_RECORD_LENGTH = 48  # (bytes)


@dataclass(frozen=True)
class SummaryRecord:
    min_lat: float
    max_lat: float
    min_long: float
    max_long: float
    min_depth: float
    max_depth: float
    start_time_sec: int
    start_time_nsec: int
    end_time_sec: int
    end_time_nsec: int

    @property
    def start_time(self):
        return c_timespec(
            tv_sec=c_int32(self.start_time_sec), tv_nsec=c_long(self.start_time_nsec)
        )

    @property
    def end_time(self):
        return c_timespec(
            tv_sec=c_int32(self.end_time_sec), tv_nsec=c_long(self.end_time_nsec)
        )

    def to_summary(self, summary: c_gsfSwathBathySummary):
        summary.min_latitude = self.min_lat
        summary.max_latitude = self.max_lat
        summary.min_longitude = self.min_long
        summary.max_longitude = self.max_long
        summary.max_depth = self.max_depth
        summary.min_depth = self.min_depth
        summary.start_time = self.start_time
        summary.end_time = self.end_time

    @staticmethod
    def from_summary(summary: c_gsfSwathBathySummary) -> "SummaryRecord":
        return SummaryRecord(
            min_lat=summary.min_latitude,
            max_lat=summary.max_latitude,
            min_long=summary.min_longitude,
            max_long=summary.max_longitude,
            max_depth=summary.max_depth,
            min_depth=summary.min_depth,
            start_time_sec=summary.start_time.tv_sec,
            start_time_nsec=summary.start_time.tv_nsec,
            end_time_sec=summary.end_time.tv_sec,
            end_time_nsec=summary.end_time.tv_nsec,
        )


SUMMARY_RECORD = SummaryRecord(
    min_lat=-14.02349,
    max_lat=34.089,
    min_long=3.089234,
    max_long=3.235,
    min_depth=3.23,
    max_depth=93.23,
    start_time_sec=1_500_000_000,
    start_time_nsec=506,
    end_time_sec=1_500_001_000,
    end_time_nsec=509,
)


def test_gsf_swath_summary(gsf_test_data_03_08: GsfDatafile):
    file_handle = c_int(0)

    swath_summary_id = c_gsfDataID()
    swath_summary_id.recordID = RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY

    records = c_gsfRecords()

    # Read from file
    return_value = gsfpy3_08.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_08.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy3_08.bindings.gsfRead(
        file_handle,
        RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY,
        byref(swath_summary_id),
        byref(records),
    )
    assert_that(bytes_read).is_equal_to(SUMMARY_RECORD_LENGTH)

    return_value = gsfpy3_08.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    assert_that(SummaryRecord.from_summary(records.summary)).is_equal_to(
        SummaryRecord(
            min_lat=8.7118203,
            max_lat=8.713543,
            min_long=167.4759106,
            max_long=167.477003,
            min_depth=3862.43,
            max_depth=4145.0,
            start_time_sec=1458759363,
            start_time_nsec=224999904,
            end_time_sec=1458759436,
            end_time_nsec=727999925,
        )
    )


def test_gsf_swath_summary_save_update(gsf_test_data_03_08: GsfDatafile):
    file_handle = c_int(0)

    swath_summary_data_id = c_gsfDataID()
    swath_summary_data_id.recordID = RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY

    record = c_gsfRecords()

    return_value = gsfpy3_08.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_08.path)),
        FileMode.GSF_UPDATE,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy3_08.bindings.gsfRead(
        file_handle,
        RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY,
        byref(swath_summary_data_id),
        byref(record),
    )
    assert_that(bytes_read).is_equal_to(SUMMARY_RECORD_LENGTH)

    assert_that(SummaryRecord.from_summary(record.summary)).is_not_equal_to(
        SUMMARY_RECORD
    )

    # copy our data into the record
    SUMMARY_RECORD.to_summary(record.summary)

    # Go back to the first record so it doesn't write
    # the updated first summary over the top of the second one
    return_value = gsfpy3_08.bindings.gsfSeek(
        file_handle, SeekOption.GSF_PREVIOUS_RECORD
    )
    assert_that(return_value).is_zero()

    bytes_written = gsfpy3_08.bindings.gsfWrite(
        file_handle, byref(swath_summary_data_id), byref(record)
    )
    assert_that(bytes_written).is_equal_to(SUMMARY_RECORD_LENGTH)

    return_value = gsfpy3_08.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Read it back out and check it was saved correctly

    file_handle = c_int(0)
    updated_swath_summary_data_id = c_gsfDataID()
    updated_swath_summary_data_id.recordID = RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY

    updated_record = c_gsfRecords()

    return_value = gsfpy3_08.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_08.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy3_08.bindings.gsfRead(
        file_handle,
        RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY,
        byref(updated_swath_summary_data_id),
        byref(updated_record),
    )
    assert_that(bytes_read).is_equal_to(SUMMARY_RECORD_LENGTH)

    return_value = gsfpy3_08.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    assert_that(SummaryRecord.from_summary(updated_record.summary)).is_equal_to(
        SUMMARY_RECORD
    )


def test_gsf_swath_summary_save_create(gsf_test_data_03_08: GsfDatafile):
    file_handle = c_int(0)

    swath_summary_id = c_gsfDataID()
    swath_summary_id.recordID = RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY

    record = c_gsfRecords()
    record.summary = c_gsfSwathBathySummary(
        start_time=SUMMARY_RECORD.start_time,
        end_time=SUMMARY_RECORD.end_time,
        min_latitude=SUMMARY_RECORD.min_lat,
        max_latitude=SUMMARY_RECORD.max_lat,
        min_longitude=SUMMARY_RECORD.min_long,
        max_longitude=SUMMARY_RECORD.max_long,
        min_depth=SUMMARY_RECORD.min_depth,
        max_depth=SUMMARY_RECORD.max_depth,
    )

    return_value = gsfpy3_08.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_08.path)),
        FileMode.GSF_CREATE,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_written = gsfpy3_08.bindings.gsfWrite(
        file_handle, byref(swath_summary_id), byref(record)
    )
    assert_that(bytes_written).is_equal_to(SUMMARY_RECORD_LENGTH)

    return_value = gsfpy3_08.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    # Read it back out and check that it matches expected values
    file_handle = c_int(0)
    gsf_read_data_id = c_gsfDataID()
    gsf_read_data_id.recordID = RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING

    written_record = c_gsfRecords()

    return_value = gsfpy3_08.bindings.gsfOpen(
        os.fsencode(str(gsf_test_data_03_08.path)),
        FileMode.GSF_READONLY,
        byref(file_handle),
    )
    assert_that(return_value).is_zero()

    bytes_read = gsfpy3_08.bindings.gsfRead(
        file_handle,
        RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY,
        byref(gsf_read_data_id),
        byref(written_record),
    )
    assert_that(bytes_read).is_equal_to(SUMMARY_RECORD_LENGTH)

    return_value = gsfpy3_08.bindings.gsfClose(file_handle)
    assert_that(return_value).is_zero()

    assert_that(SummaryRecord.from_summary(written_record.summary)).is_equal_to(
        SUMMARY_RECORD
    )
