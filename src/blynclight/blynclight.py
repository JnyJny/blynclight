'''
'''

import ctypes
import os
import time
from pathlib import Path

from .color import Color, ColorToRGB
from .devicetype import DeviceType
from .flashspeed import FlashSpeed

MAXIMUM_DEVICES = 32

class DeviceInfo(ctypes.Structure):
    _fields_ = [ ('byType', ctypes.c_byte)]


class BlyncLightControl(object):
    _SO = 'libblynclightcontrol.so'

    _dll = ctypes.cdll.LoadLibrary(Path(__file__).
                                   absolute().
                                   parent.
                                   joinpath('libs',
                                            os.uname().sysname,
                                            _SO))
    _blc = None
    
    @classmethod
    def getLight(cls, light_id, color=(0,255,0)):
        '''returns a properly configured light.
        '''

        if not cls._blc:
            cls._blc = cls()
        
        return BlyncLight(light_id, color=color, blc=cls._blc)
    
    def __init__(self):
        '''
        '''

        if self._blc:
            raise Exception('BlyncLightControl is a singleton')
        
        self.find_devices()

    def __del__(self):
        '''
        '''
        self.release_devices()


    def light(self, light_id, color=(0,255,0)):
        '''returns a properly configured BlyncLight.
        '''
        return BlyncLight(light_id, color=color, blc=self)
        

    def _fixup(self, fname, proto=None, retval=None):
        '''
        '''
        proto = (proto or [ctypes.c_byte])
        retval = (retval or ctypes.c_int)
        func = getattr(self._dll, fname)
        func.argtypes = proto
        func.restype = retval
        return func
        
    def find_devices(self, max_dev=MAXIMUM_DEVICES):

        n = ctypes.c_int(max_dev)
        try:
            result = self._find_devices(ctypes.byref(n))
            return n.value
        except AttributeError:
            pass
        self._find_devices = self._fixup('FindDevices',
                                         proto=[ctypes.c_void_p],
                                         retval=ctypes.c_ubyte)
        result = self._find_devices(ctypes.byref(n))
        return n.value

    def release_devices(self):
        '''
        '''
        self._dll.ReleaseDevices()

    def turn_off_light(self, light_id):
        '''
        '''
        try:
            return self._turn_off_light(light_id)
        except AttributeError:
            pass
        self._turn_off_light = self._fixup('TurnOffLight')
        return self._turn_off_light(light_id)

    def turn_on_green_light(self, light_id):
        '''
        '''
        try:
            return self._turn_on_green_light(light_id)
        except AttributeError:
            pass
        self._turn_on_green_light = self._fixup('TurnOnGreenLight')
        return self._turn_on_green_light(light_id)

    def turn_on_red_light(self, light_id):
        '''
        '''
        try:
            return self._turn_on_red_light(light_id)
        except AttributeError:
            pass
        self._turn_on_red_light = self._fixup('TurnOnRedLight')
        return self._turn_on_red_light(light_id)

    def turn_on_magenta_light(self, light_id):
        '''
        '''
        try:
            return self._turn_on_magenta_light(light_id)
        except AttributeError:
            pass
        self._turn_on_magenta_light = self._fixup('TurnOnMagentaLight')
        return self._turn_on_magenta_light(light_id)

    def turn_on_yellow_light(self, light_id):
        '''
        '''
        try:
            return self._turn_on_yellow_light(light_id)
        except AttributeError:
            pass
        self._turn_on_yellow_light = self._fixup('TurnOnYellowLight')
        return self._turn_on_yellow_light(light_id)    

    def turn_on_blue_light(self, light_id):
        '''
        '''
        try:
            return self._turn_on_blue_light(light_id)
        except AttributeError:
            pass
        self._turn_on_blue_light = self._fixup('TurnOnBlueLight')
        return self._turn_on_blue_light(light_id)

    def turn_on_cyan_light(self, light_id):
        '''
        '''
        try:
            return self._turn_on_cyan_light(light_id)
        except AttributeError:
            pass
        self._turn_on_cyan_light = self._fixup('TurnOnCyanLight')
        return self._turn_on_cyan_light(light_id)

    def turn_on_white_light(self, light_id):
        '''
        '''
        try:
            return self._turn_on_white_light(light_id)
        except AttributeError:
            pass
        self._turn_on_white_light = self._fixup('TurnOnWhiteLight')
        return self._turn_on_white_light(light_id)

    def turn_on_orange_light(self, light_id):
        '''
        '''
        try:
            return self._turn_on_orange_light(light_id)
        except AttributeError:
            pass
        self._turn_on_orange_light = self._fixup('TurnOnOrangeLight')
        return self._turn_on_orange_light(light_id)

    def turn_on_rgb_lights(self, light_id, red, green, blue):
        '''
        '''
        try:
            return self._turn_on_rgb_lights(light_id, red, green, blue)
        except AttributeError:
            pass
        self._turn_on_rgb_lights = self._fixup('TurnOnRGBLights',
                                               proto=[ctypes.c_byte] * 4)
        return self._turn_on_rgb_lights(light_id, red, green, blue)

    def turn_on_v30_light(self, light_id):
        '''
        '''
        try:
            return self._turn_on_v30_light(light_id)
        except AttributeError:
            pass
        self._turn_on_v30_light = self._fixup('TurnOnV30Light')
        return self._turn_on_v30_light(light_id)

    def turn_off_v30_light(self, light_id):
        '''
        '''
        try:
            return self._turn_off_v30_light(light_id)
        except AttributeError:
            pass
        self._turn_off_v30_light = self._fixup('TurnOffV30Light')
        return self._turn_off_v30_light(light_id)

    def set_red_color(self, light_id, level):
        try:
            return self._red_color(light_id, level)
        except AttributeError:
            pass
        self._red_color = self._fixup('SetRedColorBrightnessLevel',
                                      proto=[ctypes.c_byte]*2)
        return self._red_color(light_id, level)

    def set_green_color(self, light_id, level):
        try:
            return self._green_color(light_id, level)
        except AttributeError:
            pass
        self._green_color = self._fixup('SetGreenColorBrightnessLevel',
                                      proto=[ctypes.c_byte]*2)
        return self._green_color(light_id, level)    

    def set_blue_color(self, light_id, level):
        try:
            return self._blue_color(light_id, level)
        except AttributeError:
            pass
        self._blue_color = self._fixup('SetBlueColorBrightnessLevel',
                                      proto=[ctypes.c_byte]*2)
        return self._blue_color(light_id, level)

    def start_light_flash(self, light_id):
        try:
            return self._start_light_flash(light_id)
        except AttributeError:
            pass
        self._start_light_flash = self._fixup('StartLightFlash')

        return self._start_light_flash(light_id)

    def stop_light_flash(self, light_id):
        try:
            return self._stop_light_flash(light_id)
        except AttributeError:
            pass
        self._stop_light_flash = self._fixup('StopLightFlash')
        return self._stop_light_flash(light_id)

    def select_light_flash_speed(self, light_id, speed):
        try:
            speed = speed.value
        except AttributeError:
            pass
        try:
            return self._select_light_flash_speed(light_id, speed)
        except AttributeError:
            pass
        self._select_light_flash_speed = self._fixup('SelectLightFlashSpeed',
                                                     proto=[ctypes.c_byte]*2)
        return self._select_light_flash_speed(light_id, speed)

    def set_light_dim(self, light_id):
        try:
            return self._set_light_dim(light_id)
        except AttributeError:
            pass
        self._set_light_dim = self._fixup('SetLightDim')
        return self._set_light_dim(light_id)

    def clr_light_dim(self, light_id):
        try:
            return self._clr_light_dim(light_id)
        except AttributeError:
            pass
        self._clr_light_dim = self._fixup('ClearLightDim')
        return self._clr_light_dim(light_id)
    

    
