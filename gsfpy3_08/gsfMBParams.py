from ctypes import Structure, c_char, c_int

from . import gsfMBOffsets

NUM_EPOCH_BYTES = 64
START_OF_EPOCH = c_char * NUM_EPOCH_BYTES


class c_gsfMBParams(Structure):
    _fields_ = [
        ("start_of_epoch", START_OF_EPOCH),
        ("horizontal_datum", c_int),
        ("vertical_datum", c_int),
        ("utc_offset", c_int),
        ("number_of_transmitters", c_int),
        ("number_of_receivers", c_int),
        ("roll_reference", c_int),
        ("roll_compensated", c_int),
        ("pitch_compensated", c_int),
        ("heave_compensated", c_int),
        ("tide_compensated", c_int),
        ("ray_tracing", c_int),
        ("depth_calculation", c_int),
        ("vessel_type", c_int),
        ("full_raw_data", c_int),
        ("msb_applied_to_attitude", c_int),
        ("heave_removed_from_gps_tc", c_int),
        ("to_apply", gsfMBOffsets.c_gsfMBOffsets),
        ("applied", gsfMBOffsets.c_gsfMBOffsets),
    ]
