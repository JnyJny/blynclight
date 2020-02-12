"""
"""

from blynclight import BlyncLight, BlyncLightNotFound
from itertools import cycle
from collections import deque

from pprint import pprint
from time import sleep
from typer import Typer, Option, Exit


from .effects import Gradient, Spectrum
from .cli_options import light_id_option
from .cli_options import red_option
from .cli_options import green_option
from .cli_options import blue_option
from .cli_options import dim_option
from .cli_options import list_available_option
from .cli_options import version_option
from .cli_options import verbose_option

# from .options import


blync_cli = Typer()
fli_cli = Typer()
throbber_cli = Typer()
rainbow_cli = Typer()


@blync_cli.command()
def blync_cmd(
    light_id: int = light_id_option,
    red: int = red_option,
    blue: int = blue_option,
    green: int = green_option,
    off: bool = Option(True, "--off/-on", "-o/-n", help="Activate the light."),
    dim: bool = dim_option,
    flash: bool = Option(False, "--flash", "-f", help="Toggle flash mode."),
    speed: int = Option(0, "--speed", "-s", help="Flash speed range: 0 - 4"),
    verbose: bool = verbose_option,
    duration: int = Option(-1, "--duration", "-D", help="Time in seconds."),
    available: bool = list_available_option,
    version: bool = version_option,
):
    """Initialize the state of a connected BlyncLight and activate the
    light for 'duration' seconds. If duration is not specified,
    activation continues until an interrupt from the user is received.

    """

    try:
        light = BlyncLight.get_light(light_id)
    except BlyncLightNotFound as not_found:
        print(not_found)
        raise Exit()

    with light.updates_paused():
        light.red = red
        light.blue = blue
        light.green = green
        light.off = off
        light.dim = dim
        light.flash = flash
        light.speed = speed

    if verbose:
        print(light)

    while duration != 0:
        duration -= 1
        sleep(1)


@fli_cli.command()
def fli_cmd(
    light_id: int = light_id_option,
    interval: float = Option(0.1, "--interval", "-n", help="Seconds between flashes."),
    count: int = Option(-1, "--count", "-c", help="Number of times to flash."),
    intensity: int = Option(255, "--intensity", "-I", help="Integer range: 0 - 255"),
    available: bool = list_available_option,
    version: bool = version_option,
):
    """FLI - Flash Light Impressively

    Cycles the light identified by `light_id` thru red, green and blue
    with the given intensity `count` times, pausing for `interval`
    seconds.

    Giving a count of -1 (the default) flashes the light until the user
    supplies an interrupt.
    """

    try:
        light = BlyncLight.get_light(light_id)
    except BlyncLightNotFound as not_found:
        print(not_found)
        raise Exit()

    color = deque([(0x0FF & intensity) >> 0, 0, 0])

    with light.updates_paused():
        light.on = 1
        light.color = list(color)

    try:
        while count != 0:
            count -= 1
            color.rotate(1)
            light.color = list(color)
            sleep(interval)
    except KeyboardInterrupt:
        pass


@throbber_cli.command()
def throbber_cmd(
    light_id: int = light_id_option,
    red: bool = Option(False, "--red", "-r", help="Toggle red channel on."),
    green: bool = Option(False, "--green", "-g", help="Toggle green channel on."),
    blue: bool = Option(False, "--blue", "-b", help="Toggle blue channel on."),
    white: bool = Option(False, "--white", "-w", help="Toggle all channels on."),
    fast: int = Option(0, "--fast", "-f", help="Integer range: 0 - 24"),
    dim: bool = Option(False, "--dim", "-d", help="Enable dim mode."),
    available: bool = list_available_option,
    version: bool = version_option,
):
    """BlyncLight intensifies.
    """

    try:
        light = BlyncLight.get_light(light_id)
    except BlyncLightNotFound as not_found:
        print(not_found)
        raise Exit()

    if white:
        red = True
        green = True
        blue = True

    if not any([red, green, blue]):
        red = True

    step = 8 * (min(max(0, fast), 24) + 1)

    colors = Gradient(0, 255, step, red, green, blue)

    colors.extend(c for c in reversed(colors))

    with light.updates_paused():
        light.on = True
        light.color = (0, 0, 0)
        light.dim = dim

    try:
        light.on = True
        while True:
            for color in cycle(colors):
                light.color = color
                sleep(0.05)
    except KeyboardInterrupt:
        pass


@rainbow_cli.command()
def rainbow_cmd(
    light_id: int = light_id_option,
    speed: int = Option(
        1, "--speed", "-s", help="Decrease color cycle interval by 0.1 seconds."
    ),
    available: bool = list_available_option,
    version: bool = version_option,
):
    """BlyncLights Love Rainbows!

    """

    try:
        light = BlyncLight.get_light(light_id)
    except BlyncLightNotFound as not_found:
        print(not_found)
        raise Exit()

    colors = [rgb for rgb in Spectrum(steps=255)]

    interval = speed * 0.1

    with light.updates_paused():
        light.on = True
        light.color = (0, 0, 0)

    try:
        for color in cycle(colors):
            light.color = color
            sleep(interval)
    except KeyboardInterrupt:
        pass
