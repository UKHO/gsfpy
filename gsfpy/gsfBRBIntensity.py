from ctypes import (
    POINTER,
    Structure,
    Union,
    c_char,
    c_double,
    c_int,
    c_short,
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


EM3IMG_SPARE = c_ubyte * 4


class c_gsfEM3ImagerySpecific(Structure):
    _fields_ = [
        ("range_norm", c_ushort),
        ("start_tvg_ramp", c_ushort),
        ("stop_tvg_ramp", c_ushort),
        ("bsn", c_char),
        ("bso", c_char),
        ("mean_absorption", c_double),
        ("offset", c_short),
        ("scale", c_short),
        ("spare", EM3IMG_SPARE),
    ]


RESON7100IMG_SPARE = c_ubyte * 64


class c_gsfReson7100ImagerySpecific(Structure):
    _fields_ = [
        ("size", c_ushort),
        ("spare", RESON7100IMG_SPARE),
    ]


RESON8100IMG_SPARE = c_ubyte * 8


class c_gsfReson8100ImagerySpecific(Structure):
    _fields_ = [
        ("spare", RESON8100IMG_SPARE),
    ]


RESONTSERIESIMG_SPARE = c_ubyte * 64


class c_gsfResonTSeriesImagerySpecific(Structure):
    _fields_ = [
        ("size", c_ushort),
        ("spare", RESONTSERIESIMG_SPARE),
    ]


EM4IMG_SPARE = c_ubyte * 20


class c_gsfEM4ImagerySpecific(Structure):
    _fields_ = [
        ("sampling_frequency", c_double),
        ("mean_absorption", c_double),
        ("tx_pulse_length", c_double),
        ("range_norm", c_int),
        ("start_tvg_ramp", c_int),
        ("stop_tvg_ramp", c_int),
        ("bsn", c_double),
        ("bso", c_double),
        ("tx_beam_width", c_double),
        ("tvg_cross_over", c_double),
        ("offset", c_short),
        ("scale", c_short),
        ("spare", EM4IMG_SPARE),
    ]


KLEIN5410IMG_BEAM = c_uint * 5
KLEIN5410IMG_SPARE = c_ubyte * 4


class c_gsfKlein5410BssImagerySpecific(Structure):
    _fields_ = [
        ("res_mode", c_uint),
        ("tvg_page", c_uint),
        ("beam_id", KLEIN5410IMG_BEAM),
        ("spare", KLEIN5410IMG_SPARE),
    ]


class c_gsfSensorImagery(Union):
    _fields_ = [
        ("gsfEM3ImagerySpecific", c_gsfEM3ImagerySpecific),
        ("gsfReson7100ImagerySpecific", c_gsfReson7100ImagerySpecific),
        ("gsfReson8100ImagerySpecific", c_gsfReson8100ImagerySpecific),
        ("gsfResonTSeriesImagerySpecific", c_gsfResonTSeriesImagerySpecific),
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
