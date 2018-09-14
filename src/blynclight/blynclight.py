'''Embrava Blynclight Support
'''
import ctypes
import usb.core

from .constants import EMBRAVA_VENDOR_ID

class BlyncLightBitfields(ctypes.Structure):
    _fields_ = [('red', ctypes.c_uint64, 8),
                ('blue', ctypes.c_uint64, 8),
                ('green', ctypes.c_uint64, 8),
                ('off', ctypes.c_uint64, 1),
                ('dim', ctypes.c_uint64, 1),
                ('flash', ctypes.c_uint64, 1),
                ('speed', ctypes.c_uint64, 3),
                ('pad0', ctypes.c_uint64, 2),
                ('music', ctypes.c_uint64, 4),
                ('play', ctypes.c_uint64, 1),
                ('repeat', ctypes.c_uint64, 1),
                ('pad1', ctypes.c_uint64, 2),
                ('volume', ctypes.c_uint64, 4),
                ('pad2', ctypes.c_uint64, 3),
                ('mute', ctypes.c_uint64, 1),
                ('eob0', ctypes.c_uint64, 8),
                ('eob1', ctypes.c_uint64, 8),]

class BlyncLightCommand(ctypes.Union):
    _fields_ = [ ('field', BlyncLightBitfields),
                 ('bytes', ctypes.c_ubyte * 8),
                 ('word', ctypes.c_ulonglong),]
    

