"""Embrava Blynclight Support
"""
from ctypes import Structure, c_uint64
from contextlib import contextmanager
from .hid import HidDevice
from .constants import EMBRAVA_VENDOR_IDS, END_OF_COMMAND, COMMAND_LENGTH, PAD_VALUE
from .exceptions import BlyncLightNotFound, BlyncLightUnknownDevice, BlyncLightInUse


class BlyncLight(Structure):
    """BlyncLight

    The Embrava BlyncLight family of USB connected products responds
    to a 9-byte command word. The command word enables activation or
    deactivation of various features; turning the light on and off,
    changing it's color, causing the light to flash, dimming or
    brightening, playing musical tunes stored in some BlyncLight
    model's firmware, muting or changing the volume of the playing
    music.

    Not all devices have musical capability and music related
    functionality has not yet been tested. 3 Apr 2019

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

    Finally, when a BlyncLight object is deallocated it will attempt
    to return the light to a known quiescent state before releasing
    the device.

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
    red    : 8     Red component varies between 0-255
    blue   : 8     Blue component varies between 0-255
    green  : 8     Green component varies between 0-255
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
    volume : 4     1-10, increase volume by 10%
    pad    : 2
    eoc    : 16    End Of Command field, must be 0xffff

    """

    _fields_ = [
        ("report", c_uint64, 8),
        ("red", c_uint64, 8),
        ("blue", c_uint64, 8),
        ("green", c_uint64, 8),
        ("off", c_uint64, 1),
        ("dim", c_uint64, 1),
        ("flash", c_uint64, 1),
        ("speed", c_uint64, 3),
        ("pad0", c_uint64, 2),
        ("music", c_uint64, 4),
        ("play", c_uint64, 1),
        ("repeat", c_uint64, 1),
        ("pad1", c_uint64, 2),
        ("volume", c_uint64, 4),
        ("pad2", c_uint64, 3),
        ("mute", c_uint64, 1),
        ("eoc", c_uint64, 8),
        # End of Command Word
        # - pad3 and immediate round out the
        #   length of _fields_ to 128 bits
        ("pad3", c_uint64, 63),
        ("immediate", c_uint64, 1),
    ]

    _ignore_ = ("report", "pad", "eoc")

    # XXX available_lights should return a dictionary to keep
    #     from instantiating BlyncLights which makes it harder
    #     to use those devices later on. Otherwise we need to
    #     start caching and managing open USB HID devices which
    #     is complex and error prone.

    @classmethod
    def available_lights(cls):
        """:return: list of dictionaries

        Returns a list of dictonary entries, each entry describing an
        Embrava BlyncLight device. If no matching devices are found,
        an empty list is returned.

        Raises:

        - KeyError if vendor_id key is missing in DeviceInfo dictionaries.

        """

        is_blynclight = lambda d: d["vendor_id"] in EMBRAVA_VENDOR_IDS

        return [info for info in HidDevice.enumerate() if is_blynclight(info)]

    @classmethod
    def get_light(cls, light_id=0):
        """:param light_id: optional integer
        :return: BlyncLight

        Returns a BlyncLight object accessed by index 'light_id' into
        a list returned by available_lights().

        - BlyncLightNotFound raised if light_id is not found.
        - BlyncLightInUse raised if BlyncLight has already been opened.

        """
        try:
            return cls.from_dict(cls.available_lights()[light_id])
        except IndexError:
            raise BlyncLightNotFound(f"Light for {light_id} not found.")

    @classmethod
    def from_dict(cls, info):
        """:param info: dictionary
        :return: BlyncLight

        Returns a BlyncLight configured with the contents of the
        supplied dictionary 'info'. The keys 'vendor_id' and
        'product_id' are required.

        - BlyncLightInUse raised if specified light is already open.
        - KeyError if vendor_id or product_id is missing from the
          input dictionary.

        """
        return cls(info["vendor_id"], info["product_id"])

    @classmethod
    def report_available(cls):
        """Prints an ugly report to stdout about each available BlyncLight
        device. Report sort of lies. A light may be in use and so not really
        "available". I'll fix it later.
        """
        lights = cls.available_lights()
        print("Number of available lights:", len(lights))
        for i, info in enumerate(lights):
            print("{:>20s}:ID:VALUE".format("KEY"))
            for k, v in info.items():
                if len(str(v)) == 0:
                    continue
                if isinstance(v, int):
                    v = hex(v)
                if isinstance(v, bytes):
                    v = v.decode("utf-8")
                print(f"{k:>20s}:{i:02d}:{v:s}")
            print()

    def __init__(self, vendor_id, product_id, immediate=True):
        """:param vendor_id:  16-bit integer
        :param product_id: 16-bit integer
        :param immediate:  optional boolean

        Initialize a BlyncLight for use.

        The vendor_id and product_id together specify a unique USB
        device. The immediate argument configures whether or not the
        object will immediately update the physical device with the
        object's in-memory representation of the command word.

        If immediate is False, the caller will need to set immediate
        to True before updates to the device will occur.

        The following exceptions are raised:

        - BlyncLightUnknownDevice is raised if vendor_id does not
          match known Embrava vendor indentifiers.

        - BlyncLightInUse is raised if the light specified by
          vendor_id:product_id has already been opened.

        - BlyncLightNotFound is raised if the light specified by
          vendor_id:product_id does not exist.

        """
        if vendor_id not in EMBRAVA_VENDOR_IDS:
            raise BlyncLightUnknownDevice(f"unknown vendor id 0x{vendor_id:04}")
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.reset(flush=False)
        self.immediate = immediate

    def reset(self, flush=True):
        """:param flush: optional boolean
        :return: None

        Returns the command word to it's default state and writes the
        command to the device if flush is True.

        On return the immediate attribute is zero.

        """
        self.immediate = 0
        for name, typ, sz in self._fields_:
            setattr(self, name, 0)
        self.off = 1
        if flush:
            self.device.write(self.bytes)

    def __str__(self):
        s = [f"Device: {self.device.identifier}"]
        for name, value in self.status.items():
            s.append(f"\t0x{value:04x} : {name}")
        return "\n".join(s)

    @property
    def status(self):
        """A dictionary representation of the current light status.
        The keys are the command field names and the values are the
        integer contents of those fields.
        """
        retval = {}
        for command in self.commands:
            value = getattr(self, command)
            retval.setdefault(command, value)
        return retval

    def __len__(self):
        """The length of the command word in bytes.
        """
        return COMMAND_LENGTH

    def __del__(self):
        """Sets all light attributes to their default values
        and updates the device before closing the USB device.
        """
        self.reset()
        self.device.close()

    def __setattr__(self, name, value):
        """Setting any BlyncLight command attribute triggers a write
        to the device if the immediate attribute is 1. If immediate
        is 0, the in-memory representation is changed but the
        hardware is not updated with the new values. Setting
        immediate to 1 will flush the in-memory command word
        to the hardware.
        """

        if name.startswith(("report", "pad")):
            super().__setattr__(name, PAD_VALUE)
            return

        if name == "eoc":
            super().__setattr__(name, END_OF_COMMAND)
            return

        super().__setattr__(name, value)
        if name in self.commands and self.immediate:
            n = self.device.write(self.bytes)
            if n != len(self.bytes):
                raise IOError(f"wrote {n} bytes, expected {len(self.bytes)} bytes")

    @property
    def device(self):
        """A blynclight.hid.HidDevice providing write access to
        an Embrava BlyncLight device.
        """
        try:
            return self._device
        except AttributeError:
            pass
        try:
            self._device = HidDevice(self.vendor_id, self.product_id)
        except ValueError:
            raise BlyncLightInUse(self.vendor_id, self.product_id)
        except LookupError:
            raise BlyncLightNotFound(self.vendor_id, self.product_id)
        return self._device

    @property
    def bytes(self):
        """A bytes representation of the 9 byte command word.
        """
        return bytes(self)[: len(self)]

    @property
    def commands(self):
        """List of valid BlyncLight command fields.
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
        the immediate bit is reset to it's previous value, which may trigger
        a write to the hardware.
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

        A three-tuple of 8-bit integers or 24-bit hex number can be
        used to set all three colors at once.

        > red, blue, green = light.colors
        > light.colors = (0xRR, 0xBB, 0xGG)
        > light.colors = 0xRRBBGG

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
        """Inverse logic setter/getter for 'off' attribute.
        """
        return 0 if self.off else 1

    @on.setter
    def on(self, newValue):
        self.off = 0 if newValue else 1

    @property
    def bright(self):
        """Inverse logic setter/getter for 'dim' attribute.
        """
        return 0 if self.dim else 1

    @bright.setter
    def bright(self, newValue):
        self.dim = 0 if newValue else 1
