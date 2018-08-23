'''Embrava Blynclight Support
'''

from ctypes import cdll, c_byte, c_int
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
        'init_blynclights':    ([],         c_int),
        'fini_blynclights':    ([c_int],    None),
        'refresh_blynclights': ([],         c_int),
        'device_type':         ([c_byte],   c_byte),
        'light_on':            ([c_byte]*4, c_int),
        'light_off':           ([c_byte],   c_int),
        'bright':              ([c_byte]*2, c_int),
        'flash':               ([c_byte]*2, c_int),
        'flash_speed':         ([c_byte]*2, c_int),
        'music':               ([c_byte]*2, c_int),
        'music_repeat':        ([c_byte]*2, c_int),
        'music_volume':        ([c_byte]*2, c_int),
        'music_select':        ([c_byte]*2, c_int),

        'mute':                ([c_byte]*2, c_int),
    }

    def __init__(self):
        '''
        '''

        if self._instance:
            self.nlights = self.refresh()
            return

        self._instance = self
        for fname, interface in self._funcs.items():
            func = getattr(self.lib, fname)
            func.argtypes, func.restype = interface
            setattr(self, fname, func)
        self.nlights = self.lib.init_blynclights()

    def __del__(self):
        '''
        '''
        self.lib.fini_blynclights(self.nlights)

    def refresh(self):
        '''
        '''
        return self.lib.refresh_blynclights()

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
        path = path / 'libblynclightcontrol.so'
        self._lib = cdll.LoadLibrary(path)
        return self._lib

    
class BlyncLight:
    '''
    '''
    
    def __init__(self, device=0, r=0x0, g=0xff, b=0x0, on=False, api=None):
        '''
        '''
        self.device = device
        self.api = api
        self.color = (r, g, b)
        self.on = on 

    def __repr__(self):
        '''
        '''
        return ''.join([f'{self.__class__.__name__}(',
                        f'device={self.device},',
                        f'r={self.color[0]}, ',
                        f'g={self.color[1]}, ',
                        f'b={self.color[2]}, ',
                        f'on={self.on})'])

    def __str__(self):
        '''
        '''
        return '\n'.join([f'{k:12s}: {v}'for k,v in self.status.items()])

    @property
    def status(self):
        '''
        '''
        return { 'on'          : self.on,
                 'bright'      : self.bright,
                 'color'       : self.color,
                 'flashing'    : self.flashing,
                 'flash_speed' : self.flash_speed,
                 'mute'        : self.mute,
                 'volume'      : self.volume,
                 'music'       : self.music,
                 'play'        : self.play,
                 'repeat'      : self.repeat,
             }

    @property
    def device_type(self):
        '''
        '''
        return DeviceType(self.api.device_type(self.device))

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
            r,g,b = colorTuple
            self.api.light_on(self.device, r, g, b)

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
            r,g,b = self.color
            self.api.light_on(self.device, r, g, b)
        else:
            self.api.light_off(self.device)

    @property
    def flashing(self):
        try:
            return self._flashing
        except AttributeError:
            pass
        self._flashing = False
        return self._flashing
        
    @flashing.setter
    def flashing(self, value):
        self._flashing = bool(value)
        self.api.flash(self.device, self._flashing)

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
        self._bright = False
        return self._bright

    @bright.setter
    def bright(self, value):
        self._bright = bool(value)
        self.api.bright(self.device, self._bright)
