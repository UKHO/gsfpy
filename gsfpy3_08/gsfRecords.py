from ctypes import Structure

from . import (
    gsfComment,
    gsfHeader,
    gsfHistory,
    gsfHVNavigationError,
    gsfNavigationError,
    gsfProcessingParameters,
    gsfSensorParameters,
    gsfSingleBeamPing,
    gsfSVP,
    gsfSwathBathyPing,
    gsfSwathBathySummary,
)


class c_gsfRecords(Structure):
    _fields_ = [
        ("head", gsfHeader.c_gsfHeader),
        ("summary", gsfSwathBathySummary.c_gsfSwathBathySummary),
        ("mb_ping", gsfSwathBathyPing.c_gsfSwathBathyPing),
        ("sb_ping", gsfSingleBeamPing.c_gsfSingleBeamPing),
        ("svp", gsfSVP.c_gsfSVP),
        ("process_parameters", gsfProcessingParameters.c_gsfProcessingParameters),
        ("sensor_parameters", gsfSensorParameters.c_gsfSensorParameters),
        ("comment", gsfComment.c_gsfComment),
        ("history", gsfHistory.c_gsfHistory),
        ("nav_error", gsfNavigationError.c_gsfNavigationError),
        ("hv_nav_error", gsfHVNavigationError.c_gsfHVNavigationError),
    ]
