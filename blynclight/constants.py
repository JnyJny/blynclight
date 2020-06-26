"""Embrava Device Constants
"""

import enum

COMMAND_LENGTH = 9
EMBRAVA_VENDOR_IDS = [0x2C0D, 0x0E53]
END_OF_COMMAND = 0xFF22
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
    LOW = 1
    MEDIUM = 2
    HIGH = 4

    @classmethod
    def speed_for_value(cls, value: int):
        return {1: cls.LOW, 2: cls.MEDIUM, 3: cls.HIGH}.get(value, cls.LOW)

    @classmethod
    def value_for_speed(cls, speed: int) -> int:
        return {cls.LOW: 1, cls.MEDIUM: 2, cls.HIGH: 3}.get(speed, 1)


class MusicSelections(enum.Enum):
    pass
