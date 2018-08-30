'''Embrava Blynclight Support
'''

import ctypes
import enum
import atexit
from pathlib import Path
from platform import system
from .constants import FlashSpeed, DeviceType, MusicVolume
from .hid import enumerate as hid_enumerate
from .hid import write as hid_write
from .hid import open as hid_open
from .hid import read as hid_read
from .hid import close as hid_close

class BlyncLight_API:

    _instance = None

    @classmethod
    def available_lights(cls):
        '''
        '''
        api = cls()
        return [BlyncLight(n, api=api) for n in range(api.nlights)]

    @classmethod
    def first_light(cls):
        '''
        '''
        return cls.available_lights()[0]

    _funcs = {
        'init_blynclights': ([], ctypes.c_int),
        'fini_blynclights': ([], None),
        'sync_blynclights': ([ctypes.c_int], ctypes.c_int),
        'unique_device_id': ([ctypes.c_byte], ctypes.c_uint),
        'device_type': ([ctypes.c_byte], ctypes.c_byte),
        'light_on': ([ctypes.c_byte] * 4, ctypes.c_int),
        'light_off': ([ctypes.c_byte], ctypes.c_int),
        'bright': ([ctypes.c_byte] * 2, ctypes.c_int),
        'flash': ([ctypes.c_byte] * 2, ctypes.c_int),
        'flash_speed': ([ctypes.c_byte] * 2, ctypes.c_int),
        'music': ([ctypes.c_byte] * 2, ctypes.c_int),
        'music_repeat': ([ctypes.c_byte] * 2, ctypes.c_int),
        'music_volume': ([ctypes.c_byte] * 2, ctypes.c_int),
        'music_select': ([ctypes.c_byte] * 2, ctypes.c_int),
        'mute': ([ctypes.c_byte] * 2, ctypes.c_int),
    }

    def __init__(self):
        '''
        '''
        # XXX BlyncLight_API is a singleton
        if self._instance:
            self.refresh()
            return

        self._instance = self
        for fname, interface in self._funcs.items():
            func = getattr(self.lib, fname)
            func.argtypes, func.restype = interface
            setattr(self, fname, func)
        self.lib.init_blynclights()

    def __del__(self):
        '''
        '''
        self.lib.fini_blynclights()

    def refresh(self):
        '''
        '''
        return self.lib.sync_blynclights(1)

    @property
    def nlights(self):
        '''Number of lights last detected.
        '''
        return self.lib.sync_blynclights(30)

    @property
    def lib(self):
        '''
        '''
        try:
            return self._lib
        except AttributeError:
            pass
        path = Path(__file__).absolute().parent
        path = path / 'libs'
        path = path / system()
        path = path / 'libblynclight_api.so'
        self._lib = ctypes.cdll.LoadLibrary(path)
        return self._lib


class BlyncLight:
    '''
    '''

    def __init__(self, device=0, api=None):
        '''
        '''
        if not isinstance(api, BlyncLight_API):
            raise ValueError(f'api is not a BlyncLight_API')
        self.device = device
        self.api = api

    def __repr__(self):
        '''
        '''
        return f'{self.__class__.__name__}(device={self.device})'

    def __str__(self):
        '''
        '''
        return '\n'.join([f'{k:12s}: {v}'for k, v in self.status.items()])

    @property
    def status(self):
        '''
        '''
        return {'device': self.device,
                'device_type': self.device_type,
                'unique_id': self.unique_id,
                'on': self.on,
                'bright': self.bright,
                'color': self.color,
                'flash': self.flash,
                'flash_speed': self.flash_speed,
                'mute': self.mute,
                'volume': self.volume,
                'music': self.music,
                'play': self.play,
                'repeat': self.repeat,
                }

    @property
    def device_type(self):
        '''
        '''
        return DeviceType(self.api.device_type(self.device))

    @property
    def unique_id(self):
        try:
            return self._unique_id
        except AttributeError:
            pass
        self._unique_id = self.api.unique_device_id(self.device)
        return self._unique_id

    @property
    def on(self):
        try:
            return self._on
        except AttributeError:
            pass
        self._on = False
        return self._on

    @on.setter
    def on(self, value):
        self._on = bool(value)
        if self._on:
            r, g, b = self.color
            self.api.light_on(self.device, r, g, b)
        else:
            self.api.light_off(self.device)

    @property
    def color(self):
        '''
        '''
        try:
            return self._color
        except AttributeError:
            pass
        self._color = (0, 0xff, 0)
        return self._color

    @color.setter
    def color(self, colorTuple):
        self._color = colorTuple
        if self.on:
            r, g, b = colorTuple
            self.api.light_on(self.device, r, g, b)

    @property
    def flash(self):
        try:
            return self._flash
        except AttributeError:
            pass
        self._flash = False
        return self._flash

    @flash.setter
    def flash(self, value):
        self._flash = bool(value)
        self.api.flash(self.device, self._flash)

    @property
    def flash_speed(self):
        try:
            return self._flash_speed
        except AttributeError:
            pass
        self._flash_speed = FlashSpeed.OFF
        return self._flash_speed

    @flash_speed.setter
    def flash_speed(self, value):
        self._flash_speed = FlashSpeed(value)
        self.api.flash_speed(self.device, self._flash_speed.value)

    @property
    def play(self):
        try:
            return self._play
        except AttributeError:
            pass
        self._play = False
        return self._play

    @play.setter
    def play(self, value):
        self._play = bool(value)
        self.api.music(self.device, self._play)

    @property
    def music(self):
        try:
            return self._music
        except AttributeError:
            pass
        self._music = 0
        return self._music

    @music.setter
    def music(self, value):
        self._music = value
        self.api.music_select(self.device, self._music)

    @property
    def volume(self):
        try:
            return self._volume
        except AttributeError:
            pass
        self._volume = 0
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        self.api.music_volume(self.device, self._volume)

    @property
    def repeat(self):
        try:
            return self._repeat
        except AttributeError:
            pass
        self._repeat = False
        return self._repeat

    @repeat.setter
    def repeat(self, value):
        self._repeat = bool(value)
        self.api.music_repeat_on(self.device, self._repeat)

    @property
    def mute(self):
        try:
            return self._mute
        except AttributeError:
            pass
        self._mute = False
        return self._mute

    @mute.setter
    def mute(self, value):
        self._mute = value
        self.api.mute_on(self.device, self._mute)

    @property
    def bright(self):
        try:
            return self._bright
        except AttributeError:
            pass
        self._bright = True
        return self._bright

    @bright.setter
    def bright(self, value):
        self._bright = bool(value)
        self.api.bright(self.device, self._bright)



