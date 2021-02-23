import tempfile
from ctypes import c_int, create_string_buffer, string_at
from os import path

from assertpy import assert_that

from gsfpy3_09 import GsfException, open_gsf
from gsfpy3_09.enums import FileMode, RecordType, SeekOption
from gsfpy3_09.gsfRecords import c_gsfRecords


def test_open_gsf_success(gsf_test_data_03_09):
    """
    Open the test GSF file, then close.
    """
    # Act
    with open_gsf(gsf_test_data_03_09.path) as _:
        pass


def test_open_gsf_buffered_success(gsf_test_data_03_09):
    """
    Open the test GSF file in buffered mode, then close.
    """
    # Act
    with open_gsf(gsf_test_data_03_09.path, buffer_size=100) as _:
        pass


def test_seek_success(gsf_test_data_03_09):
    """
    Open the test GSF file, seek to end of file, then close.
    """
    # Act
    with open_gsf(gsf_test_data_03_09.path) as gsf_file:
        gsf_file.seek(SeekOption.GSF_END_OF_FILE)


def test_GsfException(gsf_test_data_03_09):
    """
    Try to open a non-existent GSF file, ensure a GsfException is raised and check
    that it contains the correct error code and error message.
    """
    # Assert
    assert_that(open_gsf).raises(GsfException).when_called_with(
        "non-existent.gsf"
    ).is_equal_to("[-1] GSF Error: Unable to open requested file")


def test_read_success(gsf_test_data_03_09):
    """
    Read a comment record from a GSF file.
    """
    # Act
    with open_gsf(gsf_test_data_03_09.path) as gsf_file:
        _, record = gsf_file.read(RecordType.GSF_RECORD_COMMENT)

    # Assert
    assert_that(string_at(record.comment.comment)).is_equal_to(b"My comment")


def test_read_buffered_success(gsf_test_data_03_09):
    """
    Read a comment record from a GSF file using a buffer.
    """
    # Act
    with open_gsf(gsf_test_data_03_09.path, buffer_size=1) as gsf_file:
        _, record = gsf_file.read(RecordType.GSF_RECORD_COMMENT)

    # Assert
    assert_that(string_at(record.comment.comment)).is_equal_to(b"My comment")


def test_write_success(gsf_test_data_03_09):
    """
    Write a single comment record to a new GSF file
    """
    # Arrange
    tmp_gsf_file_path = path.join(tempfile.gettempdir(), "temp.gsf")

    comment = b"My first comment"
    # Act
    with open_gsf(tmp_gsf_file_path, mode=FileMode.GSF_CREATE) as gsf_file:
        gsf_file.write(_new_comment(comment), RecordType.GSF_RECORD_COMMENT)

    # Assert
    # Read comment from newly created file to check it is as expected
    with open_gsf(tmp_gsf_file_path) as gsf_file:
        _, record = gsf_file.read(RecordType.GSF_RECORD_COMMENT)

    assert_that(string_at(record.comment.comment)).is_equal_to(comment)


def test_direct_access_write_and_read_success(tmp_path):
    """
    Create, update and read. First sequentially, then using direct access
    """
    tmp_gsf_file_path = tmp_path / "temp.gsf"

    # Create a file with 3 records
    comment_1 = b"Comment #1"
    comment_2 = b"Comment #2"
    comment_3 = b"Comment #3"
    comment_4 = b"Comment #4"

    # Write sequentially
    with open_gsf(tmp_gsf_file_path, mode=FileMode.GSF_CREATE) as gsf_file:
        gsf_file.write(_new_comment(comment_1), RecordType.GSF_RECORD_COMMENT)
        gsf_file.write(_new_comment(comment_2), RecordType.GSF_RECORD_COMMENT)
        gsf_file.write(_new_comment(comment_3), RecordType.GSF_RECORD_COMMENT)

    # Update using direct access
    with open_gsf(tmp_gsf_file_path, mode=FileMode.GSF_UPDATE_INDEX) as gsf_file:
        gsf_file.write(_new_comment(comment_4), RecordType.GSF_RECORD_COMMENT, 2)

    # Read sequentially
    with open_gsf(tmp_gsf_file_path) as gsf_file:
        _, record_1 = gsf_file.read()
        assert_that(string_at(record_1.comment.comment)).is_equal_to(comment_1)

        _, record_2 = gsf_file.read()
        assert_that(string_at(record_2.comment.comment)).is_equal_to(comment_4)

        _, record_3 = gsf_file.read()
        assert_that(string_at(record_3.comment.comment)).is_equal_to(comment_3)

        assert_that(gsf_file.read).raises(GsfException).when_called_with().is_equal_to(
            "[-23] GSF Error: End of file encountered"
        )

    # Read using direct access
    with open_gsf(tmp_gsf_file_path, mode=FileMode.GSF_READONLY_INDEX) as gsf_file:
        _, direct_access_record = gsf_file.read(RecordType.GSF_RECORD_COMMENT, 2)

    assert_that(string_at(direct_access_record.comment.comment)).is_equal_to(comment_4)


def test_get_number_records_success(gsf_test_data_03_09):
    """
    Open the test GSF file in GSF_READONLY_INDEX mode, count the number of
    GSF_RECORD_SWATH_BATHYMETRY_PING records, then close.
    """
    # Act
    with open_gsf(gsf_test_data_03_09.path, FileMode.GSF_READONLY_INDEX) as gsf_file:
        number_of_pings = gsf_file.get_number_records(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
        )

    assert_that(number_of_pings).is_equal_to(3)


def test_get_number_records_failure(gsf_test_data_03_09):
    """
    Open the test GSF file in GSF_READONLY mode, attempt to count the number of
    GSF_RECORD_SWATH_BATHYMETRY_PING records and verify the exception.
    """
    # Act
    with open_gsf(gsf_test_data_03_09.path) as gsf_file:
        assert_that(gsf_file.get_number_records).raises(GsfException).when_called_with(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
        ).is_equal_to("[-3] GSF Error: Illegal access mode")


def _new_comment(comment: bytes) -> c_gsfRecords:
    record = c_gsfRecords()
    record.comment.comment_time.tvsec = c_int(1000)
    record.comment.comment_length = c_int(len(comment))
    record.comment.comment = create_string_buffer(comment)
    return record
