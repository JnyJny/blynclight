'''
'''

from ctypes import Structure, c_byte
from enum import Enum

MAXIMUM_DEVICES = 32

class DeviceInfo(Structure):
    _fields_ = [ ('byType', c_byte)]

class DeviceType(Enum):
    INVALID       = 0
    TENX_10       = 1
    TENX_20       = 2
    V30           = 3
    V30S          = 4
    V30_LUMENA110 = 5
    WIRELESS_V30S = 6
    MINI_V30S     = 7
    V30_LUMENA120 = 8
    V30_LUMENA    = 9
    V30_LUMENA210 = 10
    V30_LUMENA220 = 11
    EMBEDDED_V30  = 12

class Color(Enum):
    RED    = 0
    GREEN  = 1
    YELLOW = 2
    PURPLE = 3
    CYAN   = 4
    BLUE   = 5
    WHITE  = 6
    ORANGE = 7
    OFF    = 8

class FlashSpeed(Enum):
    OFF    = 0
    LOW    = 1
    MEDIUM = 2
    HIGH   = 3
