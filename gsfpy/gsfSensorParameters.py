from ctypes import *

from . import timespec

GSF_MAX_SENSOR_PARAMETERS = 128
SENSORPARAMETERSPARAMSIZES = c_short * GSF_MAX_SENSOR_PARAMETERS
SENSORPARAMETERSPARAMS = c_char_p * GSF_MAX_SENSOR_PARAMETERS

class c_gsfSensorParameters(Structure):
    _fields_ = [('param_time',              timespec.c_timespec),
                ('number_parameters',       c_int),
                ('param_size',              SENSORPARAMETERSPARAMSIZES),
                ('param',                   SENSORPARAMETERSPARAMS)]