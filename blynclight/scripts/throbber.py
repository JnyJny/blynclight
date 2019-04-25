#!/usr/bin/env python3

"""BlyncLight intensifies.
"""

import click
from blynclight import BlyncLight, BlyncLightNotFound
from time import sleep
from itertools import cycle


def Gradient(start, stop, step, red=True, green=False, blue=False):
    """
    """
    colors = []
    for i in range(start, stop, step):
        colors.append((i if red else 0, i if blue else 0, i if green else 0))
    return colors


@click.command()
@click.option("-l", "--light-id", type=int, default=0)
@click.option("-r", "--red", is_flag=True, default=False)
@click.option("-g", "--green", is_flag=True, default=False)
@click.option("-b", "--blue", is_flag=True, default=False)
@click.option("-w", "--white", is_flag=True, default=False)
@click.option("-f", "--fast", default=0)
@click.option("-d", "--dim", is_flag=True, default=False)
def cli(light_id, red, green, blue, white, fast, dim):
    """BlyncLight intensifies.
    """

    if white:
        red = True
        green = True
        blue = True

    if not any([red, green, blue]):
        red = True

    step = 8 * (min(fast, 24) + 1)

    colors = Gradient(0, 255, step, red, green, blue)

    colors.extend(c for c in reversed(colors))

    try:
        b = BlyncLight.get_light(light_id)
    except BlyncLightNotFound as not_found:
        print(not_found)
        exit(-1)

    b.on = False
    b.color = (0, 0, 0)
    b.dim = dim

    try:
        b.on = True
        while True:
            for color in cycle(colors):
                b.color = color
                sleep(0.05)
    except KeyboardInterrupt:
        pass
