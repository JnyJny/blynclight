"""BlyncLight CLI Utilities
"""

import typer


from blynclight import BlyncLight, BlyncLightNotFound
from collections import deque
from itertools import cycle

from pprint import pprint
from sys import stdout
from time import sleep

from .effects import Gradient, Spectrum
from .__version__ import __version__


cli = typer.Typer()


def list_lights(value: bool) -> None:
    if value:
        BlyncLight.report_available()
        raise typer.Exit()


def report_version(value: bool) -> None:
    if value:
        print(f"version: {__version__}")
        raise typer.Exit()


@cli.callback(invoke_without_command=True)
def blync_callback(
    ctx: typer.Context,
    light_id: int = typer.Option(
        0, "--light-id", "-i", help="Light identifier", show_default=True
    ),
    red: int = typer.Option(
        0,
        "--red",
        "-r",
        is_flag=True,
        help="Integer range: 0 - 255",
        show_default=True,
    ),
    blue: int = typer.Option(
        0,
        "--blue",
        "-b",
        is_flag=True,
        help="Integer range: 0 - 255",
        show_default=True,
    ),
    green: int = typer.Option(
        0,
        "--green",
        "-g",
        is_flag=True,
        help="Integer range: 0 - 255",
        show_default=True,
    ),
    red_b: bool = typer.Option(
        False, "--RED", "-R", is_flag=True, help="Full value red [255]"
    ),
    blue_b: bool = typer.Option(
        False, "--BLUE", "-B", is_flag=True, help="Full value blue [255]"
    ),
    green_b: bool = typer.Option(
        False, "--GREEN", "-G", is_flag=True, help="Full value green [255]"
    ),
    off: bool = typer.Option(
        False, "--off/--on", "-o/-n", help="Activate the light.", show_default=True
    ),
    dim: bool = typer.Option(
        False,
        "--dim",
        "-d",
        is_flag=True,
        help="Toggle bright mode.",
        show_default=True,
    ),
    flash: int = typer.Option(0, "--flash", "-f", count=True,),
    available: bool = typer.Option(
        False,
        "--list-available",
        "-l",
        is_flag=True,
        is_eager=True,
        callback=list_lights,
    ),
    version: bool = typer.Option(
        False, "--version", "-V", is_flag=True, is_eager=True, callback=report_version
    ),
):
    """Control your Embrava BlyncLight from the command-line!

    """

    try:
        light = BlyncLight.get_light(light_id)
    except BlyncLightNotFound as not_found:
        typer.secho(str(not_found), fg="red")
        raise typer.Exit()

    light.immediate = 0
    light.red = red if not red_b else 255
    light.blue = blue if not blue_b else 255
    light.green = green if not green_b else 255
    light.off = off
    light.dim = dim
    light.flash = flash > 0
    light.speed = 1 << flash - 1 if flash else 0

    if not ctx.invoked_subcommand:
        if light.on and light.color == (0, 0, 0):
            light.green = 255
        light.immediate = 1
        typer.Exit()

    light.on = True
    light.flash = False
    light.speed = 0

    if ctx.invoked_subcommand == "throbber":
        if light.color == (0, 0, 0):
            light.red = 255

    ctx.obj = light


@cli.command("fli")
def fli_subcommand(
    ctx: typer.Context,
    interval: float = typer.Option(
        0.1, "--interval", "-n", help="Seconds between flashes."
    ),
    intensity: int = typer.Option(
        255, "--intensity", "-i", help="Integer range: 0 - 255"
    ),
):
    """Flash Light Impressively.

    """

    light = ctx.obj

    color = deque([(0x0FF & intensity) >> 0, 0, 0])

    light.color = list(color)

    light.immediate = 1
    try:
        while True:
            color.rotate(1)
            light.color = list(color)
            sleep(interval)
    except KeyboardInterrupt:
        light.off = True
        light.reset()


@cli.command("throbber")
def throbber_subcommand(
    ctx: typer.Context,
    fast: int = typer.Option(
        0, "--fast", "-f", help="Integer range: 0 - 24", count=True
    ),
):
    """BlyncLight Intensifies.

    """

    light = ctx.obj

    step = 8 * (min(max(0, fast), 24) + 1)

    colors = Gradient(0, 255, step, light.red, light.green, light.blue)

    colors.extend(c for c in reversed(colors))

    light.color = (0, 0, 0)

    light.immediate = 1

    try:
        while True:
            for color in cycle(colors):
                light.color = color
                sleep(0.05)
    except KeyboardInterrupt:
        light.off = True
        light.reset()


@cli.command("rainbow")
def rainbow_subcommand(
    ctx: typer.Context,
    speed: int = typer.Option(
        1, "--speed", "-s", help="Decrease color cycle interval by 0.1 seconds."
    ),
):
    """BlyncLights Love Rainbows!

    """

    light = ctx.obj

    colors = [rgb for rgb in Spectrum(steps=255)]

    interval = speed * 0.1

    light.on = True
    light.color = (0, 0, 0)
    light.immediate = 1

    try:
        for color in cycle(colors):
            light.color = color
            sleep(interval)
    except KeyboardInterrupt:
        light.off = True
        light.reset()
