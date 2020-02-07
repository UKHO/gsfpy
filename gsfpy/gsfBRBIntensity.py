from ctypes import (
    POINTER,
    Structure,
    Union,
    c_char,
    c_double,
    c_int,
    c_ubyte,
    c_uint,
    c_ushort,
)

from . import timespec

TIME_SERIES_INTENSITY_SPARE_BYTES = c_ubyte * 8


class c_gsfTimeSeriesIntensity(Structure):
    _fields_ = [
        ("sample_count", c_ushort),
        ("detect_sample", c_ushort),
        ("spare", TIME_SERIES_INTENSITY_SPARE_BYTES),
        ("samples", POINTER(c_uint)),
    ]


# NOTE - the largest of the imagery-specific types is defined here, to ensure the
# gsfSensorImagery union type has the correct size (see
# https://stackoverflow.com/questions/740577/sizeof-a-union-in-c-c). Other types in
# the union will be defined at a later date.
R2_SONIC_12_BYTE_STRING = c_ubyte * 12
R2_SONIC_SPARE_BYTES = c_ubyte * 32
R2_SONIC_MORE_INFO = c_double * 6


class c_gsfR2SonicImagerySpecific(Structure):
    _fields_ = [
        ("model_number", R2_SONIC_12_BYTE_STRING),
        ("serial_number", R2_SONIC_12_BYTE_STRING),
        ("dg_time", timespec.c_timespec),
        ("ping_number", c_uint),
        ("ping_period", c_double),
        ("sound_speed", c_double),
        ("frequency", c_double),
        ("tx_power", c_double),
        ("tx_pulse_width", c_double),
        ("tx_beamwidth_vert", c_double),
        ("tx_beamwidth_horiz", c_double),
        ("tx_steering_vert", c_double),
        ("tx_steering_horiz", c_double),
        ("tx_misc_info", c_uint),
        ("rx_bandwidth", c_double),
        ("rx_sample_rate", c_double),
        ("rx_range", c_double),
        ("rx_gain", c_double),
        ("rx_spreading", c_double),
        ("rx_absorption", c_double),
        ("rx_mount_tilt", c_double),
        ("rx_misc_info", c_uint),
        ("reserved", c_ushort),
        ("num_beams", c_ushort),
        ("more_info", R2_SONIC_MORE_INFO),
        ("spare", R2_SONIC_SPARE_BYTES),
    ]


# FIXME - Define classes for other imagery-specific tyes
class c_gsfEM3ImagerySpecific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfReson7100ImagerySpecific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfReson8100ImagerySpecific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfEM4ImagerySpecific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfKlein5410BssImagerySpecific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfSensorImagery(Union):
    _fields_ = [
        ("gsfEM3ImagerySpecific", c_gsfEM3ImagerySpecific),
        ("gsfReson7100ImagerySpecific", c_gsfReson7100ImagerySpecific),
        ("gsfReson8100ImagerySpecific", c_gsfReson8100ImagerySpecific),
        ("gsfEM4ImagerySpecific", c_gsfEM4ImagerySpecific),
        ("gsfKlein5410BssImagerySpecific", c_gsfKlein5410BssImagerySpecific),
        ("gsfR2SonicImagerySpecific", c_gsfR2SonicImagerySpecific),
    ]


BRB_INTENSITY_SPARE_BYTES = c_char * 16


class c_gsfBRBIntensity(Structure):
    _fields_ = [
        ("bits_per_sample", c_ubyte),
        ("applied_corrections", c_uint),
        ("spare", BRB_INTENSITY_SPARE_BYTES),
        ("sensor_imagery", c_gsfSensorImagery),
        ("time_series", POINTER(c_gsfTimeSeriesIntensity)),
    ]
