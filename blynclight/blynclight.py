from collections import Sequence
from contextlib import contextmanager
from enum import Enum
from typing import Dict, List, Tuple, Union
from functools import partial, partialmethod, wraps

import hid

from bitvector import BitVector, BitField
from loguru import logger

from .constants import EMBRAVA_VENDOR_IDS, FlashSpeed, END_OF_COMMAND, COMMAND_LENGTH
from .exceptions import BlyncLightInUse, BlyncLightNotFound, BlyncLightUnknownDevice


class BlyncCommand(BitField):
    """BlyncCommand is descriptor which will conditionally write
    the contents of the BlyncLight to the target device when a field
    is updated. 
    """

    def __set__(self, obj, value) -> None:
        super().__set__(obj, value)
        try:
            obj.update()
        except AttributeError:
            logger.error(f"Failed to update {obj!r} after setting {self.name}")


class BlyncColor(BlyncCommand):
    """An eight-bit unsigned integer color value."""


class BlyncOff(BlyncCommand):
    """Single bit toggle that toggles the light on and off."""


class BlyncDim(BlyncCommand):
    """Single bit toggle that dims the light when set."""


class BlyncFlash(BlyncCommand):
    """Single bit toggle that enables flash mode when set."""


class BlyncSpeed(BlyncCommand):

    """BlyncSpeed descriptor sets and gets the speed field of a BlyncLight
    in-memory represenation. The speed field is a bit flag whose valid
    values are 1, 2, and 4 (b001, b010, b100). 
    """

    # If more than one bit is set in the three bit speed field and the
    # flash bit is set, the light will flash exceedingly fast. If speed
    # is zero, the light turns off regardless of off == 0. Bug in the
    # firmware maybe?

    def __get__(self, obj, type=None) -> object:
        v = super().__get__(obj, type)
        return FlashSpeed.value_for_speed(v)

    def __set__(self, obj, value) -> None:
        speed = FlashSpeed.speed_for_value(value)
        super().__set__(obj, speed)


class BlyncRepeat(BlyncCommand):
    """Single bit that toggles music repeat on and off."""


class BlyncPlay(BlyncCommand):
    """Single bit that toggles music start and stop."""


class BlyncMusic(BlyncCommand):
    """Four bit field that chooses which song to play."""


class BlyncVolume(BlyncCommand):
    """Four bit field that controls the volume used to play a song."""


class BlyncMute(BlyncCommand):
    """Single bit toggles that mutes and unmutes playing music."""


