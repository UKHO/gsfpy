from enum import IntEnum

# Enums
class FileMode(IntEnum):
    GSF_CREATE              = 1
    GSF_READONLY            = 2
    GSF_UPDATE              = 3
    GSF_READONLY_INDEX      = 4
    GSF_UPDATE_INDEX        = 5
    GSF_APPEND              = 6

class RecordType(IntEnum):
    GSF_NEXT_RECORD                     = 0
    GSF_RECORD_HEADER                   = 1
    GSF_RECORD_SWATH_BATHYMETRY_PING    = 2
    GSF_RECORD_SOUND_VELOCITY_PROFILE   = 3
    GSF_RECORD_PROCESSING_PARAMETERS    = 4
    GSF_RECORD_SENSOR_PARAMETERS        = 5
    GSF_RECORD_COMMENT                  = 6
    GSF_RECORD_HISTORY                  = 7
    GSF_RECORD_SWATH_BATHY_SUMMARY      = 9
    GSF_RECORD_SINGLE_BEAM_PING         = 10
    GSF_RECORD_HV_NAVIGATION_ERROR      = 11
    GSF_RECORD_ATTITUDE                 = 12

class SeekOption(IntEnum):
    GSF_REWIND                          = 1
    GSF_END_OF_FILE                     = 2
    GSF_PREVIOUS_RECORD                 = 3