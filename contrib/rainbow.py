#!/usr/bin/env python3

'''BlyncLights Love Rainbows!
'''

import math
from blynclight import BlyncLight
from time import sleep
from argparse import ArgumentParser
from itertools import cycle


def Spectrum(steps=64, frequency=None, phase=None, center=128, width=127):
    '''generator function that returns 'steps' rbg tuples.

        steps: optional integer, default=64
    frequency: optional 3-tuple for rbg frequency, default=(.3,.3,.3)
        phase: optional 3-tuple for rbg phase, default=(0,2,4)
       center: optional integer, default=128
        width: optional integer, default=127

    Returns (r, b, g) where each member is a value between 0 and 255.
    '''

    frequency = frequency or (.3, .3, .3)
    phase = phase or (0, 2, 4)

    for i in range(steps):
        r = int((math.sin(frequency[0] * i + phase[0]) * width) + center)
        b = int((math.sin(frequency[2] * i + phase[2]) * width) + center)
        g = int((math.sin(frequency[1] * i + phase[1]) * width) + center)
        yield (r, b, g)


if __name__ == '__main__':
    '''
    '''

    parser = ArgumentParser()

    parser.add_argument('-l', '--light-id',
                        type=int,
                        default=0)

    parser.add_argument('-s', '--speed',
                        action='count',
                        default=1)

    args = parser.parse_args()

    colors = [rgb for rgb in Spectrum(steps=255)]

    try:
        b = BlyncLight.available_lights()[args.light_id]
    except IndexError:
        print(f'light {args.light_id} unavailable')
        exit(-1)

    interval = (args.speed * .1)

    b.on = True
    try:
        for color in cycle(colors):
            b.color = color
            sleep(interval)
    except KeyboardInterrupt:
        pass
    b.on = False