class BlyncLight(object):
    '''
    '''
    
    def __init__(self, device_id, color=(0,255,0), blc=None):
        '''
        '''
        if not isinstance(blc, BlyncLightControl):
            raise ValueError('missing BlyncLightControl object')
        self.blc = blc
        self.device_id = device_id
        self.reset()
        self.color = color

    def reset(self):
        '''resets the state of the BlyncLight.

        1. Turns light off.
        2. Disables flashing
        3. Flash speed to low
        4. Stops music playback (for models that support music)
        5. Sets music selection to 0
        6. Sets music volume to 0
        7. Disables music volume mute.

        '''
        self.illuminated = False
        self.flashing = False
        self.playing = False
        self.flash_speed = FlashSpeed.LOW
        self.blc.turn_off_light(self.device_id)

    def __repr__(self):
        '''
        '''
        return f'{self.__class__.__name__}(id={self.device_id})'

    def __del__(self):
        '''
        '''
        self.reset()

    def on(self):
        '''Turns the light on.
        '''

        r,g,b = self.color
        v = self.blc.turn_on_rgb_lights(self.device_id, r, g, b)
        self.illuminated = bool(v == 0)

    def off(self):
        '''Turns the light off.
        '''
        v = self.blc.turn_off_light(self.device_id)
        self.illuminated = not bool(v == 0)

    @property
    def red(self):
        '''Red light color, integer between 0 and 255.
        '''
        try:
            return self.color[0]
        except TypeError:
            pass
        return ColorToRGB(self.color)[0]

    @red.setter
    def red(self, newRed):
        r,g,b = self.color
        self.color = (newRed, g, b)

    @property
    def green(self):
        '''Green light color, integer between 0 and 255.
        '''
        try:
            return self.color[1]
        except TypeError:
            pass
        return ColorToRGB(self.color)[1]
        
    @green.setter
    def green(self, newGreen):
        r,g,b = self.color
        self.color = (r, newGreen, b)

    @property
    def blue(self):
        '''Blue light color, integer between 0 and 255.
        '''
        try:
            return self.color[2]
        except TypeError:
            pass
        return ColorToRGB(self.color)[2]

    @blue.setter
    def blue(self, newBlue):
        r,g,b = self.color
        self.color = (r, g, newBlue)
        
    @property
    def color(self):
        '''Tuple of red, green and blue color values.
        Colors may be in the range of zero to 255.
        '''
        try:
            return self._color
        except AttributeError:
            pass
        self._color = (0, 0, 0)
        return self._color

    @color.setter
    def color(self, newColor):
        
        self._color = tuple(newColor[:3])
        if self.illuminated:
            self.on()

    @property
    def dim(self):
        '''
        '''
        try:
            return self._dim
        except AttributeError:
            pass
        self._dim = False


    @dim.setter
    def dim(self, newValue):
        '''
        '''
        
        if bool(newValue):
            v = self.blc.set_light_dim(self.device_id)
            self._dim = bool(v == 0)
        else:
            v = self.blc.clr_light_dim(self.device_id)
            self._dim = not bool(v == 0)

    @property
    def flash(self):
        try:
            return self._flash
        except AttributeError:
            pass
        self._flash = False
        return self._flash

    @flash.setter
    def flash(self, newValue):
        '''
        '''
        if bool(newValue):
            v = self.blc.start_light_flash(self.device_id)
            self._flash = bool(v == 0)
        else:
            v = self.blc.stop_light_flash(self.device_id)
            self._flash = not bool(v == 0)
            
    @property
    def flash_speed(self):
        '''
        '''
        try:
            return self._flash_speed
        except AttributeError:
            pass
        self._flash_speed = FlashSpeed.LOW
        return self._flash_speed

    @flash_speed.setter
    def flash_speed(self, newValue):
        
        if isinstance(newValue, FlashSpeed):
            self._flash_speed = newValue
        else:
            self._flash_speed = FlashSpeed(newValue)
        self.blc.select_light_flash_speed(self.device_id,
                                          self._flash_speed.value)
        
    def cycle(self, colors, interval_ms=100, repeat=1, preserve=True):
        '''Cycle between colors.

             colors: list of rgb tuples
        interval_ms: optional integer
             repeat: optional integer
           preserve: optional boolean

        '''
        
        if not self.illuminated:
            return
            
        if preserve:
            old_color = self.color
        for n in range(repeat):
            for color in colors:
                self.color = color
                time.sleep(interval_ms/100)
        if preserve:
            self.color = old_color
        
        
    
