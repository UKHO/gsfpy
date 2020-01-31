from ctypes import *

class c_gsfDataID(Structure):
    _fields_ = [('checksumFlag', c_int),                # Boolean
                ('reserved', c_int),                    # Up to 9 bits
                ('recordID', c_uint),                   # Bits 00-11 => data type number
                                                        # Bits 12-22 => registry number
                ('record_number', c_int)]               # Specifies the nth occurance of record type specified by recordID
                                                        # Relevant only for direct access. The record_number counts from 1