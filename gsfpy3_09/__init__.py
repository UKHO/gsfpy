__author__ = """UK Hydrographic Office"""
__email__ = "datascienceandengineering@ukho.gov.uk"
__version__ = "1.7.0"

from ctypes import byref, c_int
from os import fsencode
from pathlib import Path
from typing import Optional, Tuple, Union

from gsfpy3_09.bindings import (
    gsfClose,
    gsfGetNumberRecords,
    gsfIntError,
    gsfOpen,
    gsfOpenBuffered,
    gsfRead,
    gsfSeek,
    gsfStringError,
    gsfWrite,
)
from gsfpy3_09.enums import FileMode, RecordType, SeekOption
from gsfpy3_09.gsfDataID import c_gsfDataID
from gsfpy3_09.gsfRecords import c_gsfRecords


class GsfException(Exception):
    """
    Generates an exception based on the last error code
    """

    def __init__(self):
        self._error_code = gsfIntError()
        self._error_message = gsfStringError().decode()
        super().__init__(f"[{self._error_code}] {self._error_message}")

    @property
    def error_code(self) -> int:
        return self._error_code

    @property
    def error_message(self) -> str:
        return self._error_message


class GsfFile:
    """
    Represents an open connection to a GSF file
    """

    def __init__(self, handle: c_int, file_mode: FileMode):
        self._handle = handle
        self._file_mode = file_mode

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def file_mode(self) -> FileMode:
        """
        Mode the file has been opened in
        """
        return self._file_mode

    def close(self):
        """
        Once this method has been called further operations will fail
        :raises GsfException: Raised if anything went wrong
        """
        _handle_failure(gsfClose(self._handle))

    def seek(self, option: SeekOption):
        """
        :param option: Where to seek to
        :raises GsfException: Raised if anything went wrong
        """
        _handle_failure(gsfSeek(self._handle, option))

    def read(
        self,
        desired_record: RecordType = RecordType.GSF_NEXT_RECORD,
        record_number: int = 0,
    ) -> Tuple[c_gsfDataID, c_gsfRecords]:
        """
        When the file is open in GSF_READONLY_INDEX or GSF_UPDATE_INDEX mode then the
        record_number parameter may be used to indicate which instance of the record to
        read.
        :param desired_record: Record type to read
        :param record_number: nth occurrence of the record to read from, starting from 1
        :return: Tuple of c_gsfDataID and c_gsfRecords
        :raises GsfException: Raised if anything went wrong
        """
        data_id = c_gsfDataID()
        data_id.record_number = record_number

        records = c_gsfRecords()

        _handle_failure(
            gsfRead(self._handle, desired_record, byref(data_id), byref(records))
        )

        return data_id, records

    def write(
        self, records: c_gsfRecords, record_type: RecordType, record_number: int = 0
    ) -> int:
        """
        When the file is open in GSF_UPDATE_INDEX mode then the record_number parameter
        may be used to indicate which instance of the record to write over.
        :param records: Data to write
        :param record_type: Specifies the type of record to write to
        :param record_number: nth occurrence of the record to write to, starting from 1
        :return: Number of bytes written
        :raises GsfException: Raised if anything went wrong
        """
        data_id = c_gsfDataID()
        data_id.recordID = record_type
        data_id.record_number = record_number

        bytesWritten = gsfWrite(self._handle, byref(data_id), byref(records))
        _handle_failure(bytesWritten)

        return bytesWritten

    def get_number_records(self, desired_record: RecordType) -> int:
        """
        May only be used when the file is open for direct access (GSF_READONLY_INDEX or
        GSF_UPDATE_INDEX).
        :param desired_record: Specifies the type of record to count
        :return: Number of records of type desired_record, otherwise -1
        """
        count = gsfGetNumberRecords(self._handle, desired_record)
        _handle_failure(count)
        return count


def open_gsf(
    path: Union[str, Path],
    mode: FileMode = FileMode.GSF_READONLY,
    buffer_size: Optional[int] = None,
) -> GsfFile:
    """
    Factory function to create GsfFile objects
    :param path: Location of GSF file to open
    :param mode: Mode to open the file in (read-only by default)
    :param buffer_size: If a value is provided then a buffer will be used to read the
                        file
    :return: Object representing the open connection to the specified file
    :raises GsfException: Raised if anything went wrong
    """
    handle = c_int(0)

    if isinstance(path, Path):
        path = str(path)

    _handle_failure(
        gsfOpen(fsencode(path), mode, byref(handle))
        if buffer_size is None
        else gsfOpenBuffered(path.encode(), mode, byref(handle), buffer_size)
    )

    return GsfFile(handle, mode)


_ERROR_CODE = -1


def _handle_failure(return_code: int):
    """
    Error handling logic
    :param return_code: The return code from one of functions in the gsfpy3_09.bindings
                        package
    """
    if return_code == _ERROR_CODE:
        raise GsfException()
