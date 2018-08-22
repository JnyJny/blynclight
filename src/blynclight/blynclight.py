'''Embrava Blynclight Support
'''

from ctypes import cdll, c_byte, c_int
from pathlib import Path
from platform import system
from .constants import FlashSpeed

class BlyncLightAPI:
    
    _funcs = {
        'init_blynclights': ([],         c_int),
        'fini_blynclights': ([c_int],    None),
        'red_on':           ([c_byte],   c_int),
        'green_on':         ([c_byte],   c_int),
        'blue_on':          ([c_byte],   c_int),
        'cyan_on':          ([c_byte],   c_int),
        'magenta_on':       ([c_byte],   c_int),
        'yellow_on':        ([c_byte],   c_int),
        'white_on':         ([c_byte],   c_int),
        'orange_on':        ([c_byte],   c_int),
        'rgb_on':           ([c_byte]*4, c_int),
        'light_off':        ([c_byte],   c_int),
        'flash_on':         ([c_byte],   c_int),
        'flash_off':        ([c_byte],   c_int),
        'flash_speed':      ([c_byte]*2, c_int),
        'music_select':     ([c_byte]*2, c_int),
        'music_play':       ([c_byte],   c_int),
        'music_stop':       ([c_byte],   c_int),
        'music_repeat_on':  ([c_byte],   c_int),
        'music_repeat_off': ([c_byte],   c_int),
        'mute_on':          ([c_byte],   c_int),
        'mute_off':         ([c_byte],   c_int),
        'music_volume':     ([c_byte]*2, c_int),
        'dim':              ([c_byte],   c_int),
        'bright':           ([c_byte],   c_int),
    }

    def __init__(self):

        for fname, interface in self._funcs.items():
            func = getattr(self.lib, fname)
            func.argtypes, func.restype = interface
            setattr(self, fname, func)
        self.lib.init_blynclights()

    def __del__(self):
        
        self.lib.fini_blynclights(self.nlights)

    @property
    def nlights(self):
        '''
        '''
        return self.lib.init_blynclights()

    @property
    def lib_path(self):
        '''
        '''
        try:
            return self._lib_path
        except AttributeError:
            pass
        self._lib_path = Path(__file__).absolute().parent 
        self._lib_path = self._lib_path / 'libs'
        self._lib_path = self._lib_path / system()
        self._lib_path = self._lib_path / 'libblynclightcontrol.so'
        return self._lib_path

    @property
    def lib(self):
        '''
        '''
        try:
            return self._lib
        except AttributeError:
            pass
        self._lib = cdll.LoadLibrary(self.lib_path)
        return self._lib

    
class BlyncLight:
    '''
    '''

    @classmethod
    def available(cls):
        raise NotImplementedError('available')
    
    def __init__(self, device=0, r=0x0, g=0xff, b=0x0, on=False, api=None):
        '''
        '''
        self.device = device
        self.api = api or BlyncLightAPI()
        self.color = (r, g, b)
        self.on = on 

    def __del__(self):
        '''
        '''
        del(self.api)

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
                 'color'       : self.color,
                 'flashing'    : self.flashing,
                 'flash_speed' : self.flash_speed,
                 'mute'        : self.mute,
                 'volume'      : self.volume,
                 'music'       : self.music,
                 'play'        : self.play,
                 'repeat'      : self.repeat,
                 'dim'         : self.dim }

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
            self.api.rgb_on(self.device, r, g, b)

    @property
    def on(self):
        try:
            return self._on
        except AttributeError:
            pass
        self._on = False
        return self._on

    @on.setter
    def on(self, newValue):
        self._on = newValue
        if self._on:
            r,g,b = self.color
            self.api.rgb_on(self.device, r, g, b)
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
        self._flashing = value
        if self._flashing:
            self.api.flash_start(self.device)
        else:
            self.api.flash_stop(self.device)

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
        if value < FlashSpeed.OFF:
            value = FlashSpeed.OFF
        if value > FlashSpeed.HIGH:
            value = FlashSpeed.HIGH
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
        self._play = value
        if self._play:
            self.api.music_play(self.device)
        else:
            self.api.music_stop(self.device)
            
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
        self._repeat = value
        if self._repeat:
            self.api.music_repeat_on(self.device)
        else:
            self.api.music_repeat_off(self.device)

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
        if self._mute:
            self.api.mute_on(self.device)
        else:
            self.api.mute_off(self.device)

    @property
    def dim(self):
        try:
            return self._dim
        except AttributeError:
            pass
        self._dim = False
        return self._dim

    @dim.setter
    def dim(self, value):
        self._dim = value
        if self._dim:
            self.api.dim(self.device)
        else:
            self.api.bright(self.device)
