from ctypes import *

from . import timespec

GSF_MAX_PROCESSING_PARAMETERS = 128
PROCESSINGPARAMETERSPARAMSIZES = c_short * GSF_MAX_PROCESSING_PARAMETERS
PROCESSINGPARAMETERSPARAMS = c_char_p * GSF_MAX_PROCESSING_PARAMETERS

class c_gsfProcessingParameters(Structure):
    _fields_ = [('param_time',              timespec.c_timespec),
                ('number_parameters',       c_int),
                ('param_size',              PROCESSINGPARAMETERSPARAMSIZES),
                ('param',                   PROCESSINGPARAMETERSPARAMS)]