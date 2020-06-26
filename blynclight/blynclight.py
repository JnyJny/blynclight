from contextlib import contextmanager
from enum import Enum
from typing import Dict, List, Tuple, Union
from functools import partial, partialmethod, wraps

import hid

from loguru import logger

from .bitvector import BitVector, BitField
from .constants import EMBRAVA_VENDOR_IDS, FlashSpeed, END_OF_COMMAND, COMMAND_LENGTH
from .exceptions import BlyncLightInUse, BlyncLightNotFound, BlyncLightUnknownDevice


class BlyncCommand(BitField):
    def __set__(self, obj, value) -> None:
        super().__set__(obj, value)
        try:
            obj.update()
        except AttributeError:
            logger.error(f"Failed to update {obj!r} after setting {self.name}")


class BlyncSpeed(BitField):
    # speed gets it's own descriptor implementation due to it's being a
    # flag instead of a "value" and this was easier than trying to
    # shoehorn the logic into the BlyncCommand descriptor.
    #
    # If more than one bit is set in the three bit speed field and the
    # flash bit is set, the light will flash exceedingly fast. If speed
    # is zero, the light turns off regardless of off == 0. Bug in the
    # firmware maybe?

    def __get__(self, obj, type=None) -> object:
        v = super().__get__(obj, type)
        return FlashSpeed.speed_for_value(v)

    def __set__(self, obj, value) -> None:
        speed = FlashSpeed.value_for_speed(value)
        super().__set__(obj, speed)
        try:
            obj.update()
        except AttributeError:
            logger.error(f"Failed to update {obj!r} after setting {self.name}")


class BlyncLight(BitVector):
    @classmethod
    def available_lights(cls) -> List[Dict[str, Union[int, str]]]:
        """
        """
        lights = []
        for vendor_id in EMBRAVA_VENDOR_IDS:
            lights.extend(hid.enumerate(vendor_id))
        return lights

    @classmethod
    def get_light(cls, light_id: int = 0, immediate: bool = True):
        """
        Raises
        - KeyError
        - ValueError
        """
        try:
            light = cls.available_lights()[light_id]
        except IndexError:
            raise BlyncLightNotFound(light_id)

        return cls(light["vendor_id"], light["product_id"], immediate)

    def __init__(self, vendor_id: int, product_id: int, immediate: bool = False):
        super().__init__(size=COMMAND_LENGTH * 8)

        self.vendor_id = vendor_id
        self.product_id = product_id
        if vendor_id not in EMBRAVA_VENDOR_IDS:
            raise BlyncLightUnknownDevice(self.identifier)
        self.device = hid.device()
        try:
            self.device.open(vendor_id, product_id)
        except OSError:
            raise BlyncLightInUse(self.identifier)
        except ValueError:
            raise BlyncLightNotFound(self.identifier)
        self.reset()
        self.immediate = immediate

    red = BlyncCommand(56, 8)
    blue = BlyncCommand(48, 8)
    green = BlyncCommand(40, 8)
    off = BlyncCommand(32, 1)
    dim = BlyncCommand(33, 1)
    flash = BlyncCommand(34, 1)
    speed = BlyncSpeed(35, 3)
    repeat = BlyncCommand(29, 1)
    play = BlyncCommand(28, 1)
    music = BlyncCommand(24, 4)
    mute = BlyncCommand(23, 1)
    volume = BlyncCommand(16, 4)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.identifier})"

    def __str__(self):
        lines = [f" Light:{self.identifier}", f" Value:{super().__str__()}"]
        for k, v in self.status.items():
            lines.append(f"{k.capitalize():>6s}:{v}")
        return "\n".join(lines)

    def __del__(self):

        self.device.close()

    def update(self, force: bool = False) -> None:
        """
        """
        if self.immediate or force:
            self.device.write(self.bytes)
            return

    def reset(self, flush: bool = True) -> None:
        """
        """
        with self.updates_paused():
            self[64:72] = 0
            self.red = 0
            self.blue = 0
            self.green = 0
            self.off = 1
            self.dim = 0
            self.flash = 0
            self.speed = 1
            self.repeat = 0
            self.play = 0
            self.music = 0
            self.mute = 0
            self.volume = 0
            self[0:16] = END_OF_COMMAND

        self.update(force=flush)

    @property
    def identifier(self):
        return f"0x{self.vendor_id:04x}:0x{self.product_id:04x}"

    @property
    def status(self) -> Dict[str, str]:
        try:
            return self._status
        except AttributeError:
            pass

        self._status = {
            "red": f"0x{self.red:02x}",
            "blue": f"0x{self.blue:02x}",
            "green": f"0x{self.green:02x}",
            "off": f"0x{self.off:1x}",
            "dim": f"0x{self.dim:1x}",
            "flash": f"0x{self.flash:1x}",
            "speed": f"0x{self.speed:1x}",
            "repeat": f"0x{self.repeat:1x}",
            "play": f"0x{self.play:1x}",
            "music": f"0x{self.music:1x}",
            "mute": f"0x{self.mute:1x}",
            "volume": f"0x{self.volume:1x}",
        }

        return self._status

    @property
    def immediate(self):
        return getattr(self, "_immediate", False)

    @immediate.setter
    def immediate(self, new_value: bool) -> None:
        self._immediate = bool(new_value)
        self.update()

    @property
    def on(self) -> bool:
        return not self.off

    @on.setter
    def on(self, new_value: Union[int, bool]) -> None:
        self.off = not new_value

    @property
    def bright(self) -> bool:
        return not self.dim

    @bright.setter
    def bright(self, new_value: Union[int, bool]) -> None:
        self.dim = not new_value

    @property
    def color(self) -> Tuple[int, int, int]:
        return (self.red, self.blue, self.green)

    @color.setter
    def color(self, new_value: Union[int, Tuple[int, int, int]]) -> None:

        if isinstance(new_value, int):
            values = new_value.to_bytes(3, "big")

        if isinstance(new_value, tuple):
            values = new_value

        with self.updates_paused():
            try:
                self.red, self.blue, self.green = values
            except NameError:
                raise TypeError("Expecting a 24-bit color or tuple of bytes.")

    @contextmanager
    def updates_paused(self):
        """Pauses updates to the light until the context manager exits.
        """
        imm = self.immediate
        self.immediate = False
        try:
            yield
        finally:
            self.immediate = imm
