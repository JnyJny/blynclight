
import ctypes
import os
import time
import platform
from pathlib import Path

from .color import ColorToRGB
from .constants import (Color,
                        FlashSpeed,
                        DeviceType,
                        DeviceInfo)


class BlyncLightControl(object):
    '''
    '''
    
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
        '''Returns a configured BlyncLight.
        '''
        cls._get_so()
        return BlyncLight(light_id, color=color, blc=cls._blc)

    @classmethod
    def available_lights(cls):
        '''Returns a list of available BlyncLight device indices and types.
        '''
        cls._get_so()
        return [(i,str(t)) for i,t in enumerate(cls._blc.devices)
                if t != DeviceType.INVALID]

    @classmethod
    def _get_so(cls):
        
        if not cls._blc:
            cls._blc = cls()
        return cls._blc
    
    def __init__(self):
        '''
        '''

        if self._blc:
            raise Exception('BlyncLightControl is a singleton')
        

    def __del__(self):
        '''Releases all configured devices when deleted.
        '''
        self.release_devices()


    def light(self, light_id, color=(0,0,0)):
        '''Returns a configured BlyncLight.
        '''
        return BlyncLight(light_id, color=color, blc=self)

    # The following fuctions are stri

    def _fixup(self, fname, proto=None, retval=None):
        '''Updates ctypes functions with prototype and return value types.
        '''
        proto = (proto or [ctypes.c_byte])
        retval = (retval or ctypes.c_int)
        func = getattr(self._dll, fname)
        func.argtypes = proto
        func.restype = retval
        return func
    

    @property
    def devices(self):
        ''' List of DeviceInfo
        '''

        self._dll.init_blynclights()
        DeviceInfo_p = ctypes.POINTER(DeviceInfo * self._dll.MAXDEV)
        devs = ctypes.cast(self._dll.asDeviceInfo, DeviceInfo_p)
        return [DeviceType(d.byType) for d in devs.contents if d.byType]


    def release_devices(self):
        '''ReleaseDevices

        This function releases the resources reserved for the devices
        up on calling the FindDevices function.  
        '''
        self._dll.fini_blynclights()


    def turn_off_light(self, light_id):
        '''TurnOffLight

        light_id: device index

        Returns 0 for success, 1 for failure.

        This function releases the resources reserved for the devices
        up on calling the FindDevices function.
        '''
        try:
            return self._turn_off_light(light_id)
        except AttributeError:
            pass
        self._turn_off_light = self._fixup('TurnOffLight')
        return self._turn_off_light(light_id)


    def turn_on_green_light(self, light_id):
        '''TurnOnGreenLight

        light_id: device index

        Returns 0 for success, 1 for failure.

        This function lights the Blync device specified by
        byDeviceIndex in green color. This function call can be used
        for all types of devices.

        '''
        try:
            return self._turn_on_green_light(light_id)
        except AttributeError:
            pass
        self._turn_on_green_light = self._fixup('TurnOnGreenLight')
        return self._turn_on_green_light(light_id)


    def turn_on_red_light(self, light_id):
        '''TurnOnRedLight

        light_id: device index

        Returns 0 for success, 1 for failure.

        This function lights the Blync device specified by
        byDeviceIndex in red color. This function call can be used for
        all types of devices.
        '''
        try:
            return self._turn_on_red_light(light_id)
        except AttributeError:
            pass
        self._turn_on_red_light = self._fixup('TurnOnRedLight')
        return self._turn_on_red_light(light_id)


    def turn_on_magenta_light(self, light_id):
        '''TurnOnMagentaLight

        light_id: device index

        Returns 0 for success, 1 for failure.

        This function lights the Blync device specified by
        byDeviceIndex in magenta (purple) color. This function call
        can be used for all types of devices.
        '''
        try:
            return self._turn_on_magenta_light(light_id)
        except AttributeError:
            pass
        self._turn_on_magenta_light = self._fixup('TurnOnMagentaLight')
        return self._turn_on_magenta_light(light_id)


    def turn_on_yellow_light(self, light_id):
        '''TurnOnYellowLight

        light_id: device index

        Returns 0 for success, 1 for failure.
        
        This function lights the Blync device specified by
        byDeviceIndex in yellow color. This function call can be used
        for all types of devices.

        '''
        try:
            return self._turn_on_yellow_light(light_id)
        except AttributeError:
            pass
        self._turn_on_yellow_light = self._fixup('TurnOnYellowLight')
        return self._turn_on_yellow_light(light_id)    


    def turn_on_blue_light(self, light_id):
        '''TurnOnBlueLight

        light_id: device index

        Returns 0 for success, 1 for failure.

        This function lights the Blync device specified by
        byDeviceIndex in blue color. This function call can be used
        for all types of devices.
        '''
        try:
            return self._turn_on_blue_light(light_id)
        except AttributeError:
            pass
        self._turn_on_blue_light = self._fixup('TurnOnBlueLight')
        return self._turn_on_blue_light(light_id)


    def turn_on_cyan_light(self, light_id):
        '''TurnOnCyanLight

        light_id: device index

        Returns 0 for success, 1 for failure.

        This function lights the Blync device specified by
        byDeviceIndex in cyan color.  This function call can be used
        for all types of devices.
        '''
        try:
            return self._turn_on_cyan_light(light_id)
        except AttributeError:
            pass
        self._turn_on_cyan_light = self._fixup('TurnOnCyanLight')
        return self._turn_on_cyan_light(light_id)


    def turn_on_white_light(self, light_id):
        '''TurnOnWhiteLight

        light_id: device index

        Returns 0 for success, 1 for failure.

        This function lights the Blync device specified by
        byDeviceIndex in white color. This function call can be used
        for all types of devices.
        '''
        try:
            return self._turn_on_white_light(light_id)
        except AttributeError:
            pass
        self._turn_on_white_light = self._fixup('TurnOnWhiteLight')
        return self._turn_on_white_light(light_id)


    def turn_on_orange_light(self, light_id):
        '''TurnOnOrangeLight

        light_id: device index

        Returns 0 for success, 1 for failure.

        This function lights the Blync device specified by
        byDeviceIndex in orange color. This function call can be used
        only for the following types of devices namely Blynclight
        Standard, Blynclight Plus, Blynclight Mini, Blynclight
        Wireless, Lumena Headset devices an Embrava Embedded Devices
        '''
        try:
            return self._turn_on_orange_light(light_id)
        except AttributeError:
            pass
        self._turn_on_orange_light = self._fixup('TurnOnOrangeLight')
        return self._turn_on_orange_light(light_id)


    def turn_on_rgb_lights(self, light_id, red, green, blue):
        '''TurnOnRGBLights

        light_id: device index
             red: unsigned 8 bit quantity, 0 to 255
           green: unsigned 8 bit quantity, 0 to 255
            blue: unsigned 8 bit quantity, 0 to 255

        Returns 0 for success, 1 for failure.

        This function lights the Blync device specified by
        byDeviceIndex in the color which represents the combination of
        the red, green and blue color. The brightness levels of each
        color can be adjusted by the corresponding red, green, and
        blue level levels. This function call can be used only for the
        following types of devices namely BlyncUSB30 (Blynclight
        Standard), BlyncUSB30S (Blynclight Plus), Blynclight Mini,
        Blynclight Wireless, Lumena Headset (110 and 120) devices.
        '''
        try:
            return self._turn_on_rgb_lights(light_id, red, green, blue)
        except AttributeError:
            pass
        self._turn_on_rgb_lights = self._fixup('TurnOnRGBLights',
                                               proto=[ctypes.c_byte] * 4)
        return self._turn_on_rgb_lights(light_id, red, green, blue)


    def turn_on_v30_light(self, light_id):
        '''TurnOnV30Light

        light_id: device index

        Returns 0 for success, 1 for failure.
        '''
        try:
            return self._turn_on_v30_light(light_id)
        except AttributeError:
            pass
        self._turn_on_v30_light = self._fixup('TurnOnV30Light')
        return self._turn_on_v30_light(light_id)


    def turn_off_v30_light(self, light_id):
        '''TurnOffV30Light

        light_id: device index

        Returns 0 for success, 1 for failure.
        '''
        try:
            return self._turn_off_v30_light(light_id)
        except AttributeError:
            pass
        self._turn_off_v30_light = self._fixup('TurnOffV30Light')
        return self._turn_off_v30_light(light_id)


    def set_red_color(self, light_id, level):
        '''SetRedColorBrightnessLevel

        light_id: device index
           level: unsigned 8 bit quantity, 0 to 255

        Returns 0 for success, 1 for failure.

        '''
        try:
            return self._red_color(light_id, level)
        except AttributeError:
            pass
        self._red_color = self._fixup('SetRedColorBrightnessLevel',
                                      proto=[ctypes.c_byte]*2)
        return self._red_color(light_id, level)


    def set_green_color(self, light_id, level):
        '''SetGreenColorBrightnessLevel

        light_id: device index
           level: unsigned 8 bit quantity, 0 to 255

        Returns 0 for success, 1 for failure.
        '''
        try:
            return self._green_color(light_id, level)
        except AttributeError:
            pass
        self._green_color = self._fixup('SetGreenColorBrightnessLevel',
                                      proto=[ctypes.c_byte]*2)
        return self._green_color(light_id, level)    


    def set_blue_color(self, light_id, level):
        '''SetBlueColorBrightnessLevel

        light_id: device index
           level: unsigned 8 bit quantity, 0 to 255

        Returns 0 for success, 1 for failure.
        '''
        try:
            return self._blue_color(light_id, level)
        except AttributeError:
            pass
        self._blue_color = self._fixup('SetBlueColorBrightnessLevel',
                                      proto=[ctypes.c_byte]*2)
        return self._blue_color(light_id, level)


    def start_light_flash(self, light_id):
        '''StartLightFlash

        light_id: device index

        Returns 0 for success, 1 for failure.

        This function starts the light to blink at the specified
        blinking speed. This function call can be used only for the
        following types of devices namely BlyncUSB30 (Blynclight
        Standard), BlyncUSB30S (Blynclight Plus), Blynclight Mini,
        Blynclight Wireless, Lumena Headset (110 and 120) devices. The
        blinking speed would be specified by SelectLightFlashSpeed
        function call.
        '''
        
        try:
            return self._start_light_flash(light_id)
        except AttributeError:
            pass
        self._start_light_flash = self._fixup('StartLightFlash')

        return self._start_light_flash(light_id)


    def stop_light_flash(self, light_id):
        '''StopLightFlash

        light_id: device index

        Returns 0 for success, 1 for failure.

        This function stops blinking the light. This function call can
        be used only for the following types of devices namely
        BlyncUSB30 (Blynclight Standard), BlyncUSB30S (Blynclight
        Plus), Blynclight Mini, Blynclight Wireless, Lumena Headset
        (110 and 120) devices.
        '''
        try:
            return self._stop_light_flash(light_id)
        except AttributeError:
            pass
        self._stop_light_flash = self._fixup('StopLightFlash')
        return self._stop_light_flash(light_id)


    def select_light_flash_speed(self, light_id, speed):
        '''SelectLightFlashSpeed

        light_id: device index
           speed: 1=LOW, 2=MEDIUM, 3=HIGH

        Returns 0 for success, 1 for failure.

        This function selects the speed at which the light will
        blink. This function call can be used only for the following
        types of devices namely BlyncUSB30 (Blynclight Standard),
        BlyncUSB30S (Blynclight Plus), Blynclight Mini, Blynclight
        Wireless, Lumena Headset (110 and 120) devices.
        '''
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
        '''SetLightDim

        light_id: device index

        Returns 0 for success, 1 for failure.

        This function makes the current light brightness to dim by 50%
        of the full brightness. This function call can be used only
        for the following types of devices namely BlyncUSB30
        (Blynclight Standard), BlyncUSB30S (Blynclight Plus),
        Blynclight Mini, Blynclight Wireless, Lumena Headset (110 and
        120) devices.
        '''
        try:
            return self._set_light_dim(light_id)
        except AttributeError:
            pass
        self._set_light_dim = self._fixup('SetLightDim')
        return self._set_light_dim(light_id)


    def clr_light_dim(self, light_id):
        '''ClearLightDim

        light_id: device index

        Returns 0 for success, 1 for failure.

        This function resets the light dimness and bring the light
        brightness to full level. This function call can be used only
        for the following types of devices namely BlyncUSB30
        (Blynclight Standard), BlyncUSB30S (Blynclight Plus),
        Blynclight Mini, Blynclight Wireless, Lumena Headset (110 and
        120) devices.
        '''
        try:
            return self._clr_light_dim(light_id)
        except AttributeError:
            pass
        self._clr_light_dim = self._fixup('ClearLightDim')
        return self._clr_light_dim(light_id)


    def select_music_to_play(self, light_id, music_id):
        '''SelectMusicToPlay

        light_id: device index
        music_id: music index

        Returns 0 for success, 1 for failure.

        This function selects the music to be played on the Blync
        light. This function call can be used only for the following
        types of devices namely BlyncUSB30S (Blynclight Plus),
        Blynclight Mini, Blynclight Wireless devices. The BlynUSB30S
        can play 10 sounds, Blynclight Mini and Wireless devices can
        play 14 sounds.
        '''
        try:
            return self._select_music_to_play(light_id, music_id)
        except AttributeError:
            pass
        self._select_music_to_play = self._fixup('SelectMusicToPlay',
                                                 proto=[ctypes.c_byte]*2)
        return self._select_music_top_play(light_id, music_id)


    def start_music_play(self, light_id):
        '''StartMusicPlay

        light_id: device index

        Returns 0 for success, 1 for failure.        

        This function starts playing the selected music on the Blync
        light. This function call can be used only for the following
        types of devices namely BlyncUSB30S (Blynclight Plus),
        Blynclight Mini, Blynclight Wireless devices.
        '''
        
        try:
            return self._start_music_play(light_id)
        except AttributeError:
            pass
        self._start_music_play = self._fixup('StartMusicPlay')
        return self._start_music_play(light_id)


    def stop_music_play(self, light_id):
        '''StopMusicPlay

        light_id: device index

        Returns 0 for success, 1 for failure.        

        This function stops playing the music that is being played on
        the Blync light. This function call can be used only for the
        following types of devices namely BlyncUSB30S (Blynclight
        Plus), Blynclight Mini, Blynclight Wireless devices.
        '''
        try:
            return self._stop_music_play(light_id)
        except AttributeError:
            pass
        self._stop_music_play = self._fixup('StartMusicPlay')
        return self._stop_music_play(light_id)


    def set_music_repeat(self, light_id):
        '''SetMusicRepeat

        light_id: device index

        Returns 0 for success, 1 for failure.        

        This function enables the repeated playing of the music that
        is being played on the Blync light, till the repeat flag gets
        cleared. This function call can be used only for the following
        types of devices namely BlyncUSB30S (Blynclight Plus),
        Blynclight Mini, Blynclight Wireless devices.
        '''
        
        try:
            return self._set_music_repeat(light_id)
        except AttributeError:
            pass
        self._set_music_repeat = self._fixup('SetMusicRepeat')
        return self._set_music_repeat(light_id)


    def clr_music_repeat(self, light_id):
        '''ClearMusicRepeat

        light_id: device index

        Returns 0 for success, 1 for failure.        

        This function clears repeated playing of the music that is
        being played on the Blync light, so that any music to be
        played will be played once. This function call can be used
        only for the following types of devices namely BlyncUSB30S
        (Blynclight Plus), Blynclight Mini, Blynclight Wireless
        devices.
        '''
        try:
            return self._clr_music_repeat(light_id)
        except AttributeError:
            pass
        self._clr_music_repeat = self._fixup('ClearMusicRepeat')
        return self._clr_music_repeat(light_id)


    def set_volume_mute(self, light_id):
        '''SetVolumeMute

        light_id: device index

        Returns 0 for success, 1 for failure.        

        This function mutes the volume level of the music that is
        being played on the Blync light, so that if any music is being
        played it will not be audible. But this doesn’t stop playing
        the music. This function call can be used only for the
        following types of devices namely BlyncUSB30S (Blynclight
        Plus), Blynclight Mini, Blynclight Wireless devices.
        '''
        try:
            return self._set_volume_mute(light_id)
        except AttributeError:
            pass
        self._set_volume_mute = self._fixup('SetVolumeMute')
        return self._set_volume_mute(light_id)


    def clr_volume_mute(self, light_id):
        '''ClearVolumeMute

        light_id: device index

        Returns 0 for success, 1 for failure.        

        This function clears the volume mute on Blync light. So that
        if any music is being played it will be audible. This function
        call can be used only for the following types of devices
        namely BlyncUSB30S (Blynclight Plus), Blynclight Mini,
        Blynclight Wireless devices.
        '''
        
        try:
            return self._clr_volume_mute(light_id)
        except AttributeError:
            pass
        self._clr_volume_mute = self._fixup('SetVolumeMute')
        return self._clr_volume_mute(light_id)


    def set_music_volume(self, light_id, level):
        '''SetMusicVolume

        light_id: device index
           level: volume

        Returns 0 for success, 1 for failure.        

        This function sets the volume level of the music that is being
        played on the Blync light. This function call can be used only
        for the following types of devices namely BlyncUSB30S
        (Blynclight Plus), Blynclight Mini, Blynclight Wireless
        devices.
        '''
        try:
            return self._set_music_volume(light_id, level)
        except AttributeError:
            pass
        self._set_music_volume = self._fixup('SetVolumeMute',
                                             proto=[ctypes.c_byte]*2)
        return self._set_music_volume(light_id, level)


    def get_device_unique_id(self, light_id):
        '''GetDeviceUniqueId

        light_id: device index

        Returns device unique identifier.

        This function gets the devices unique serial number which is
        the hard coded value with the device as device unique id. The
        devices supporting this unique id feature are version 40 of
        Blynclight Plus, Standard, Mini, Wireless and Embrava Embedded
        devices.
        '''
        # sdk/patch.h  int unique_device_id(unsigned char *devIndex)
        return self._dll.unique_device_id(light_id)

    
