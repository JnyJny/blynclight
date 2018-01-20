#!/usr/bin/env python3

import hug
from blynclight import *

lights = [BlyncLightControl.getLight(i) for i,t in BlyncLightControl.available_lights()]

#  /blynclight/status
#  /blynclight/devid/[on|dim|flash|mute]
#  /blynclight/devid/status
#  /blynclight/devid/color/0xRRGGBB
#  /blynclight/devid/red/0xRR
#  /blynclight/devid/green/0xGG
#  /blynclight/devid/blue/0xBB
#  /blynclight/devid/flash
#  /blynclight/devid/flash/speed/{value}

@hug.get('/blynclight/status')
def status():
    return [l.status for l in lights]

@hug.get('/blynclight/{light_id}/on')
def turn_on_light(light_id : hug.types.number):
    lights[light_id].on = True
    return lights[light_id].status

@hug.get('/blynclight/{light_id}/off')
def turn_off_light(light_id : hug.types.number):
    lights[light_id].on = False
    return lights[light_id].status

@hug.get('/blynclight/{light_id}/dim')
def toggle_dim(light_id : hug.types.number):
    lights[light_id].dim = not lights[light_id].dim
    return lights[light_id].status

@hug.get('/blynclight/{light_id}/flash')
def toggle_flash(light_id : hug.types.number):
    lights[light_id].flash = not lights[light_id].flash
    return lights[light_id].status

@hug.get('/blynclight/{light_id}/mute')
def toggle_mute(light_id : hug.types.number):
    lights[light_id].mute = not lights[light_id].mute
    return lights[light_id].status

@hug.get('/blynclight/{light_id}/flash/speed/{value}')
def set_flash_speed(light_id : hug.types.number, value: hug.types.number):
    lights[light_id].flash_speed = value
    return lights[light_id].status

@hug.get('/blynclight/{light_id}/color/{hex_rgb_value}')
def set_color(light_id : hug.types.number, hex_rgb_value: hug.types.text):
    lights[light_id].color = HexToRGB(hex_rgb_value)
    return lights[light_id].status

@hug.get('/blynclight/{light_id}/red/{hex_rgb_value}')
def set_red(light_id : hug.types.number, hex_rgb_value: hug.types.text):
    lights[light_id].red = max(min(int(hex_rgb_value, 16), 255), 0)
    return lights[light_id].status

@hug.get('/blynclight/{light_id}/green/{hex_rgb_value}')
def set_green(light_id : hug.types.number, hex_rgb_value: hug.types.text):
    lights[light_id].green = max(min(int(hex_rgb_value, 16), 255), 0)
    return lights[light_id].status

@hug.get('/blynclight/{light_id}/blue/{hex_rgb_value}')
def set_blue(light_id : hug.types.number, hex_rgb_value: hug.types.text):
    lights[light_id].blue = max(min(int(hex_rgb_value, 16), 255), 0)
    return lights[light_id].status










