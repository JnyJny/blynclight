#!/usr/bin/env python3

"""BlyncLights Love Rainbows!
"""

import click
import math
from blynclight import BlyncLight, BlyncLightNotFound
from time import sleep
from itertools import cycle


def Spectrum(steps=64, frequency=None, phase=None, center=128, width=127):
    """generator function that returns 'steps' rbg tuples.

        steps: optional integer, default=64
    frequency: optional 3-tuple for rbg frequency, default=(.3,.3,.3)
        phase: optional 3-tuple for rbg phase, default=(0,2,4)
       center: optional integer, default=128
        width: optional integer, default=127

    Returns (r, b, g) where each member is a value between 0 and 255.
    """

    frequency = frequency or (0.3, 0.3, 0.3)
    phase = phase or (0, 2, 4)

    for i in range(steps):
        r = int((math.sin(frequency[0] * i + phase[0]) * width) + center)
        b = int((math.sin(frequency[2] * i + phase[2]) * width) + center)
        g = int((math.sin(frequency[1] * i + phase[1]) * width) + center)
        yield (r, b, g)


@click.command()
@click.option("-l", "--light-id", default=0)
@click.option("-s", "--speed", default=1)
def cli(light_id, speed):
    """BlyncLights Love Rainbows!

    """

    colors = [rgb for rgb in Spectrum(steps=255)]

    try:
        b = BlyncLight.get_light(light_id)
    except BlyncLightNotFound as error:
        print(f"{error}")
        exit(-1)

    interval = speed * 0.1

    b.on = True
    try:
        for color in cycle(colors):
            b.color = color
            sleep(interval)
    except KeyboardInterrupt:
        pass
