__author__ = """UK Hydrographic Office"""
__email__ = "datascienceandengineering@ukho.gov.uk"
__version__ = "1.0.0"

from ctypes import byref, c_int
from typing import Optional, Tuple

from gsfpy.bindings import (
    gsfClose,
    gsfIntError,
    gsfOpen,
    gsfOpenBuffered,
    gsfRead,
    gsfSeek,
    gsfStringError,
    gsfWrite,
)
from gsfpy.enums import FileMode, RecordType, SeekOption
from gsfpy.gsfDataID import c_gsfDataID
from gsfpy.gsfRecords import c_gsfRecords


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

    def read(self, desired_record: RecordType) -> Tuple[c_gsfDataID, c_gsfRecords]:
        """
        :param desired_record: Record type or id to read
        :return: Tuple of c_gsfDataID and c_gsfRecords
        :raises GsfException: Raised if anything went wrong
        """
        data_id = c_gsfDataID()
        records = c_gsfRecords()

        _handle_failure(
            gsfRead(self._handle, desired_record, byref(data_id), byref(records))
        )

        return data_id, records

    def direct_read(
        self, desired_record: RecordType, record_number: int
    ) -> Tuple[c_gsfDataID, c_gsfRecords]:
        """
        For use when the file is open in GSF_READONLY_INDEX or GSF_UPDATE_INDEX mode
        :param desired_record: Record type or id to read
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

    def write(self, record_type: RecordType, records: c_gsfRecords):
        """
        For use when the file is open in GSF_CREATE, GSF_UPDATE or GSF_UPDATE_INDEX mode
        :param record_type: Specifies the type of record to write
        :param records: Data to write
        :raises GsfException: Raised if anything went wrong
        """
        data_id = c_gsfDataID()
        data_id.recordID = record_type

        _handle_failure(gsfWrite(self._handle, byref(data_id), byref(records)))

    def direct_write(
        self, record_type: RecordType, record_number: int, records: c_gsfRecords
    ):
        """
        For use when the file is open in GSF_UPDATE_INDEX mode
        :param record_type: Specifies the type of record to write to
        :param record_number: nth occurrence of the record to write to, starting from 1
        :param records: Data to write
        :raises GsfException: Raised if anything went wrong
        """
        data_id = c_gsfDataID()
        data_id.recordID = record_type
        data_id.record_number = record_number

        _handle_failure(gsfWrite(self._handle, byref(data_id), byref(records)))


def open_gsf(
    path: str, mode: FileMode = FileMode.GSF_READONLY, buffer_size: Optional[int] = None
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

    _handle_failure(
        gsfOpen(path.encode(), mode, byref(handle))
        if buffer_size is None
        else gsfOpenBuffered(path.encode(), mode, byref(handle), buffer_size)
    )

    return GsfFile(handle, mode)


_ERROR_CODE = -1


def _handle_failure(return_code: int):
    """
    Error handling logic
    :param return_code: The return code from one of functions in the gsfpy.bindings
                        package
    """
    if return_code == _ERROR_CODE:
        raise GsfException()
