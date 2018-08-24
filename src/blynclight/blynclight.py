'''Embrava Blynclight Support
'''

from ctypes import cdll, c_byte, c_int, c_uint
from pathlib import Path
from platform import system
from .constants import FlashSpeed, DeviceType


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
        'init_blynclights': ([], c_int),
        'fini_blynclights': ([], None),
        'sync_blynclights': ([c_int], c_int),
        'unique_device_id': ([c_byte], c_uint),
        'device_type': ([c_byte], c_byte),
        'light_on': ([c_byte] * 4, c_int),
        'light_off': ([c_byte], c_int),
        'bright': ([c_byte] * 2, c_int),
        'flash': ([c_byte] * 2, c_int),
        'flash_speed': ([c_byte] * 2, c_int),
        'music': ([c_byte] * 2, c_int),
        'music_repeat': ([c_byte] * 2, c_int),
        'music_volume': ([c_byte] * 2, c_int),
        'music_select': ([c_byte] * 2, c_int),
        'mute': ([c_byte] * 2, c_int),
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
        self._lib = cdll.LoadLibrary(path)
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
