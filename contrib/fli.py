#!/usr/bin/env python3

'''Flash Lights Impressively
'''

from blynclight import BlyncLight_API
from itertools import cycle

if __name__ == '__main__':

    light = BlyncLight_API.first_light()

    colors = [ (255,0,0), (0,0,255) ]

    try:
        light.on = True
        for color in cycle(colors):
            light.color = color
            
    except KeyboardInterrupt:
        pass
    light.on = False
