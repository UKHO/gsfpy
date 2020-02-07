from ctypes import Structure, c_char, c_char_p

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
        ("command_line", c_char_p),
        ("comment", c_char_p),
    ]
