"""Embrava Device Constants
"""

import enum

EMBRAVA_VENDOR_IDS = [0x2C0D, 0x0E53]
END_OF_COMMAND = 0xFF
COMMAND_LENGTH = 9
PAD_VALUE = 0


class DeviceType(enum.Enum):
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


class FlashSpeed(enum.IntEnum):
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 4

    def is_valid(self, speed):
        """Returns True if speed is a valid flash speed value.

        """
        return speed in [self.OFF, self.LOW, self.MEDIUM, self.HIGH]


class MusicSelections(enum.Enum):
    pass


class MusicVolume(enum.IntEnum):
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
