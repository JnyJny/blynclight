#!/usr/bin/env python3

from blynclight import BlyncLight
from apistar import App, Route, http

PORT=21169

def hex_string_to_rbg(hexString):
    '''
    '''
    h = int(hexString, 16)
    return [((h & (0xff << i)) >> i) for i in range(16, -1, -8)]

def rbg_to_hex_string(rbg):
    '''
    '''
    return f'{sum((rbg[i] << v) for i,v in enumerate(range(16, -1, -8))):06x}'


class BlyncLightController:

    def __init__(self, port=21169):
        self.port = port

#        for light in self.lights:
#            light.update_device()

    @property
    def lights(self):
        try:
            return self._lights
        except AttributeError:
            pass
        self._lights = BlyncLight.available_lights()
        return self._lights

    def _rescan_lights(self):
        del(self._lights)
        self.lights
    
    def light(self, index):
        return self.lights[index]

    def nlights(self) -> str:
        return f'Available blynclights: {len(self.lights)}'

    def status(self, light_id: int) -> dict:
        return self.light(light_id).status

    def toggle_on(self, light_id: int) -> dict:
        light = self.light(light_id)
        prev = light.on
        light.on = 0 if light.on else 1
        return light.status

    def on(self, light_id: int) -> dict:
        light = self.light(light_id)
        light.off = 0
        return light.status

    def off(self, light_id: int) -> dict:
        light = self.light(light_id)
        light.off = 1
        return light.status

    def color(self, light_id: int, hexcolor: str) -> dict:
        light = self.light(light_id)
        light.color = int(hexcolor, 16)
        return light.status

    def red(self, light_id: int, hexred: str) -> dict:
        light = self.light(light_id)
        light.red = int(hexred, 16)
        return light.status

    def blue(self, light_id: int, hexblue: str) -> dict:
        light = self.light(light_id)
        light.blue = int(hexblue, 16)
        return light.status

    def green(self, light_id: int, hexgreen: str) -> dict:
        light = self.light(light_id)
        light.green = int(hexgreen, 16)
        return light.status

    def flash_toggle(self, light_id: int) -> dict:
        light = self.light(light_id)
        light.flash = ~light.flash
        return light.status

    def flash_on(self, light_id: int) -> dict:
        light = self.light(light_id)
        light.flash = 1
        return light.status

    def flash_off(self, light_id: int) -> dict:
        light = self.light(light_id)
        light.flash = 0
        return light.status

    def flash_speed(self, light_id: int, speed: int) -> dict:
        light = self.light(light_id)
        light.speed = speed
        return light.status

    def mute_toggle(self, light_id: int) -> dict:
        light = self.light(light_id)
        light.mute = ~light.mute
        return light.status

    def mute_on(self, light_id: int) -> dict:
        light = self.light(light_id)
        light.mute = 1
        return light.status

    def mute_off(self, light_id: int) -> dict:
        light = self.light(light_id)
        light.mute = 0
        return light.status    

    def music(self, light_id: int, music: str) -> dict:
        light = self.light(light_id)
        light.music = int(music)
        return light.status

    def play_toggle(self, light_id: int) -> dict:
        light = self.light(light_id)
        light.play = ~light.play
        return light.status

    def play_on(self, light_id: int) -> dict:
        light = self.light(light_id)
        light.play = 1
        return light.status

    def play_off(self, light_id: int) -> dict:
        light = self.light(light_id)
        light.play = 0
        return light.status

    def repeat_toggle(self, light_id: int) -> dict:
        light = self.light(light_id)
        light.repeat = ~light.repeat
        return light.status

    def repeat_on(self, light_id: int) -> dict:
        light = self.light(light_id)
        light.repeat = 1
        return light.status

    def repeat_off(self, light_id: int) -> dict:
        light = self.light(light_id)
        light.repeat = 0
        return light.status


    def volume(self, light_id: int, volume; int) -> dict:
        light = self.light(light_id)
        light.volume = volume
        return light.status

controller = BlyncLightController(port=PORT)

routes = [
    Route('/blynclight/count', method='GET',
          handler=controller.nlights),
    
    Route('/blynclight/{light_id}/status', method='GET',
          handler=controller.status),
    
    Route('/blynclight/{light_id}/on/toggle', method='GET',
          handler=controller.toggle_on),
    
    Route('/blynclight/{light_id}/on', method='GET',
          handler=controller.on),
    
    Route('/blynclight/{light_id}/off', method='GET',
          handler=controller.off),
    
    Route('/blynclight/{light_id}/color/{hexcolor}', method='GET',
          handler=controller.color),
    
    Route('/blynclight/{light_id}/red/{hexred}', method='GET',
          handler=controller.red),
    
    Route('/blynclight/{light_id}/blue/{hexblue}', method='GET',
          handler=controller.blue),
    
    Route('/blynclight/{light_id}/green/{hexgreen}', method='GET',
          handler=controller.green),

    Route('/blynclight/{light_id}/flash/toggle', method='GET',
          handler=controller.flash_toggle),
    
    Route('/blynclight/{light_id}/flash/on', method='GET',
          handler=controller.flash_on),

    Route('/blynclight/{light_id}/flash/off', method='GET',
          handler=controller.flash_off),

    Route('/blynclight/{light_id}/flash/speed/{speed}', method='GET',
          handler=controller.flash_speed),    

    
]


blyncd = App(routes=routes, template_dir='.')

if __name__ == '__main__':
    
    blyncd.serve('127.0.0.1', PORT, debug=True)


