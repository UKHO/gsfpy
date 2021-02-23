from ctypes import Structure, c_double, c_int, c_ubyte

from . import constants


class c_gsfScaleInfo(Structure):
    _fields_ = [
        # Specifies bytes of storage in high order nibble and type of compression in
        # low order nibble.
        ("compressionFlag", c_ubyte),
        # The scale factor (millionths)for the array.
        ("multiplier", c_double),
        # DC offset to scale data by.
        ("offset", c_double),
    ]


SCALE_INFO_ARRAY = c_gsfScaleInfo * constants.GSF_MAX_PING_ARRAY_SUBRECORDS


class c_gsfScaleFactors(Structure):
    _fields_ = [
        # The number of scaling factors we actually have.
        ("numArraySubrecords", c_int),
        # For syntax see
        # https://stackoverflow.com/questions/4351721/python-ctypes-passing-a-struct-to-a-function-as-a-pointer-to-get-back-data
        ("scaleTable", SCALE_INFO_ARRAY),
    ]
