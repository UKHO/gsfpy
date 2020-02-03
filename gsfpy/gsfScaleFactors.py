from ctypes import *

from . import constants


class c_gsfScaleInfo(Structure):
    _fields_ = [('compressionFlag', c_ubyte),           # Specifies bytes of storage in high order nibble and type of compression in low order nibble. */
                ('multiplier', c_double),               # The scale factor (millionths)for the array. */
                ('offset', c_double)]                   # DC offset to scale data by. */

SCALEINFOARRAY = c_gsfScaleInfo * constants.GSF_MAX_PING_ARRAY_SUBRECORDS

class c_gsfScaleFactors(Structure):
    _fields_ = [('numArraySubrecords', c_int),          # The number of scaling factors we actually have. */
                ('scaleTable', SCALEINFOARRAY)]         # For syntax see https://stackoverflow.com/questions/4351721/python-ctypes-passing-a-struct-to-a-function-as-a-pointer-to-get-back-data
