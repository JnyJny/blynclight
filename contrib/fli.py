#!/usr/bin/env python3

'''Flash Lights Impressively
'''

from blynclight import BlyncLight
from itertools import cycle
from collections import deque
from time import sleep

if __name__ == '__main__':

    lights = deque(BlyncLight.available_lights())

    colors = [(255, 0, 0), (0, 255, 0),
              (0, 255, 0), (0, 0, 255),
              (0, 0, 255), (255, 0 ,0)]

    for light in lights:
        light.on = True

    try:
        for color in cycle(colors):
            lights.rotate(1)
            lights[0].color = color
            sleep(0.01)
    except KeyboardInterrupt:
        pass

    for light in lights:
        light.on = False

