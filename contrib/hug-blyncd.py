#!/usr/bin/env python3

import hug
from blynclight import BlyncLight_API


def HexToRGB(hexValue):
    '''
    '''
    if isinstance(hexValue, str):
        hexStr = hexValue[2:]
    else:
        hexStr = hex(hexValue)[2:]

    if len(hexStr) == 6:
        return tuple(int(hexStr[i:i + 2], 16)
                     for i in range(0, len(hexStr), 2))

    raise ValueError(f'hex value out of bounds {hexValue}')


def RGBToHex(rgb):
    '''
    '''
    return f'0x{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'


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
        self._lights = BlyncLight_API.available_lights()
        return self._lights

    @hug.object.get('/blynclight/status')
    def status(self):
        '''Returns a list of BlyncLight.status dictionaries.'''
        return [l.status for l in self.lights]

    @hug.object.get('/blynclight/{light_id}/status')
    def light_status(self, light_id: hug.types.number):
        '''Returns a status dictionary for the BlyncLight identified by
        'light_id'.'''
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/on')
    def turn_on_light(self, light_id: hug.types.number):
        '''Turns the BlyncLight with 'light_id' on.'''
        self.lights[light_id].on = True
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/off')
    def turn_off_light(self, light_id: hug.types.number):
        '''Turns the BlyncLight with 'light_id' off.'''
        self.lights[light_id].on = False
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/dim')
    def toggle_dim(self, light_id: hug.types.number):
        '''Toggles the dim mode of the BlyncLight identified by 'light_id'.'''
        self.lights[light_id].dim = not self.lights[light_id].dim
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/flash')
    def toggle_flash(self, light_id: hug.types.number):
        '''Toggles the flash mode of the BlyncLight identified by
        'light_id'.'''
        self.lights[light_id].flash = not self.lights[light_id].flash
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/mute')
    def toggle_mute(self, light_id: hug.types.number):
        '''Toggles the mute mode of the BlyncLight identified by
        'light_id'.'''
        self.lights[light_id].mute = not self.lights[light_id].mute
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/flash/speed/{value}')
    def set_flash_speed(self,
                        light_id: hug.types.number,
                        value: hug.types.number):
        '''Sets the flash speed of the BlyncLight identified by 'light_id'.
        Valid speeds are: (1,low), (2, medium), (3, fast).'''
        self.lights[light_id].flash_speed = value
        return self.lights[light_id].status

    @hug.object.get('/blynclight/{light_id}/color/{hex_rgb_value}')
    def set_color(self,
                  light_id: hug.types.number,
                  hex_rgb_value: hug.types.text):
        '''Sets the color of the BlyncLight identifed by 'light_id'.
        Valid color specifiers are hex RGB strings with the format: 0xRRGGBB'''
        self.lights[light_id].color = HexToRGB(hex_rgb_value)
        return self.lights[light_id].status
