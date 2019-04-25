#!/usr/bin/env python3

"""Flash Lights Impressively
"""

from blynclight import BlyncLight, BlyncLightNotFound
from itertools import cycle
from collections import deque
from time import sleep
import click


def rotatable_color(intensity: str):
    """
    :param intensity: string hexadecimal number
    :return: collections.deque of integers
    """
    I = (0xFF & int(intensity, 16)) >> 0
    return deque([I, 0, 0])


@click.command()
@click.option("-l", "--light-id", default=0, help="Integer light identfier.")
@click.option(
    "-i", "--interval", default=0.1, help="Float interval in seconds to flash."
)
@click.option("-c", "--count", default=-1, help="Integer count to flash impressively.")
@click.option("-I", "--intensity", default="0xff", help="8-bit color intensity.")
@click.option(
    "-a", "--available", is_flag=True, help="List available BlyncLights and exit."
)
def cli(light_id, interval, count, intensity, available):
    """FLI - Flash Light Impressively

    Cycles the light identified by light_id thru red, green and blue
    with the given intensity count times, pausing for interval
    seconds. It can be stupid annoying. Apologize to your cow-orkers
    for me (not a typo).

    """

    if available:
        BlyncLight.report_available()
        return

    try:
        light = BlyncLight.get_light(light_id)
    except BlyncLightNotFound as not_found:
        print(not_found)
        return

    light.on = 1

    color = rotatable_color(intensity)

    try:
        while count != 0:
            count -= 1
            color.rotate(1)
            light.color = list(color)
            sleep(interval)
    except KeyboardInterrupt:
        pass
