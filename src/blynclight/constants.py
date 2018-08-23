'''
'''

from enum import Enum

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

class FlashSpeed(Enum):
    OFF    = 0
    LOW    = 1
    MEDIUM = 2
    HIGH   = 3

class MusicSelections(Enum):
    pass

class MusicVolume(Enum):
    pass
