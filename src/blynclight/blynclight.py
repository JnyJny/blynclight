"""Embrava Blynclight Support
"""
import ctypes
from .hid import HidDevice
from .constants import EMBRAVA_VENDOR_IDS
from contextlib import contextmanager


class BlyncLight(ctypes.Structure):

    """BlyncLight

    The Embrava BlyncLight family of USB connected products responds
    to a 9-byte command word. The command word enables activation or
    deactivation of various features; turning the light on and off,
    changing it's color, causing the light to flash, dimming or
    brightening, playing musical tunes stored in some BlyncLight
    model's firmware, muting the music or changing it's volume.

    Not all devices have musical capability and music related functionality
    has not yet been tested. 31 Aug 2018

    The recommended way to obtain a BlyncLight object is to use either
    of these two class methods: available_lights or first_light.

    >>> lights = BlyncLight.available_lights()

    or

    >>> light = BlyncLight.first_light()

    Usage Notes

    Any updates to the bit fields in the ByncLight class will
    immediately be sent to the associated device by default.  Callers
    can defer device update by setting the 'immediate' attribute to
    False. Any changes to command fields will not be written to the
    device. Setting 'immediate' to True will then write the current
    state of the command buffer to the device.

    ===CAVEAT===

    Before turning the light on, make sure to specify a color
    otherwise the device will not emit any light. It can be
    very frustrating to turn the light on and not have any
    noticible effect.

    
    The Embrava BlyncLight command word's bit fields are:

    report : 8     Must be zero
    red    : 8     Red component varies between 0-255
    blue   : 8     Blue component varies between 0-255
    green  : 8     Green component varies between 0-255
    off    : 1     0==on     1==off
    dim    : 1     0==bright 1==dim
    flash  : 1     0==steady 1==>flash  
    speed  : 3     0==off 1==low 2==medium 4==fast
    pad    : 2
    mute   : 1     0==unmute 1==mute 
    music  : 4     select a built-in musical tune
    play   : 1     0==>stop 1==play
    repeat : 1     0==no repeat 1==repeat
    pad    : 2
    volume : 4     1-10, increase volume by 10%
    pad    : 2
    eob    : 16    End Of Buffer field, must be 0xffff
    """

    _fields_ = [
        ("report", ctypes.c_uint64, 8),
        ("red", ctypes.c_uint64, 8),
        ("blue", ctypes.c_uint64, 8),
        ("green", ctypes.c_uint64, 8),
        ("off", ctypes.c_uint64, 1),
        ("dim", ctypes.c_uint64, 1),
        ("flash", ctypes.c_uint64, 1),
        ("speed", ctypes.c_uint64, 3),
        ("pad0", ctypes.c_uint64, 2),
        ("music", ctypes.c_uint64, 4),
        ("play", ctypes.c_uint64, 1),
        ("repeat", ctypes.c_uint64, 1),
        ("pad1", ctypes.c_uint64, 2),
        ("volume", ctypes.c_uint64, 4),
        ("pad2", ctypes.c_uint64, 3),
        ("mute", ctypes.c_uint64, 1),
        ("eob", ctypes.c_uint64, 16),
        ("pad3", ctypes.c_uint64, 23),
        ("immediate", ctypes.c_uint64, 1),
    ]

    _ignore_ = ("report", "pad", "eob")

    @classmethod
    def available_lights(cls):
        """Returns a list of BlyncLight objects found at run-time.
        If no BlyncLights are found, an empty list is returned.
        """
        lights = []
        for devi in HidDevice.enumerate():
            if devi["vendor_id"] in EMBRAVA_VENDOR_IDS:
                light = cls(
                    vendor_id=devi["vendor_id"], product_id=devi["product_id"]
                )
                lights.append(light)
        return lights

    @classmethod
    def first_light(cls):
        """Returns the first BlyncLight found at run-time.

        ValueError is raised if no light is found.
        """
        try:
            return cls.available_lights()[0]
        except IndexError:
            raise ValueError("No BlyncLights Found")

    def __init__(self, vendor_id, product_id, immediate=True):
        """
        """
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.reset(flush=False)
        self.immediate = immediate

    def reset(self, flush=True):
        """
        """
        self.immediate = 0
        for name, typ, sz in self._fields_:
            setattr(self, name, 0)
        self.off = 1
        self.eob = 0xFFFF
        if flush:
            self.device.write(self.bytes)

    def __str__(self):
        s = [f"{self!r}"]
        for name in self.commands:
            value = getattr(self, name)
            s.append(f"\t0x{value:04x} : {name}")
        return "\n".join(s)

    def __len__(self):
        """The length of the command buffer in bytes.
        """
        return 9

    def __del__(self):
        self.reset()
        self.device.close()

    def __setattr__(self, name, value):
        """
        """
        super().__setattr__(name, value)
        if name in self.commands and self.immediate:
            self.device.write(self.bytes)

    @property
    def device(self):
        try:
            return self._device
        except AttributeError:
            pass
        self._device = HidDevice(self.vendor_id, self.product_id)
        return self._device

    @property
    def bytes(self):
        """Nine-byte string representation of the command buffer.
        """
        return bytes(self)[: len(self)]

    @property
    def commands(self):
        """List of valid BlyncLight command directives.
        """
        try:
            return self._commands
        except AttributeError:
            pass
        self._commands = [
            f for f, t, s in self._fields_ if not f.startswith(self._ignore_)
        ]
        return self._commands

    @contextmanager
    def updates_paused(self):
        """Context manager that suspends immediate updating of the device
        for the duration of the manager's execution. When the manager exits
        the immediate bit is reset to it's previous value.
        """
        imm = self.immediate
        self.immediate = 0
        try:
            yield
        finally:
            self.immediate = imm

    @property
    def color(self):
        """A tuple of (red, blue, green) hexadecimal values.

        A tuple or a 24-bit hex number can be used to set all
        three colors at once. 

        e.g.
        
        >> light.colors = (0xaa, 0xbb, 0xcc)
        >> light.colors = 0xaabbcc

        """
        return (self.red, self.blue, self.green)

    @color.setter
    def color(self, newValue):
        with self.updates_paused():
            try:
                self.red = (newValue >> 16) & 0x00FF
                self.blue = (newValue >> 8) & 0x00FF
                self.green = newValue & 0x00FF
                return
            except TypeError:
                pass
            self.red, self.blue, self.green = newValue[:3]

    @property
    def on(self):
        """Inverse logic accessor for 'off'.
        """
        return 0 if self.off else 1

    @on.setter
    def on(self, newValue):
        self.off = 0 if newValue else 1

    @property
    def bright(self):
        """Inverse logic accessor for 'dim'.
        """
        return 0 if self.dim else 1

    @bright.setter
    def bright(self, newValue):
        self.dim = 0 if newValue else 1
