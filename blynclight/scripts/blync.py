#!/usr/bin/env python3

from blynclight import BlyncLight
import click
from time import sleep
from pprint import pprint


@click.command()
@click.option("-l", "--light-id", default=0, help="Integer light identifer")
@click.option("-r", "--red", default=0, help="Integer 0-255")
@click.option("-b", "--blue", default=0, help="Integer 0-255")
@click.option("-g", "--green", default=0, help="Integer 0-255")
@click.option("--off/--on", default=True)
@click.option("--bright/--dim", default=False)
@click.option("--flash/--no-flash", default=False)
@click.option("-s", "--speed", default=0, help="0, 1, 2, 4")
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Prints the light status."
)
@click.option("-d", "--duration", default=-1)
@click.option(
    "-a", "--available", is_flag=True, default=False, help="Show available lights."
)
def cli(
    light_id, red, blue, green, off, bright, flash, speed, verbose, duration, available
):
    """Initialize the state of a connected BlyncLight and
    activate the light for 'duration' seconds.
    """

    if available:
        for light_id, info in enumerate(BlyncLight.available_lights()):
            # XXX better print of available light info
            print("Light Identifier:", light_id)
            pprint(info)
        return

    light = BlyncLight.get_light(light_id)

    with light.updates_paused():
        light.red = red
        light.blue = blue
        light.green = green
        light.off = off
        light.dim = bright
        light.flash = flash
        light.speed = speed

    if verbose:
        print(light)

    while duration != 0:
        duration -= 1
        sleep(1)


if __name__ == "__main__":
    cli()