class BlyncLight(object):
    '''
    '''
    
    def __init__(self, device_id, color, blc=None):
        '''
        '''
        if not isinstance(blc, BlyncLightControl):
            raise ValueError('missing BlyncLightControl object')
        self.blc = blc
        self.device_id = device_id
        self.reset()
        self.color = color

    def reset(self):
        '''Resets the state of the BlyncLight.

        1. Turns light off.
        2. Disables flashing
        3. Flash speed to low
        4. Stops music playback (for models that support music)
        5. Sets music selection to 0
        6. Sets music volume to 0
        7. Disables music volume mute.
        '''
        
        self.on = False
        self.flashing = False
        self.flash_speed = FlashSpeed.LOW
        self.play = False
        self.music_selection = 0
        self.volume = 0
        self.mute = False

    def __repr__(self):
        '''
        '''
        return f'{self.__class__.__name__}(id={self.device_id})'

    def __str__(self):
        '''
        '''
        return '\n'.join(f'{k}: {v}' for k,v in self.status.items())

    def __del__(self):
        '''Resets the light before releasing it.
        '''
        self.reset()

    @property
    def status(self):
        '''
        '''
        return {
            'device_id': self.device_id,
            'on': self.on,
            'color': self.color,
            'dim': self.dim,
            'flash': self.flash,
            'flash_speed': self.flash_speed.value,
        }

    @property
    def on(self):
        '''Boolean indicating if the light is on or off.

        Assign True to turn light on, False to turn light off.
        '''
        try:
            return self._on
        except AttributeError:
            pass
        self.blc.turn_off_light(self.device_id)
        self._on = False
        return self._on

    @on.setter
    def on(self, newValue):
        if bool(newValue):
            r,g,b = self.color
            v = self.blc.turn_on_rgb_lights(self.device_id, r, g, b)
            self._on = bool(v == 0)
        else:
            v = self.blc.turn_off_light(self.device_id)
            self._on = not bool(v == 0)

    @property
    def red(self):
        '''Red light color, integer between 0 and 255.
        '''
        return self.color[0]

    @red.setter
    def red(self, newRed):
        r,g,b = self.color
        self.color = (newRed, g, b)

    @property
    def green(self):
        '''Green light color, integer between 0 and 255.
        '''
        return self.color[1]
        
    @green.setter
    def green(self, newGreen):
        r,g,b = self.color
        self.color = (r, newGreen, b)

    @property
    def blue(self):
        '''Blue light color, integer between 0 and 255.
        '''
        return self.color[2]

    @blue.setter
    def blue(self, newBlue):
        r,g,b = self.color
        self.color = (r, g, newBlue)
        
    @property
    def color(self):
        '''3-tuple of red, green and blue color values.
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
        if self._on:
            self.on = True

    @property
    def dim(self):
        '''Boolean indicating if the light is in dim mode.

        Assign True to activate dim mode, False to deactivate.
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
        return self._dim

    @property
    def flash(self):
        '''Boolean indicating if the light is in flash mode.

        Assign True to active flash mode, False to deactivate.
        '''
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
        '''The light's flash speed. Valid setttings are:

        FlashSpeed.LOW
        FlashSpeed.MEDIUM
        FlashSpeed.HIGH
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
