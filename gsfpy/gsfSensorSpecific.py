from ctypes import (
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


class c_gsfSeaBeamSpecific(Structure):
    _fields_ = [("EclipseTime", c_ushort)]


class c_gsfEM100Specific(Structure):
    _fields_ = [
        ("ship_pitch", c_double),
        ("transducer_pitch", c_double),
        ("mode", c_int),
        ("power", c_int),
        ("attenuation", c_int),
        ("tvg", c_int),
        ("pulse_length", c_int),
        ("counter", c_int),
    ]


class c_gsfEM121ASpecific(Structure):
    _fields_ = [
        ("ping_number", c_int),
        ("mode", c_int),
        ("valid_beams", c_int),
        ("pulse_length", c_int),
        ("beam_width", c_int),
        ("tx_power", c_int),
        ("tx_status", c_int),
        ("rx_status", c_int),
        ("surface_velocity", c_double),
    ]


class c_gsfSeaBatSpecific(Structure):
    _fields_ = [
        ("ping_number", c_int),
        ("surface_velocity", c_double),
        ("mode", c_int),
        ("sonar_range", c_int),
        ("transmit_power", c_int),
        ("receive_gain", c_int),
    ]


class c_gsfEM950Specific(Structure):
    _fields_ = [
        ("ping_number", c_int),
        ("mode", c_int),
        ("ping_quality", c_int),
        ("ship_pitch", c_double),
        ("transducer_pitch", c_double),
        ("surface_velocity", c_double),
    ]


SEAMAP_DOUBLE_ARRAY_OF_2 = c_double * 2


class c_gsfSeamapSpecific(Structure):
    _fields_ = [
        ("portTransmitter", SEAMAP_DOUBLE_ARRAY_OF_2),
        ("stbdTransmitter", SEAMAP_DOUBLE_ARRAY_OF_2),
        ("portGain", c_double),
        ("stbdGain", c_double),
        ("portPulseLength", c_double),
        ("stbdPulseLength", c_double),
        ("pressureDepth", c_double),
        ("altitude", c_double),
        ("temperature", c_double),
    ]


class c_gsfTypeIIISpecific(Structure):
    _fields_ = [
        ("leftmost_beam", c_ushort),
        ("rightmost_beam", c_ushort),
        ("total_beams", c_ushort),
        ("nav_mode", c_ushort),
        ("ping_number", c_ushort),
        ("mission_number", c_ushort),
    ]


class c_gsfCmpSassSpecific(Structure):
    _fields_ = [("lfreq", c_double), ("lntens", c_double)]


class c_gsfSBAmpSpecific(Structure):
    _fields_ = [
        ("hour", c_ushort),
        ("minute", c_ushort),
        ("second", c_ushort),
        ("hundredths", c_ushort),
        ("block_number", c_uint),
        ("avg_gate_depth", c_short),
    ]


SEA_BAT_CHAR_ARRAY_OF_4 = c_char * 4


class c_gsfSeaBatIISpecific(Structure):
    _fields_ = [
        ("ping_number", c_int),
        ("surface_velocity", c_double),
        ("mode", c_int),
        ("sonar_range", c_int),
        ("transmit_power", c_int),
        ("receive_gain", c_int),
        ("fore_aft_bw", c_double),
        ("athwart_bw", c_double),
        ("spare", SEA_BAT_CHAR_ARRAY_OF_4),
    ]


class c_gsfSeaBat8101Specific(Structure):
    _fields_ = [
        ("ping_number", c_int),
        ("surface_velocity", c_double),
        ("mode", c_int),
        ("range", c_int),
        ("power", c_int),
        ("gain", c_int),
        ("pulse_width", c_int),
        ("tvg_spreading", c_int),
        ("tvg_absorption", c_int),
        ("fore_aft_bw", c_double),
        ("athwart_bw", c_double),
        ("range_filt_min", c_double),
        ("range_filt_max", c_double),
        ("depth_filt_min", c_double),
        ("depth_filt_max", c_double),
        ("projector", c_int),
        ("spare", SEA_BAT_CHAR_ARRAY_OF_4),
    ]


SEA_BEAM_ALGORITHM_ORDER = c_char * 5
SEA_BEAM_SPARE = c_char * 2


class c_gsfSeaBeam2112Specific(Structure):
    _fields_ = [
        ("mode", c_int),
        ("surface_velocity", c_double),
        ("ssv_source", c_char),
        ("ping_gain", c_int),
        ("pulse_width", c_int),
        ("transmitter_attenuation", c_int),
        ("number_algorithms", c_int),
        ("algorithm_order", SEA_BEAM_ALGORITHM_ORDER),
        ("spare", SEA_BEAM_SPARE),
    ]


class c_gsfElacMkIISpecific(Structure):
    _fields_ = [
        ("mode", c_int),
        ("ping_num", c_int),
        ("sound_vel", c_int),
        ("pulse_length", c_int),
        ("receiver_gain_stbd", c_int),
        ("receiver_gain_port", c_int),
        ("reserved", c_int),
    ]


class c_gsfEM3RunTime(Structure):
    _fields_ = [
        ("model_number", c_int),
        ("dg_time", timespec.c_timespec),
        ("ping_number", c_int),
        ("serial_number", c_int),
        ("system_status", c_int),
        ("filter_id", c_int),
        ("min_depth", c_double),
        ("max_depth", c_double),
        ("absorption", c_double),
        ("pulse_length", c_double),
        ("transmit_beam_width", c_double),
        ("power_reduction", c_int),
        ("receive_beam_width", c_double),
        ("receive_bandwidth", c_int),
        ("receive_gain", c_int),
        ("cross_over_angle", c_int),
        ("ssv_source", c_int),
        ("swath_width", c_int),
        ("beam_spacing", c_int),
        ("coverage_sector", c_int),
        ("stabilization", c_int),
        ("port_swath_width", c_int),
        ("stbd_swath_width", c_int),
        ("port_coverage_sector", c_int),
        ("stbd_coverage_sector", c_int),
        ("hilo_freq_absorp_ratio", c_int),
        ("spare1", c_int),
    ]


EM3_RUN_TIME_2_ARRAY = c_gsfEM3RunTime * 2


class c_gsfEM3Specific(Structure):
    _fields_ = [
        ("model_number", c_int),
        ("ping_number", c_int),
        ("serial_number", c_int),
        ("surface_velocity", c_double),
        ("transducer_depth", c_double),
        ("valid_beams", c_int),
        ("sample_rate", c_int),
        ("depth_difference", c_double),
        ("offset_multiplier", c_int),
        ("run_time", EM3_RUN_TIME_2_ARRAY),
    ]


EM3_RAW_SPARE_BYTES = c_ubyte * 16


class c_gsfEMRunTime(Structure):
    _fields_ = [
        ("model_number", c_int),
        ("dg_time", timespec.c_timespec),
        ("ping_counter", c_int),
        ("serial_number", c_int),
        ("operator_station_status", c_ubyte),
        ("processing_unit_status", c_ubyte),
        ("bsp_status", c_ubyte),
        ("head_transceiver_status", c_ubyte),
        ("mode", c_ubyte),
        ("filter_id", c_ubyte),
        ("min_depth", c_double),
        ("max_depth", c_double),
        ("absorption", c_double),
        ("tx_pulse_length", c_double),
        ("tx_beam_width", c_double),
        ("tx_power_re_max", c_double),
        ("rx_beam_width", c_double),
        ("rx_bandwidth", c_double),
        ("rx_fixed_gain", c_double),
        ("tvg_cross_over_angle", c_double),
        ("ssv_source", c_ubyte),
        ("max_port_swath_width", c_int),
        ("beam_spacing", c_ubyte),
        ("max_port_coverage", c_int),
        ("stabilization", c_ubyte),
        ("max_stbd_coverage", c_int),
        ("max_stbd_swath_width", c_int),
        ("durotong_speed", c_double),
        ("hi_low_absorption_ratio", c_double),
        ("tx_along_tilt", c_double),
        ("filter_id_2", c_ubyte),
        ("spare", EM3_RAW_SPARE_BYTES),
    ]


class c_gsfEMPUStatus(Structure):
    _fields_ = [
        ("pu_cpu_load", c_double),
        ("sensor_status", c_ushort),
        ("achieved_port_coverage", c_int),
        ("achieved_stbd_coverage", c_int),
        ("yaw_stabilization", c_double),
        ("spare", EM3_RAW_SPARE_BYTES),
    ]


class c_gsfEM3RawTxSector(Structure):
    _fields_ = [
        ("tilt_angle", c_double),
        ("focus_range", c_double),
        ("signal_length", c_double),
        ("transmit_delay", c_double),
        ("center_frequency", c_double),
        ("waveform_id", c_int),
        ("sector_number", c_int),
        ("signal_bandwidth", c_double),
        ("spare", EM3_RAW_SPARE_BYTES),
    ]


GSF_MAX_EM3_SECTORS = 20
EM3_RAW_SECTORS = c_gsfEM3RawTxSector * GSF_MAX_EM3_SECTORS


class c_gsfEM3RawSpecific(Structure):
    _fields_ = [
        ("model_number", c_int),
        ("ping_counter", c_int),
        ("serial_number", c_int),
        ("surface_velocity", c_double),
        ("transducer_depth", c_double),
        ("valid_detections", c_int),
        ("sampling_frequency", c_double),
        ("vehicle_depth", c_double),
        ("depth_difference", c_double),
        ("offset_multiplier", c_int),
        ("spare_1", EM3_RAW_SPARE_BYTES),
        ("transmit_sectors", c_int),
        ("sector", EM3_RAW_SECTORS),
        ("spare_2", EM3_RAW_SPARE_BYTES),
        ("run_time", c_gsfEMRunTime),
        ("pu_status", c_gsfEMPUStatus),
    ]


RESON8100_SPARE_BYTES = c_char * 2


class c_gsfReson8100Specific(Structure):
    _fields_ = [
        ("latency", c_int),
        ("ping_number", c_int),
        ("sonar_id", c_int),
        ("sonar_model", c_int),
        ("frequency", c_int),
        ("surface_velocity", c_double),
        ("sample_rate", c_int),
        ("ping_rate", c_int),
        ("mode", c_int),
        ("range", c_int),
        ("power", c_int),
        ("gain", c_int),
        ("tvg_spreading", c_int),
        ("tvg_absorption", c_int),
        ("fore_aft_bw", c_double),
        ("athwart_bw", c_double),
        ("projector_type", c_int),
        ("projector_angle", c_int),
        ("range_filt_min", c_double),
        ("range_filt_max", c_double),
        ("depth_filt_min", c_double),
        ("depth_filt_max", c_double),
        ("filters_active", c_int),
        ("temperature", c_int),
        ("beam_spacing", c_double),
        ("spare", RESON8100_SPARE_BYTES),
    ]


# FIXME - Define classes for other sensor-specific tyes (from c_gsfReson7100Specific
#  onwards in the c_gsfSensorSpecific definition)
class c_gsfReson7100Specific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfResonTSeriesSpecific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfEM4Specific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfGeoSwathPlusSpecific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfKlein5410BssSpecific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfDeltaTSpecific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfEM12Specific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfR2SonicSpecific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfSBEchotracSpecific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfSBMGD77Specific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfSBBDBSpecific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfSBNOSHDBSpecific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfSBNavisoundSpecific(Structure):
    _fields_ = [("FIXME", c_int)]


class c_gsfSensorSpecific(Union):
    _fields_ = [
        ("gsfSeaBeamSpecific", c_gsfSeaBeamSpecific),
        ("gsfEM100Specific", c_gsfEM100Specific),
        ("gsfEM121ASpecific", c_gsfEM121ASpecific),
        ("gsfEM121Specific", c_gsfEM121ASpecific),
        ("gsfSeaBatSpecific", c_gsfSeaBatSpecific),
        ("gsfEM950Specific", c_gsfEM950Specific),
        ("gsfEM1000Specific", c_gsfEM950Specific),
        ("gsfSeamapSpecific", c_gsfSeamapSpecific),
        ("gsfTypeIIISeaBeamSpecific", c_gsfTypeIIISpecific),
        ("gsfSASSSpecific", c_gsfTypeIIISpecific),
        ("gsfCmpSassSpecific", c_gsfCmpSassSpecific),
        ("gsfSBAmpSpecific", c_gsfSBAmpSpecific),
        ("gsfSeaBatIISpecific", c_gsfSeaBatIISpecific),
        ("gsfSeaBat8101Specific", c_gsfSeaBat8101Specific),
        ("gsfSeaBeam2112Specific", c_gsfSeaBeam2112Specific),
        ("gsfElacMkIISpecific", c_gsfElacMkIISpecific),
        # used for EM120, EM300, EM1002, EM3000, EM3002, and EM121A_SIS
        ("gsfEM3Specific", c_gsfEM3Specific),
        # used for EM120, EM300, EM1002, EM3000, EM3002, and EM121A_SIS
        # with raw range and beam angle
        ("gsfEM3RawSpecific", c_gsfEM3RawSpecific),
        ("gsfReson8100Specific", c_gsfReson8100Specific),
        ("gsfReson7100Specific", c_gsfReson7100Specific),
        # used for T50 and T20
        ("gsfResonTSeriesSpecific", c_gsfResonTSeriesSpecific),
        # used for EM710, EM302, EM122, and EM2040
        ("gsfEM4Specific", c_gsfEM4Specific),
        # DHG 2006/09/27 Use for GeoSwath+ interferometer
        ("gsfGeoSwathPlusSpecific", c_gsfGeoSwathPlusSpecific),
        # Use for Klein 5410 Bathy Sidescan
        ("gsfKlein5410BssSpecific", c_gsfKlein5410BssSpecific),
        ("gsfDeltaTSpecific", c_gsfDeltaTSpecific),
        ("gsfEM12Specific", c_gsfEM12Specific),
        ("gsfR2SonicSpecific", c_gsfR2SonicSpecific),
        ("gsfSBEchotracSpecific", c_gsfSBEchotracSpecific),
        ("gsfSBBathy2000Specific", c_gsfSBEchotracSpecific),
        ("gsfSBMGD77Specific", c_gsfSBMGD77Specific),
        ("gsfSBBDBSpecific", c_gsfSBBDBSpecific),
        ("gsfSBNOSHDBSpecific", c_gsfSBNOSHDBSpecific),
        ("gsfSBPDDSpecific", c_gsfSBEchotracSpecific),
        ("gsfSBNavisoundSpecific", c_gsfSBNavisoundSpecific),
    ]
