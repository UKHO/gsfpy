from ctypes import POINTER, Structure, c_char

from . import timespec

GSF_HOST_NAME_LENGTH = 64
GSF_OPERATOR_LENGTH = 64
HISTORY_HOST_NAME = c_char * (GSF_HOST_NAME_LENGTH + 1)
HISTORY_OPERATOR_NAME = c_char * (GSF_OPERATOR_LENGTH + 1)


class c_gsfHistory(Structure):
    _fields_ = [
        ("history_time", timespec.c_timespec),
        ("host_name", HISTORY_HOST_NAME),
        ("operator_name", HISTORY_OPERATOR_NAME),
        ("command_line", POINTER(c_char)),
        ("comment", POINTER(c_char)),
    ]
