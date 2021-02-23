from ctypes import Structure, c_double


# Note: the coordinate system is:
#       +x forward, +y starboard, + z down, +hdg cw from north
class c_GSF_POSITION_OFFSETS(Structure):
    _fields_ = [
        ("x", c_double),
        ("y", c_double),
        ("z", c_double),
    ]
