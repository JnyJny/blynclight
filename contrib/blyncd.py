#!/usr/bin/env python3

import hug
from blynclight import BlyncLight
from blynclight import HexToRGB

@hug.object.urls('/')
class BlyncDaemon(object):

    def __init__(self):
        pass

    @property
    def lights(self):
        try:
            return self._lights
        except AttributeError:
            pass
        self._lights = [BlyncLight(i) for i in BlyncLight.available()]
        return self._lights

    @hug.object.get('/blynclight/status')
    def status(self):
        '''Returns a list of BlyncLight.status dictionaries.'''
        return [l.status for l in self.lights]    

    @hug.object.get('/blynclight/{light_id}/status')
    def light_status(self, light_id : hug.types.number):
        '''Returns a status dictionary for the BlyncLight identified by 'light_id'.'''
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/on')
    def turn_on_light(self, light_id : hug.types.number):
        '''Turns the BlyncLight with 'light_id' on.'''
        self.lights[light_id].on = True
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/off')
    def turn_off_light(self, light_id : hug.types.number):
        '''Turns the BlyncLight with 'light_id' off.'''
        self.lights[light_id].on = False
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/dim')
    def toggle_dim(self, light_id : hug.types.number):
        '''Toggles the dim mode of the BlyncLight identified by 'light_id'.'''
        self.lights[light_id].dim = not self.lights[light_id].dim
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/flash')
    def toggle_flash(self, light_id : hug.types.number):
        '''Toggles the flash mode of the BlyncLight identified by 'light_id'.'''
        self.lights[light_id].flash = not self.lights[light_id].flash
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/mute')
    def toggle_mute(self, light_id : hug.types.number):
        '''Toggles the mute mode of the BlyncLight identified by 'light_id'.'''
        self.lights[light_id].mute = not self.lights[light_id].mute
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/flash/speed/{value}')
    def set_flash_speed(self, light_id : hug.types.number, value: hug.types.number):
        '''Sets the flash speed of the BlyncLight identified by 'light_id'.
        Valid speeds are: (1,low), (2, medium), (3, fast).'''
        self.lights[light_id].flash_speed = value
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/color/{hex_rgb_value}')
    def set_color(self, light_id : hug.types.number, hex_rgb_value: hug.types.text):
        '''Sets the color of the BlyncLight identifed by 'light_id'.
        Valid color specifiers are hex RGB strings with the format: 0xRRGGBB'''
        self.lights[light_id].color = HexToRGB(hex_rgb_value)
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/red/{hex_rgb_value}')
    def set_red(self, light_id : hug.types.number, hex_rgb_value: hug.types.text):
        '''Sets the red color of the BlyncLight identified by 'light_id'.
        The green and blue colors are not modified. Expected color values
        are integers in the range [0, 255].'''
        self.lights[light_id].red = max(min(int(hex_rgb_value, 16), 255), 0)
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/green/{hex_rgb_value}')
    def set_green(self, light_id : hug.types.number, hex_rgb_value: hug.types.text):
        '''Sets the green color of the BlyncLight identified by 'light_id'.
        The red and blue colors are not modified. Expected color values
        are integers in the range [0, 255].'''
        self.lights[light_id].green = max(min(int(hex_rgb_value, 16), 255), 0)
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/blue/{hex_rgb_value}')
    def set_blue(self, light_id : hug.types.number, hex_rgb_value: hug.types.text):
        '''Sets the blue color of the BlyncLight identified by 'light_id'.
        The red and green colors are not modified. Expected color values
        are integers in the range [0, 255].'''
        self.lights[light_id].blue = max(min(int(hex_rgb_value, 16), 255), 0)
        return self.lights[light_id].status









