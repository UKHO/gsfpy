
from ctypes import *

from . import timespec

GSF_HOST_NAME_LENGTH = 64
GSF_OPERATOR_LENGTH = 64
HISTORYHOSTNAME = c_char * (GSF_HOST_NAME_LENGTH + 1)
HISTORYOPERATORNAME = c_char * (GSF_OPERATOR_LENGTH + 1)

class c_gsfHistory(Structure):
    _fields_ = [('history_time',            timespec.c_timespec),
                ('host_name',               HISTORYHOSTNAME),
                ('operator_name',           HISTORYOPERATORNAME),
                ('command_line',            c_char_p),
                ('comment',                 c_char_p)]