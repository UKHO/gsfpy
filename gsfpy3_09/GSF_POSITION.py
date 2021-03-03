from ctypes import Structure, c_double


class c_GSF_POSITION(Structure):
    _fields_ = [
        ("lon", c_double),
        ("lat", c_double),
        ("z", c_double),
    ]
