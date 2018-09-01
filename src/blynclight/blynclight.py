'''Embrava Blynclight Support
'''

import ctypes
from .hid import enumerate as hid_enumerate
from .hid import write as hid_write
from .hid import open as hid_open
from .hid import close as hid_close


class BlyncLight(ctypes.Structure):
    '''BlyncLight

    The Embrava BlyncLight family of USB connected products responds
    to a 9-byte command word. The command word enables activation or
    deactivation of various features; turning the light on and off,
    changing it's color, causing the light to flash, dimming or
    brightening, playing musical tunes stored in some BlyncLight
    model's firmware, muting the music or changing it's volume.

    Not all devices have musical capability and music related functionality
    has not yet been tested. 31 Aug 2018

    The command word's bit fields are defined as:

    report : 8     Always 1 byte zero
    red    : 8     Red component varies between 0-255
    blue   : 8     Blue component varies between 0-255
    green  : 8     Green component varies between 0-255
    off    : 1     0->on 1->off
    dim    : 1     0->bright 1->dim
    flash  : 1     1->flash 0->steady
    speed  : 3     0->off 1->low 2->medium 4->fast
    pad    : 2
    mute   : 1     1->mute 0->unmute
    music  : 4     select a built-in musical tune
    start  : 1     0->stop 1->play
    repeat : 1     0->no repeat 1->repeat
    pad    : 2
    volume : 4     1-10, vary volume by 10%
    pad    : 2
    EOM    : 16    The End of Message field is always 0xfff

    The recommended way to obtain a BlyncLight object is to use either
    of these two class methods: available_lights or first_light.

    >>> lights = BlyncLight.available_lights()

    or

    >>> light = BlyncLight.first_light()


    Usage Notes

    Any changes to the bit fields in the ByncLight class will
    immediately be sent to the associated device by default.
    Callers can defer device update by setting the 'immediate'
    attribute to False and calling device_update when ready
    to send new values to the device. Setting immediate to True
    will then cause any updates to be written without delay to
    the device.

    ===CAVEAT===

    Before turning the light on, make sure to specify a color
    otherwise the device will not emit any light. It can be
    very frustrating to turn the light on and not have any
    noticible effect.

    '''

    _EMBRAVA_VENDOR_ID = 0x2c0d
    _fields_ = [('pad3', ctypes.c_uint64, 56),
                ('report', ctypes.c_uint64, 8),
                ('red', ctypes.c_uint64, 8),
                ('blue', ctypes.c_uint64, 8),
                ('green', ctypes.c_uint64, 8),
                ('off', ctypes.c_uint64, 1),
                ('dim', ctypes.c_uint64, 1),
                ('flash', ctypes.c_uint64, 1),
                ('speed', ctypes.c_uint64, 3),
                ('pad0', ctypes.c_uint64, 2),
                ('mute', ctypes.c_uint64, 1),
                ('music', ctypes.c_uint64, 4),
                ('start', ctypes.c_uint64, 1),
                ('repeat', ctypes.c_uint64, 1),
                ('pad1', ctypes.c_uint64, 2),
                ('volume', ctypes.c_uint64, 4),
                ('pad2', ctypes.c_uint64, 3),
                ('eom', ctypes.c_uint64, 16), ]

    @classmethod
    def available_lights(cls):
        '''Returns a list of BlyncLight objects found at run-time.
        '''
        return [cls._from_dict(d) for d in
                hid_enumerate(vendor_id=cls._EMBRAVA_VENDOR_ID)]

    @classmethod
    def first_light(cls):
        '''Returns the first BlyncLight device found.

        Raises IOError if no lights are found.

        '''
        try:
            return cls.available_lights()[0]
        except IndexError:
            raise IOError('no blynclights found')

    @classmethod
    def _from_dict(cls, device):
        '''Configures a BlyncLight from a DeviceInfo dictionary.
        '''
        return cls(vendor_id=device['vendor_id'],
                   product_id=device['product_id'])

    def __init__(self, vendor_id=None, product_id=1, immediate=True):
        '''
        :param vendor_id:  two-byte integer quantity, defaults to 0x2c0d
        :param product_id: two-byte integer quantity, defaults to 0
        :param immediate:  optional boolean, defaults to True

        The 'immediate' argument indicates whether changes to device
        control bit fields should be immediately written to the device
        or written explicitly by calls to the update_device method.

        This behavior can be changed after instantiating a BlyncLight
        by assigning True or False to the 'immediate' attribute. See
        the 'color' property for an example of how and why this might
        be desired behavior.

        '''
        self.immediate = False  # disable updates until we've got a viable
        # device handle from open
        self.eom = 0xffff
        self.report = 0
        self.on = 0

        vendor_id = vendor_id or self._EMBRAVA_VENDOR_ID
        self._handle = hid_open(vendor_id, product_id)
        if not self._handle:
            msg = f'unable to open device {vendor_id}:{product_id}'
            raise IOError(msg)

        self.vendor_id = vendor_id
        self.product_id = product_id
        self.immediate = immediate

    @property
    def status(self):
        '''A dictionary of current device bit field values.
        '''
        status = {}
        for name, *_ in self._fields_:
            if name in ['report', 'eom',
                        'pad0', 'pad1',
                        'pad2', 'pad3']:
                continue
            v = getattr(self, name, None)
            status.setdefault(name, v)
        return status

    def __del__(self):
        '''Release HID handle when done with object.
        '''
        try:
            hid_close(self._handle)
        except BaseException:
            pass

    def __repr__(self):
        '''
        '''
        return ''.join([f'{self.__class__.__name__}(',
                        f'vendor_id={self.vendor_id},',
                        f'product_id={self.product_id})'])

    def __str__(self):
        # XXX prettier string?
        return '\n'.join(f'{k:10s}: {v:X}' for k, v in self.status.items())

    def __setattr__(self, name, value):
        '''__setattr__ is overridden to allow immediate or deferred
        update of the target device.

        If the BlyncLight attribute 'immediate' is true, the contents
        of the light control bitfields are written to the target
        device (if the attribute being updated is a member of the
        _fields_ array).  See the 'colors' property for an example of
        how immediate can be used to schedule updates to the light
        with more control.
        '''
        if name in ['report', 'pad0', 'pad1', 'pad2', 'pad3']:
            return

        if name == 'eom' and value != 0xffff:
            return

        super().__setattr__(name, value)

        if name == 'immediate':
            return

        if name in [n for n, c, b in self._fields_] and self.immediate:
            self.update_device()

    @property
    def on(self):
        '''The 'on' property is a negative logic alias for the 'off' attribute.

        light.on = 1

        is equivalent to

        light.off = 0

        Note: If the colors are zero when the light is turned on,
              it will shine with black light (but not the fun 70s
              black light that makes white things glow). Author not
              responsible if this somehow creates a black hole.

              To avoid soul crushing 'nothing' when turning the
              light on, be sure to assign a color.
        '''
        return 0 if self.off else 1

    @on.setter
    def on(self, newValue):
        self.off = 0 if newValue else 1

    @property
    def bright(self):
        '''Bright is a negative logic alias for the 'dim' attribute.

        light.bright = 1

        is equivalent to

        light.dim = 0

        Dim/bright only takes effect if the light is on and if a color
        has been written to the device.
        '''
        return 0 if self.dim else 1

    @bright.setter
    def bright(self, newValue):
        self.dim = 0 if newValue else 1

    @property
    def color(self, newValue):
        '''Color is a convenience property to access the red, blue and green
        bit field attributes as a tuple.  The tuple returned is three
        single byte quatities (0-255) representing red, blue and green
        in that order.

        The color property can be set with either an iterator yielding
        at least three integer values, or a single 3-byte hexadecimal
        integer. The hex integer is expected to be structured as
        follows:

        0xRRBBGG

        Setting red, blue and green with the color property has the
        advantage of calling the device update method one time instead
        of three times if you were to update red, blue and green via
        the bit field properties.

        The user could accomplish the same behavior with:

        light.immediate = False
        light.red = newRed
        light.blue = newBlue
        light.immediate = True
        light.green = newGreen   # this assignment triggers update_device()

        '''
        return (self.red, self.blue, self.green)

    @color.setter
    def color(self, newValue):
        prev_imm = self.immediate
        if prev_imm:
            self.immediate = False
        try:
            self.red = (newValue >> 16) & 0x00ff
            self.blue = (newValue >> 8) & 0x00ff
            self.green = newValue & 0x00ff
            self.update_device()
            self.immediate = prev_imm
            return
        except TypeError:
            pass
        self.red, self.blue, self.green = newValue[:3]
        self.update_device()
        self.immediate = prev_imm

    def update_device(self):
        '''This method writes the contents of the BlyncLight 9-byte control
        word to the target device. The method returns True if 9 bytes
        are writtn, otherwise False. If the blynclight.hid.write
        method returns -1, IOError is raised.

        :returns: bool
        '''
        offset = 7
        size = ctypes.sizeof(self) - offset
        ref = ctypes.byref(self, offset)
        nbytes = hid_write(self._handle, ref, size)
        if nbytes == -1:
            # XXX support calling hid_error for better error reporting
            raise IOError('hid_write')
        return nbytes == size
