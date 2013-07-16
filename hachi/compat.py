# -*- coding: utf-8 -*-
import struct
import sys

__all__ = ['unpack', 'pack']


if sys.version_info[0] == 2:
    unpack = lambda x, y: struct.unpack(bytes(x), buffer(y))
    pack = lambda x, y: struct.pack(bytes(x), y)
elif sys.version_info[0] == 3:
    unpack = struct.unpack
    pack = struct.pack