class BlyncLightStatus(ctypes.Structure):
    _fields_ = [('bigpad', ctypes.c_uint64, 56),
                ('report', ctypes.c_uint64, 8),
                ('red', ctypes.c_uint64, 8),
                ('blue', ctypes.c_uint64, 8),
                ('green', ctypes.c_uint64, 8),
                ('pad0', ctypes.c_uint64, 2),
                ('speed', ctypes.c_uint64, 3),
                ('flash', ctypes.c_uint64, 1),
                ('dim', ctypes.c_uint64, 1),
                ('off', ctypes.c_uint64, 1),
                ('pad1', ctypes.c_uint64, 2),
                ('repeat', ctypes.c_uint64, 1),
                ('start', ctypes.c_uint64, 1),
                ('music', ctypes.c_uint64, 4),
                ('mute', ctypes.c_uint64, 1),
                ('pad2', ctypes.c_uint64, 3),
                ('volume', ctypes.c_uint64, 4),
                ('eob', ctypes.c_uint64, 16)]

    def as_dict(self):
        ret = {}
        for name, *_ in self._fields_:
            if 'pad' in name:
                continue
            v = getattr(self, name, None)
            ret.setdefault(name, v)
        return ret

    @property
    def value(self):
        r = 0
        shift = sum(b for n,t,b in self._fields_)
        for name, ctype, bits in self._fields_:
            shift -= bits
            r |= getattr(self, name) << shift
        return r

class NewBlyncLight(BlyncLightStatus):

    @classmethod
    def available_lights(cls):
        return [cls.from_dict(d) for d in hid_enumerate(vendor_id=0x2c0d)]

    @classmethod
    def first_light(cls):
        return cls.available_lights()[0]

    @classmethod
    def from_dict(cls, device):
        return cls(vendor_id=device['vendor_id'],
                   product_id=device['product_id'])

    def __init__(self, vendor_id, product_id, value=None):
        self._handle = hid_open(vendor_id, product_id)
        self.eob = 0xffff
        self.on = 0

    def __del__(self):
        
        hid_close(self._handle)

    def __repr__(self):

        return ''.join([f'{self.__class__.__name__}(',
                        'vendor_id={vendor_id},',
                        'product_id={product_id})'])

    def __str__(self):
        return '\n'.join(f'{k:10s}: {v:X}' for k,v in self.as_dict().items())

    @property
    def on(self):
        return 0 if self.off else 1

    @on.setter
    def on(self, newValue):
        self.off = 0 if newValue else 1

    @property
    def bright(self):
        return 0 if self.dim else 1

    @bright.setter
    def bright(self, newValue):
        self.dim = 0 if newValue else 1

    def send(self):

        offset = 7
        return hid_write(self._handle,
                         ctypes.byref(self, offset),
                         ctypes.sizeof(self) - offset)