class BlyncLight(BlyncLightCommand):
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

    red    : 8     Red component varies between 0-255
    blue   : 8     Blue component varies between 0-255
    green  : 8     Green component varies between 0-255
    off    : 1     0->on 1->off
    dim    : 1     0->bright 1->dim
    bflash : 1     1->flash 0->steady
    bspeed : 3     0->off 1->low 2->medium 4->fast
    pad    : 2
    mute   : 1     1->mute 0->unmute
    music  : 4     select a built-in musical tune
    play   : 1     0->stop 1->play
    repeat : 1     0->no repeat 1->repeat
    pad    : 2
    volume : 4     1-10, increase volume by 10%
    pad    : 2

    The recommended way to obtain a BlyncLight object is to use either
    of these two class methods: available_lights or first_light.

    >>> lights = BlyncLight.available_lights()

    or

    >>> light = BlyncLight.first_light()

    Usage Notes

    Any updates to the bit fields in the ByncLight class will
    immediately be sent to the associated device by default.  Callers
    can defer device update by setting the 'immediate' attribute to
    False and calling device_update when ready to send new values to
    the device. Setting 'immediate' to True will then cause any
    following updates to sent without delay to the device.

    ===CAVEAT===

    Before turning the light on, make sure to specify a color
    otherwise the device will not emit any light. It can be
    very frustrating to turn the light on and not have any
    noticible effect.

    '''

    @classmethod
    def available_lights(cls, vendor_id=None):
        '''Returns a list of BlyncLight objects found at run-time.
        '''
        vendor_id = vendor_id or EMBRAVA_VENDOR_ID
        return [cls(d) for d in usb.core.find(idVendor=vendor_id, find_all=True)]

    @classmethod
    def light_info(cls, light_id=-1, vendor_id=None):
        '''
        '''
        vendor_id = vendor_id or EMBRAVA_VENDOR_ID
        lights = usb.core.find(idVendor=vendor_id, find_all=True)
                               
        return lights[light_id] if light_id >= 0 else lights

    @classmethod
    def first_light(cls, vendor_id=None):
        '''Returns the first BlyncLight device found.
        '''
        vendor_id = vendor_id or EMBRAVA_VENDOR_ID
        return cls(usb.core.find(idVendor=vendor_id))


    def __init__(self, device, immediate=True):
        '''
        :param device: 
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
        self.on = 0
        self.device = device
        self.immediate = immediate

    @property
    def device(self):
        try:
            return self._device
        except AttributeError:
            pass
        self._device = None
        return self._device

    @device.setter
    def device(self, newValue):
        self._device = newValue
        try:
            for cfg in self._device:
                for n in [i.bInterfaceNumber for i in cfg]:
                    if self._device.is_kernel_driver_active(n):
                        self._device.detach_kernel_driver(n)
            self._device.set_configuration()
        except Exception as e:
            raise ValueError()

    @property
    def status(self):
        '''A dictionary of current device bit field values.
        '''
        status = {}
        for name, *_ in self._fields_['fields']._fields:
            if name.startswith('pad'):
                continue
            v = getattr(self, name, None)
            status.setdefault(name, v)
        return status

    def __repr__(self):
        '''
        '''
        return ''.join([f'{self.__class__.__name__}(',
                        f'device={self.device!r})'])

    def __str__(self):
        # XXX prettier string?
        return '\n'.join(f'{k:10s}: {v:X}' for k, v in self.status.items())

    def __setattr__(self, name, value):
        '''__setattr__ is overridden to allow immediate or deferred
        update of the target device.

        If the BlyncLight attribute 'immediate' is true, the contents
        of the light control bitfields are written to the target
        device (if the attribute being updated is a member of the
        _fields_ array).  See the 'color' property for an example of
        how 'immediate' can be used to perform batch updates to the
        light's state.
        '''
        super().__setattr__(name, value)

        if name == 'immediate':
            return

        if self.immediate:
            self.update_device()

    @property
    def red(self):
        return self.field.red

    @red.setter
    def red(self, newValue):
        self.field.red = newValue & 0xff

    @property
    def blue(self):
        return self.field.blue

    @blue.setter
    def blue(self, newValue):
        self.field.blue = newValue & 0xff

    @property
    def green(self):
        return self.field.green

    @green.setter
    def green(self, newValue):
        self.field.green = newValue & 0xff


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
        return 0 if self.field.off else 1

    @on.setter
    def on(self, newValue):
        self.field.off = 0 if newValue else 1

    @property
    def bright(self):
        '''Bright is a negative logic alias for the 'dim' attribute.

        light.bright = 1

        is equivalent to

        light.dim = 0

        Dim/bright only takes effect if the light is on and if a color
        has been written to the device.
        '''
        return 0 if self.field.dim else 1

    @bright.setter
    def bright(self, newValue):
        self.field.dim = 0 if newValue else 1

    @property
    def color(self):
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
        return (self.field.red, self.field.blue, self.field.green)

    @color.setter
    def color(self, newValue):
        prev_imm = self.immediate
        if prev_imm:
            self.immediate = False
        try:
            self.field.red = (newValue >> 16) & 0x00ff
            self.field.blue = (newValue >> 8) & 0x00ff
            self.field.green = newValue & 0x00ff
            self.update_device()
            self.immediate = prev_imm
            return
        except TypeError:
            pass
        self.field.red, self.field.blue, self.field.green = newValue[:3]
        if prev_imm:
            self.update_device()
        self.immediate = prev_imm

    @property
    def flash(self):
        '''Boolean controlling whether the device is in flash mode.

        This property is linked to the speed property in the following way:

        If flash is toggled from 0 to 1 and speed is zero, speed is set to 1

        If callers want to control the flash and speed bitfields directly,
        assign values to the bflash and bspeed attributes.
        '''
        return self.field.flash

    @flash.setter
    def flash(self, newValue):
        self.field.flash = 1 if newValue else 0
        if self.field.flash and self.field.speed == 0:
            self.field.speed = 1

    @property
    def speed(self):
        '''Device light flash speed:
           0 - off
           1 - slow
           2 - medium
           3 - fast

        This property is coupled to the flash property and will set flash
        to off if speed is set to zero. If the caller wants to set the
        flash mode and flash speed directly, use the bflash and bspeed
        attributes instead.
        '''
        # XXX this is ugly but works
        if self.field.speed == 0:
            return 0
        if self.field.speed == 1:
            return 1
        if self.field.speed == 2:
            return 2
        if self.field.speed == 4:
            return 3
        raise ValueError(f'speed out of bounds {self.field.speed}')

    @speed.setter
    def speed(self, newValue):
        if newValue == 0:
            self.field.speed = 0
            self.field.flash = 0
        else:
            self.field.speed = (1 << newValue-1) & 0x07

    _bmRequestType = 0x21
    _bRequest = 0x9
    _wValue = 0x200
    _wIndex = 0
    _timeout = 1000

    def update_device(self):
        '''This method writes the contents of the BlyncLight control
        word to the target device. The method returns True if the word
        is written, otherwise False.
        :returns: bool
        '''


        
        nbytes = self.device.ctrl_transfer(self._bmRequestType,
                                           self._bRequest,
                                           self._wValue,
                                           self._wIndex,
                                           self.bytes,
                                           self._timeout)
        return nbytes == len(self.bytes)



    
