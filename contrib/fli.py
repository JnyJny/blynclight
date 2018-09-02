#!/usr/bin/env python3

'''Flash Lights Impressively
'''

from blynclight import BlyncLight
from itertools import cycle

if __name__ == '__main__':

    try:
        light = BlyncLight.first_light()
    except IOError as e:
        print(e)
        exit(-1)

    colors = [(255, 0, 0), (0, 0, 255)]

    try:
        light.on = True
        for color in cycle(colors):
            light.color = color
    except KeyboardInterrupt:
        pass
    light.on = False
