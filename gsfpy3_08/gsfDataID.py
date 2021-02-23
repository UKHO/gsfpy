from ctypes import Structure, c_int, c_uint


class c_gsfDataID(Structure):
    _fields_ = [
        # Boolean
        ("checksumFlag", c_int),
        # Up to 9 bits
        ("reserved", c_int),
        # Bits 00-11 => data type number
        # Bits 12-22 => registry number
        ("recordID", c_uint),
        # Specifies the nth occurrence of record type specified by recordID
        # Relevant only for direct access. The record_number counts from 1
        ("record_number", c_int),
    ]
