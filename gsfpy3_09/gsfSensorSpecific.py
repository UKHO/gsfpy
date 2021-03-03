from ctypes import (
    Structure,
    Union,
    c_char,
    c_double,
    c_int,
    c_long,
    c_short,
    c_ubyte,
    c_uint,
    c_ulong,
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


class c_gsfEMRunTime(Structure):        # 168 bytes
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


class c_gsfEMPUStatus(Structure):       # 42 bytes
    _fields_ = [
        ("pu_cpu_load", c_double),
        ("sensor_status", c_ushort),
        ("achieved_port_coverage", c_int),
        ("achieved_stbd_coverage", c_int),
        ("yaw_stabilization", c_double),
        ("spare", EM3_RAW_SPARE_BYTES),
    ]


class c_gsfEM3RawTxSector(Structure):   # 72 bytes
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
EM3_RAW_SECTORS = c_gsfEM3RawTxSector * GSF_MAX_EM3_SECTORS     # 1440 bytes


class c_gsfEM3RawSpecific(Structure):       # 1792 bytes (1746 + 23 * 2)
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
        ("transmit_sectors", c_int),        # 80 bytes
        ("sector", EM3_RAW_SECTORS),        # 1520 bytes
        ("spare_2", EM3_RAW_SPARE_BYTES),   # 1536 bytes
        ("run_time", c_gsfEMRunTime),       # 1704 bytes
        ("pu_status", c_gsfEMPUStatus),     # 1746 bytes
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


RESON7100_RESERVED_1 = c_ubyte * 16
RESON7100_RESERVED_2 = c_char * 15
RESON7100_RESERVED_3 = c_char * 8


class c_gsfReson7100Specific(Structure):
    _fields_ = [
        ("protocol_version", c_uint),
        ("device_id", c_uint),
        ("reserved_1", RESON7100_RESERVED_1),
        ("major_serial_number", c_uint),
        ("minor_serial_number", c_uint),
        ("ping_number", c_uint),
        ("multi_ping_seq", c_uint),
        ("frequency", c_double),
        ("sample_rate", c_double),
        ("receiver_bandwdth", c_double),
        ("tx_pulse_width", c_double),
        ("tx_pulse_type_id", c_uint),
        ("tx_pulse_envlp_id", c_uint),
        ("tx_pulse_envlp_param", c_double),
        ("tx_pulse_reserved", c_uint),
        ("max_ping_rate", c_double),
        ("ping_period", c_double),
        ("range", c_double),
        ("power", c_double),
        ("gain", c_double),
        ("control_flags", c_uint),
        ("projector_id", c_uint),
        ("projector_steer_angl_vert", c_double),
        ("projector_steer_angl_horz", c_double),
        ("projector_beam_wdth_vert", c_double),
        ("projector_beam_wdth_horz", c_double),
        ("projector_beam_focal_pt", c_double),
        ("projector_beam_weighting_window_type", c_uint),
        ("projector_beam_weighting_window_param", c_uint),
        ("transmit_flags", c_uint),
        ("hydrophone_id", c_uint),
        ("receiving_beam_weighting_window_type", c_uint),
        ("receiving_beam_weighting_window_param", c_uint),
        ("receive_flags", c_uint),
        ("receive_beam_width", c_double),
        ("range_filt_min", c_double),
        ("range_filt_max", c_double),
        ("depth_filt_min", c_double),
        ("depth_filt_max", c_double),
        ("absorption", c_double),
        ("sound_velocity", c_double),
        ("spreading", c_double),
        ("raw_data_from_7027", c_ubyte),
        ("reserved_2", RESON7100_RESERVED_2),
        ("sv_source", c_ubyte),
        ("layer_comp_flag", c_ubyte),
        ("reserved_3", RESON7100_RESERVED_3),
    ]


RESONTSERIES_RESERVED_1 = c_ubyte * 10
RESONTSERIES_RESERVED_2 = c_ubyte * 3
RESONTSERIES_RESERVED_3 = c_ubyte * 32
RESONTSERIES_RESERVED_7027 = c_ubyte * 420
RESONTSERIES_DEVICE_DESCRIPTION = c_char * 60


class c_gsfResonTSeriesSpecific(Structure):
    _fields_ = [
        ("protocol_version", c_uint),
        ("device_id", c_uint),
        ("number_devices", c_uint),
        ("system_enumerator", c_ushort),
        ("reserved_1", RESONTSERIES_RESERVED_1),
        ("major_serial_number", c_uint),
        ("minor_serial_number", c_uint),
        ("ping_number", c_uint),
        ("multi_ping_seq", c_uint),
        ("frequency", c_double),
        ("sample_rate", c_double),
        ("receiver_bandwdth", c_double),
        ("tx_pulse_width", c_double),
        ("tx_pulse_type_id", c_uint),
        ("tx_pulse_envlp_id", c_uint),
        ("tx_pulse_envlp_param", c_double),
        ("tx_pulse_mode", c_ushort),
        ("tx_pulse_reserved", c_ushort),
        ("max_ping_rate", c_double),
        ("ping_period", c_double),
        ("range", c_double),
        ("power", c_double),
        ("gain", c_double),
        ("control_flags", c_uint),
        ("projector_id", c_uint),
        ("projector_steer_angl_vert", c_double),
        ("projector_steer_angl_horz", c_double),
        ("projector_beam_wdth_vert", c_double),
        ("projector_beam_wdth_horz", c_double),
        ("projector_beam_focal_pt", c_double),
        ("projector_beam_weighting_window_type", c_uint),
        ("projector_beam_weighting_window_param", c_double),
        ("transmit_flags", c_uint),
        ("hydrophone_id", c_uint),
        ("receiving_beam_weighting_window_type", c_uint),
        ("receiving_beam_weighting_window_param", c_double),
        ("receive_flags", c_uint),
        ("receive_beam_width", c_double),
        ("range_filt_min", c_double),
        ("range_filt_max", c_double),
        ("depth_filt_min", c_double),
        ("depth_filt_max", c_double),
        ("absorption", c_double),
        ("sound_velocity", c_double),
        ("sv_source", c_ubyte),
        ("spreading", c_double),
        ("beam_spacing_mode", c_ushort),
        ("sonar_source_mode", c_ushort),
        ("coverage_mode", c_ubyte),
        ("coverage_angle", c_double),
        ("horizontal_receiver_steering_angle", c_double),
        ("reserved_2", RESONTSERIES_RESERVED_2),
        ("uncertainty_type", c_uint),
        ("transmitter_steering_angle", c_double),
        ("applied_roll", c_double),
        ("detection_algorithm", c_ushort),
        ("detection_flags", c_uint),
        ("device_description", RESONTSERIES_DEVICE_DESCRIPTION),
        ("reserved_7027", RESONTSERIES_RESERVED_7027),
        ("reserved_3", RESONTSERIES_RESERVED_3),
    ]


EM4_SPARE_BYTES = c_ubyte * 16


class c_gsfEM4TxSector(Structure):
    _fields_ = [
        ("tilt_angle", c_double),
        ("focus_range", c_double),
        ("signal_length", c_double),
        ("transmit_delay", c_double),
        ("center_frequency", c_double),
        ("mean_absorption", c_double),
        ("waveform_id", c_int),
        ("sector_number", c_int),
        ("signal_bandwidth", c_double),
        ("spare", EM4_SPARE_BYTES),
    ]


EM4_SECTORS = c_gsfEM4TxSector * 9


class c_gsfEM4Specific(Structure):
    _fields_ = [
        ("model_number", c_int),
        ("ping_counter", c_int),
        ("serial_number", c_int),
        ("surface_velocity", c_double),
        ("transducer_depth", c_double),
        ("valid_detections", c_int),
        ("sampling_frequency", c_double),
        ("doppler_corr_scale", c_uint),
        ("vehicle_depth", c_double),
        ("spare_1", EM4_SPARE_BYTES),
        ("transmit_sectors", c_int),
        ("sector", EM4_SECTORS),
        ("spare_2", EM4_SPARE_BYTES),
        ("run_time", c_gsfEMRunTime),
        ("pu_status", c_gsfEMPUStatus),
    ]


GEOSWATH_SPARE_BYTES = c_char * 32


class c_gsfGeoSwathPlusSpecific(Structure):
    _fields_ = [
        ("data_source", c_int),
        ("side", c_int),
        ("model_number", c_int),
        ("frequency", c_double),
        ("echosounder_type", c_int),
        ("ping_number", c_long),
        ("num_nav_samples", c_int),
        ("num_attitude_samples", c_int),
        ("num_heading_samples", c_int),
        ("num_miniSVS_samples", c_int),
        ("num_echosounder_samples", c_int),
        ("num_raa_samples", c_int),
        ("mean_sv", c_double),
        ("surface_velocity", c_double),
        ("valid_beams", c_int),
        ("sample_rate", c_double),
        ("pulse_length", c_double),
        ("ping_length", c_int),
        ("transmit_power", c_int),
        ("sidescan_gain_channel", c_int),
        ("stabilization", c_int),
        ("gps_quality", c_int),
        ("range_uncertainty", c_double),
        ("angle_uncertainty", c_double),
        ("spare", GEOSWATH_SPARE_BYTES),
    ]


KLEIN5410_SPARE_BYTES = c_char * 32


class c_gsfKlein5410BssSpecific(Structure):
    _fields_ = [
        ("data_source", c_int),
        ("side", c_int),
        ("model_number", c_int),
        ("acoustic_frequency", c_double),
        ("sampling_frequency", c_double),
        ("ping_number", c_uint),
        ("num_samples", c_uint),
        ("num_raa_samples", c_uint),
        ("error_flags", c_uint),
        ("range", c_uint),
        ("fish_depth", c_double),
        ("fish_altitude", c_double),
        ("sound_speed", c_double),
        ("tx_waveform", c_int),
        ("altimeter", c_int),
        ("raw_data_config", c_uint),
        ("spare", KLEIN5410_SPARE_BYTES),
    ]


DELTAT_FILE_TYPE = c_char * 4
DELTAT_SPARE = c_char * 32


class c_gsfDeltaTSpecific(Structure):
    _fields_ = [
        ("decode_file_type", DELTAT_FILE_TYPE),
        ("version", c_char),
        ("ping_byte_size", c_int),
        ("interrogation_time", timespec.c_timespec),
        ("samples_per_beam", c_int),
        ("sector_size", c_double),
        ("start_angle", c_double),
        ("angle_increment", c_double),
        ("acoustic_range", c_int),
        ("acoustic_frequency", c_int),
        ("sound_velocity", c_double),
        ("range_resolution", c_double),
        ("profile_tilt_angle", c_double),
        ("repetition_rate", c_double),
        ("ping_number", c_ulong),
        ("intensity_flag", c_ubyte),
        ("ping_latency", c_double),
        ("data_latency", c_double),
        ("sample_rate_flag", c_ubyte),
        ("option_flags", c_ubyte),
        ("num_pings_avg", c_int),
        ("center_ping_time_offset", c_double),
        ("user_defined_byte", c_ubyte),
        ("altitude", c_double),
        ("external_sensor_flags", c_char),
        ("pulse_length", c_double),
        ("fore_aft_beamwidth", c_double),
        ("athwartships_beamwidth", c_double),
        ("spare", DELTAT_SPARE),
    ]


EM12_SPARE = c_char * 32


class c_gsfEM12Specific(Structure):
    _fields_ = [
        ("ping_number", c_int),
        ("resolution", c_int),
        ("ping_quality", c_int),
        ("sound_velocity", c_double),
        ("mode", c_int),
        ("spare", EM12_SPARE),
    ]


R2SONIC_MODELNO = c_ubyte * 12
R2SONIC_SERIALNO = c_ubyte * 12
R2SONIC_INFO = c_double * 12
R2SONIC_SPARE = c_ubyte * 32


class c_gsfR2SonicSpecific(Structure):
    _fields_ = [
        ("model_number", R2SONIC_MODELNO),
        ("serial_number", R2SONIC_SERIALNO),
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
        ("A0_more_info", R2SONIC_INFO),
        ("A2_more_info", R2SONIC_INFO),
        ("G0_depth_gate_min", c_double),
        ("G0_depth_gate_max", c_double),
        ("G0_depth_gate_slope", c_double),
        ("spare", R2SONIC_SPARE),
    ]


SBECHOTRAC_SPARE = c_char * 4


class c_gsfSBEchotracSpecific(Structure):
    _fields_ = [
        ("navigation_error", c_int),
        ("mpp_source", c_ushort),
        ("tide_source", c_ushort),
        ("dynamic_draft", c_double),
        ("spare", SBECHOTRAC_SPARE),
    ]


SBMGD77_SPARE = c_char * 4


class c_gsfSBMGD77Specific(Structure):
    _fields_ = [
        ("time_zone_corr", c_ushort),
        ("position_type_code", c_ushort),
        ("correction_code", c_ushort),
        ("bathy_type_code", c_ushort),
        ("quality_code", c_ushort),
        ("travel_time", c_double),
        ("spare", SBMGD77_SPARE),
    ]


SBBDB_SPARE = c_char * 4


class c_gsfSBBDBSpecific(Structure):
    _fields_ = [
        ("doc_no", c_int),
        ("eval", c_char),
        ("classification", c_char),
        ("track_adj_flag", c_char),
        ("source_flag", c_char),
        ("pt_or_track_ln", c_char),
        ("datum_flag", c_char),
        ("spare", c_char),
    ]


SBNOSHDB_SPARE = c_char * 4


class c_gsfSBNOSHDBSpecific(Structure):
    _fields_ = [
        ("type_code", c_ushort),
        ("carto_code", c_ushort),
        ("spare", SBNOSHDB_SPARE),
    ]


SBNAVISOUND_SPARE = c_char * 8


class c_gsfSBNavisoundSpecific(Structure):
    _fields_ = [
        ("pulse_length", c_double),
        ("spare", SBNAVISOUND_SPARE),
    ]


KMALL_TX_SECTOR_SPARE_BYTES = c_ubyte * 20

class c_gsfKMALLTxSector(Structure):
    _fields_ = [
        ("txSectorNumb", c_int),
        ("txArrNumber", c_int),
        ("txSubArray", c_int),
        ("sectorTransmitDelay_sec", c_double),
        ("tiltAngleReTx_deg", c_double),
        ("txNominalSourceLevel_dB", c_double),
        ("txFocusRange_m", c_double),
        ("centreFreq_Hz", c_double),
        ("signalBandWidth_Hz", c_double),
        ("totalSignalLength_sec", c_double),
        ("pulseShading", c_int),
        ("signalWaveForm", c_int),
        ("spare1", KMALL_TX_SECTOR_SPARE_BYTES)
    ]


KMALL_EXTRA_DET_SPARE_BYTES = c_ubyte * 32

class c_gsfKMALLExtraDetClass(Structure):
    _fields_ = [
        ("numExtraDetInClass", c_int),
        ("alarmFlag", c_int),
        ("spare", KMALL_EXTRA_DET_SPARE_BYTES)
    ]


# Sensor specific data structures for the Kongsberg 2040 / SIS 5.0 */
KMALL_SPARE_BYTES_1 = c_ubyte * 8
KMALL_SPARE_BYTES_2 = c_ubyte * 16
KMALL_SPARE_BYTES_3 = c_ubyte * 32
KMALL_SPARE_BYTES_4 = c_ubyte * 32
KMALL_SPARE_BYTES_5 = c_ubyte * 32
KMALL_SECTOR = c_gsfKMALLTxSector * 9
KMALL_EXTRA_DET_CLASS_INFO = c_gsfKMALLExtraDetClass * 11

class c_gsfKMALLSpecific(Structure):
    _fields_ = [
        ("gsfKMALLVersion", c_int),
        ("dgmType", c_int),
        ("dgmVersion", c_int),
        ("systemID", c_int),
        ("echoSounderID", c_int),
        ("spare1", KMALL_SPARE_BYTES_1),
        ("numBytesCmnPart", c_int),
        ("pingCnt", c_int),
        ("rxFansPerPing", c_int),
        ("rxFanIndex", c_int),
        ("swathsPerPing", c_int),
        ("swathAlongPosition", c_int),
        ("txTransducerInd", c_int),
        ("rxTransducerInd", c_int),
        ("numRxTransducers", c_int),
        ("algorithmType", c_int),
        ("spare2", KMALL_SPARE_BYTES_2),
        ("numBytesInfoData", c_int),
        ("pingRate_Hz", c_double),
        ("beamSpacing", c_int),
        ("depthMode", c_int),
        ("subDepthMode", c_int),
        ("distanceBtwSwath", c_int),
        ("detectionMode", c_int),
        ("pulseForm", c_int),
        ("frequencyMode_Hz", c_double),
        ("freqRangeLowLim_Hz", c_double),
        ("freqRangeHighLim_Hz", c_double),
        ("maxTotalTxPulseLength_sec", c_double),
        ("maxEffTxPulseLength_sec", c_double),
        ("maxEffTxBandWidth_Hz", c_double),
        ("absCoeff_dBPerkm", c_double),
        ("portSectorEdge_deg", c_double),
        ("starbSectorEdge_deg", c_double),
        ("portMeanCov_deg", c_double),
        ("starbMeanCov_deg", c_double),
        ("portMeanCov_m", c_double),
        ("starbMeanCov_m", c_double),
        ("modeAndStabilisation", c_int),
        ("runtimeFilter1", c_int),
        ("runtimeFilter2", c_int),
        ("pipeTrackingStatus", c_int),
        ("transmitArraySizeUsed_deg", c_double),
        ("receiveArraySizeUsed_deg", c_double),
        ("transmitPower_dB", c_double),
        ("SLrampUpTimeRemaining", c_int),
        ("yawAngle_deg", c_double),
        ("numTxSectors", c_int),
        ("numBytesPerTxSector", c_int),
        ("headingVessel_deg", c_double),
        ("soundSpeedAtTxDepth_mPerSec", c_double),
        ("txTransducerDepth_m", c_double),
        ("z_waterLevelReRefPoint_m", c_double),
        ("x_kmallToall_m", c_double),
        ("y_kmallToall_m", c_double),
        ("latLongInfo", c_int),
        ("posSensorStatus", c_int),
        ("attitudeSensorStatus", c_int),
        ("latitude_deg", c_double),
        ("longitude_deg", c_double),
        ("ellipsoidHeightReRefPoint_m", c_double),
        ("spare3", KMALL_SPARE_BYTES_3),
        ("sector", KMALL_SECTOR),
        ("numBytesRxInfo", c_int),
        ("numSoundingsMaxMain", c_int),
        ("numSoundingsValidMain", c_int),
        ("numBytesPerSounding", c_int),
        ("WCSampleRate", c_double),
        ("seabedImageSampleRate", c_double),
        ("BSnormal_dB", c_double),
        ("BSoblique_dB", c_double),
        ("extraDetectionAlarmFlag", c_int),
        ("numExtraDetections", c_int),
        ("numExtraDetectionClasses", c_int),
        ("numBytesPerClass", c_int),
        ("spare4", KMALL_SPARE_BYTES_4),
        ("extraDetClassInfo", KMALL_EXTRA_DET_CLASS_INFO),
        ("spare5", KMALL_SPARE_BYTES_5)
    ]


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
        ("gsfKMallSpecific", c_gsfKMALLSpecific),
        ("gsfSBEchotracSpecific", c_gsfSBEchotracSpecific),
        ("gsfSBBathy2000Specific", c_gsfSBEchotracSpecific),
        ("gsfSBMGD77Specific", c_gsfSBMGD77Specific),
        ("gsfSBBDBSpecific", c_gsfSBBDBSpecific),
        ("gsfSBNOSHDBSpecific", c_gsfSBNOSHDBSpecific),
        ("gsfSBPDDSpecific", c_gsfSBEchotracSpecific),
        ("gsfSBNavisoundSpecific", c_gsfSBNavisoundSpecific),
    ]
