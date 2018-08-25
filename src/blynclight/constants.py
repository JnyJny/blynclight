'''
'''

from enum import Enum


class DeviceType(Enum):
    INVALID = 0
    TENX_10 = 1
    TENX_20 = 2
    V30 = 3
    V30S = 4
    V30_LUMENA110 = 5
    WIRELESS_V30S = 6
    MINI_V30S = 7
    V30_LUMENA120 = 8
    V30_LUMENA = 9
    V30_LUMENA210 = 10
    V30_LUMENA220 = 11
    EMBEDDED_V30 = 12


class FlashSpeed(Enum):
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class MusicOp(Enum):
    STOP = 0
    START = 1


class MusicSelections(Enum):
    pass


class MusicVolume(Enum):
    Vol000Percent = 0
    Vol010Percent = 1
    Vol020Percent = 2
    Vol030Percent = 3
    Vol040Percent = 4
    Vol050Percent = 5
    Vol060Percent = 6
    Vol070Percent = 7
    Vol080Percent = 8
    Vol090Percent = 9
    Vol100Percent = 10