class BlyncLight(BitVector):
    """BlyncLight

    The Embrava BlyncLight family of USB connected products responds
    to a 9-byte command word. The command word enables activation or
    deactivation of various features; turning the light on and off,
    changing it's color, causing the light to flash, dimming or
    brightening, playing musical tunes stored in some BlyncLight
    model's firmware, muting or changing the volume of the playing
    music.

    Not all devices have musical capability.

    The recommended way to obtain a BlyncLight object is to use the
    class method get_light().

    >>> light = BlyncLight.get_light()

    Features of the light are controlled by assigning values to
    attributes of the BlyncLight object:

    >>> light.red = 0xff
    >>> light.on = 1
    >>> light.on = 0

    Usage Notes
    ===========

    The BlyncLight object is an in-memory representation of the
    state of the hardware device. I have not been able to discern how
    to read the device's current state, so every time a new object is
    instantiated it writes a known state to the device by default.

    Additionally, any updates to the bit fields in the ByncLight class
    will be immediately written to the hardware device by default.

    Callers can defer hardware updates by setting the 'immediate'
    attribute to False. Any changes to command fields will not be
    written to the device. Setting 'immediate' to True will write the
    current state of the command word to the device. The BlyncLight
    object also provides a context manager method that can be used to
    defer updates:

    >>> with light.updates_paused():
    ...     light.red = 0
    ...     light.blue = 255
    ...     light.green = 0
    ...     light.on = True

    is equivalent to:

    >>> light.immediate = False
    >>> light.red = 0
    >>> light.blue = 255
    >>> light.green = 0
    >>> light.on = True
    >>> light.immediate = True

    is equivalent (almost) to:

    >>> light.color = (0, 255, 0)
    >>> light.on = True

    ===CAVEAT===

    Before turning the light on, make sure to specify a color
    otherwise the device will not emit any light. It can be
    very frustrating to turn the light on and not have any
    noticible effect.

    Command Word Documentation
    ==========================


    The Embrava BlyncLight command word bit fields are:

    report : 8     Must be zero
    red    : 8     Red component value between 0-255
    blue   : 8     Blue component value between 0-255
    green  : 8     Green component value between 0-255
    off    : 1     0==on     1==off
    dim    : 1     0==bright 1==dim
    flash  : 1     0==steady 1==flash
    speed  : 3     0==off 1==low 2==medium 4==fast
    pad    : 2
    mute   : 1     0==unmute 1==mute
    music  : 4     select a built-in musical tune
    play   : 1     0==stop 1==play
    repeat : 1     0==no repeat 1==repeat
    pad    : 2
    volume : 4     1-10, increase volume by 10% per increment
    pad    : 2
    eoc    : 16    End Of Command field, must be 0xffff
    """

    @classmethod
    def available_lights(cls) -> List[Dict[str, Union[int, str]]]:
        """Returns a list of dictionaries describing all the BlyncLight
        devices found. 
        """
        lights = []
        for vendor_id in EMBRAVA_VENDOR_IDS:
            lights.extend(hid.enumerate(vendor_id))
        return lights

    @classmethod
    def get_light(cls, light_id: int = 0, immediate: bool = True):
        """Returns a configured BlyncLight for the supplied `light_id`
        which is an index into the list of available devices discovered.

        :param light_id: int
        :param immediate: bool

        Raises
        - BlyncLightNotFound
        - BlyncLightInUse
        - BlyncLightUnknown
        """
        try:
            light = cls.available_lights()[light_id]
        except IndexError:
            raise BlyncLightNotFound(f"Light not found: {light_id}")

        return cls(light["vendor_id"], light["product_id"], immediate)

    def __init__(self, vendor_id: int, product_id: int, immediate: bool = False):
        """Returns a configured BlyncLight.

        The `immediate` argument initializes the light's immediate property. 
        If `immediate` is False, modified state is not written to the light
        until the user calls BlyncLight.update().  If immediate is True, any
        changes are written to the light immediately.

        :param vendor_id: int
        :param product_id: int

        Raises
        - BlyncLightNotFound
        - BlyncLightInUse
        - BlyncLightUnknown
        """

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

    red = BlyncColor(56, 8)
    blue = BlyncColor(48, 8)
    green = BlyncColor(40, 8)
    off = BlyncOff(32, 1)
    dim = BlyncDim(33, 1)
    flash = BlyncFlash(34, 1)
    speed = BlyncSpeed(35, 3)
    repeat = BlyncRepeat(29, 1)
    play = BlyncPlay(28, 1)
    music = BlyncMusic(24, 4)
    mute = BlyncMute(23, 1)
    volume = BlyncVolume(18, 4)

    def __repr__(self):
        return f"{self.__class__.__name__}(product_id=0x{self.product_id:04x}, vendor_id=0x{self.product_id:04x})"

    def __str__(self):
        lines = [f" Light:{self.identifier}", f" Value:{super().__str__()}"]
        for k, v in self.status.items():
            lines.append(f"{k.capitalize():>6s}:{v}")
        return "\n".join(lines)

    def __del__(self):

        self.device.close()

    def update(self, force: bool = False) -> None:
        """Write the current in-memory representation of the light's state
        to the target light. If immediate or force is True, the write is attempted.
        If not force and not self.immediate, the write is deferred.

        :param force: bool
        """
        if self.immediate or force:
            self.device.write(self.bytes)
            return

    def reset(self, flush: bool = True) -> None:
        """Resets the in-memory representation of the light's state to a known
        state (off=1, speed=1, mute=1, all other bits zero) and writes the state
        to the target light depending on the value of `flush`. 

        :param flush: bool
        """
        with self.updates_paused():
            self[64:72] = 0  # this should always be zero
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
            self.mute = 1
            self.volume = 0
            self[0:16] = END_OF_COMMAND

        self.update(force=flush)

    @property
    def identifier(self):
        """Hexadecimal concatenation of vendor_id and product_id."""
        return f"0x{self.vendor_id:04x}:0x{self.product_id:04x}"

    @property
    def status(self) -> Dict[str, str]:
        """A dictionary representation of the bit vector.
        """
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
    def immediate(self) -> bool:
        """Property which controls the frequency that state is written
        to the target light.
        """
        return getattr(self, "_immediate", False)

    @immediate.setter
    def immediate(self, new_value: bool) -> None:
        self._immediate = bool(new_value)
        self.update()

    @property
    def on(self) -> bool:
        """Reverse logic getter/setter for `off` property.
        """
        return 0 if self.off else 1

    @on.setter
    def on(self, new_value: Union[int, bool]) -> None:
        self.off = 0 if new_value else 1

    @property
    def bright(self) -> bool:
        """Reverse logic getter/setter for `dim` property.
        """
        return not self.dim

    @bright.setter
    def bright(self, new_value: Union[int, bool]) -> None:
        self.dim = not new_value

    @property
    def color(self) -> Tuple[int, int, int]:
        """Returns a 3-tuple of integers: (red, blue, green)."""
        return (self.red, self.blue, self.green)

    @color.setter
    def color(self, new_value: Union[int, Tuple[int, int, int]]) -> None:
        """Sets the red, blue and green color fields from a 24bit integer
        or a 3-tuple of ints. Updates to the device are deferred until all
        three color values are modified. 

        If a 24-bit color value is supplied, it should be of the form:

        0xRRBBGG

        :param new_value: Union[int, tupe(int, int, int)]
        """

        if issubclass(type(new_value), Sequence):
            with self.updates_paused():
                self.red, self.blue, self.green = new_value
            return

        try:
            with self.updates_paused():
                self.red, self.blue, self.green = new_value.to_bytes(3, "big")
            return
        except AttributeError:
            pass

        raise TypeError("Expected a 24-bit color or tuple of bytes.")

    @contextmanager
    def updates_paused(self):
        """Context manager that allows bulk updates to the target lights'
        in-memory state. The context manager saves the current value of
        `immediate` and sets `immediate` to False.  This reduces the number
        writes to the target device and "hides" in-between states that
        may be undesirable. On exit from the context manager, `immediate`
        is restored to it's previous value.
        """
        imm = self.immediate
        self.immediate = False
        try:
            yield
        finally:
            self.immediate = imm
