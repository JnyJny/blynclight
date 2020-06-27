"""BlyncLight CLI Utility

Control your Embrava BlyncLight from the command-line!

"""

import sys
import typer


from blynclight import BlyncLightNotFound
from blynclight.blynclight import BlyncLight
from collections import deque
from itertools import cycle
from loguru import logger

from sys import stdout
from time import sleep

from .effects import Gradient, Spectrum
from .__version__ import __version__

cli = typer.Typer()

DEFAULT_COLOR = (0, 0, 255)  # (Red, Blue, Green)


def list_lights(value: bool) -> None:
    """Display a list of BlyncLights currently available and exit.

    Typer option callback.
    """
    if value:
        typer.secho(f"{'BlyncLights':19s}:", nl=False)
        lights = BlyncLight.available_lights()
        nlights = len(lights)
        typer.secho(f"{nlights}", fg="green" if nlights else "red")
        for index, info in enumerate(lights):
            typer.secho(f"ID:{'KEY':<16s}:VALUE", fg="blue")
            for key, value in info.items():
                if not len(str(value)):
                    continue
                if isinstance(value, int):
                    value = hex(value)
                if isinstance(value, bytes):
                    value = value.decode("utf-8")
                typer.secho(f"{index:02d}:{key:<16s}:", nl=False)
                typer.secho(value, fg="green")
        raise typer.Exit()


def report_version(value: bool) -> None:
    """Display the version and exit.

    Typer option callback.
    """
    if value:
        print(f"version: {__version__}")
        raise typer.Exit()


def verbosity(value: int) -> None:

    logger.remove()

    how_verbose = {0: 40, 1: 20, 2: 10, 3: 5}

    if value > 2:
        fmt = "<level>{level:>8}</>|{file}:{function}:{line}|{message}"
    else:
        fmt = "<level>{level:>8}</>|{message}"

    logger.add(sys.stdout, colorize=True, level=how_verbose.get(value, 5), format=fmt)


@cli.callback(invoke_without_command=True)
def blync_callback(
    ctx: typer.Context,
    light_id: int = typer.Option(
        0, "--light-id", "-l", show_default=True, help="Light identifier",
    ),
    red: int = typer.Option(
        0,
        "--red",
        "-r",
        is_flag=True,
        show_default=True,
        help="Red color value range: 0 - 255",
    ),
    blue: int = typer.Option(
        0,
        "--blue",
        "-b",
        is_flag=True,
        show_default=True,
        help="Blue color value range: 0 - 255",
    ),
    green: int = typer.Option(
        0,
        "--green",
        "-g",
        is_flag=True,
        help="Green color value range: 0 - 255",
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
        False, "--off/--on", "-o/-n", show_default=True, help="Turn the light off/on."
    ),
    dim: bool = typer.Option(
        False,
        "--dim",
        "-d",
        is_flag=True,
        help="Toggle bright/dim mode.",
        show_default=True,
    ),
    flash: int = typer.Option(
        0, "--flash", "-f", count=True, is_flag=True, help="Enable flash mode.",
    ),
    play: int = typer.Option(0, "--play", "-p", help="Select song: 1-15"),
    repeat: bool = typer.Option(
        False,
        "--repeat",
        is_flag=True,
        show_default=True,
        help="Repeat the selected song.",
    ),
    volume: int = typer.Option(
        5, "--volume", show_default=True, help="Set the volume: 1-10"
    ),
    available: bool = typer.Option(
        False,
        "--list-available",
        "-a",
        is_flag=True,
        is_eager=True,
        callback=list_lights,
    ),
    verbose: int = typer.Option(0, "--verbose", "-v", count=True, callback=verbosity),
    version: bool = typer.Option(
        False, "--version", "-V", is_flag=True, is_eager=True, callback=report_version
    ),
):
    """Control your Embrava BlyncLight from the command-line!

    ## Usage

    Use the `blync` utility to directly control your Embrava BlyncLight:

    \b
    ```console
    $ blync -R        # turn the light on with red color and leave it on
    $ blync --off     # turn the light off
    $ blync -RG --dim # turn the light on with yellow color and dim
    $ blync -RBG      # turn the light on with white color
    ```

    Colors can be specified by values between 0 and 255 using the lower-case
    color options or using the upper-case full value options.

    \b
    ```console
    $ blync -r 127                # half intensity red
    $ blync -r 255                # full intensity red
    $ blync -R                    # also full intensity red
    $ blync -r 255 -b 255 -g 255  # full intensity white
    $ blync -RBG                  # full intensity white
    ```


    If that's not enough fun, there are three builtin color modes:
    `fli`, `throbber`, and `rainbow`. All modes continue until the
    user terminates with a Control-C or platform equivalent.

    \b
    ```console
    $ blync fli
    $ blync throbber
    $ blync rainbow
    ```

    ## Installation

    \b
    ```console
    $ python3 -m pip install blynclight
    $ python3 -m pip install git+https://github.com/JnyJny/blynclight.git # latest
    ```

    This module depends on
    [hidapi](https://github.com/trezor/cython-hidapi), which supports
    Windows, Linux, FreeBSD and MacOS via a Cython module.
    """
    try:
        light = BlyncLight.get_light(light_id, immediate=False)
    except BlyncLightNotFound as error:
        typer.secho(str(error), fg="red")
        raise typer.Exit(-1) from None

    assert not light.immediate

    light.red = red if not red_b else 255
    light.blue = blue if not blue_b else 255
    light.green = green if not green_b else 255
    light.off = 1 if off else 0
    light.dim = 1 if dim else 0
    light.flash = 1 if flash > 0 else 0
    light.speed = flash

    light.mute = 0 if play else 1
    light.music = play
    light.play = 1 if play else 0
    light.volume = volume
    light.repeat = 1 if repeat else 0

    if not ctx.invoked_subcommand:

        if light.on and light.color == (0, 0, 0):
            light.color = DEFAULT_COLOR
        try:
            light.immediate = True
            for line in str(light).splitlines():
                logger.info(line)
        except Exception as error:
            typer.secho(str(error), fg="red")
            raise typer.Exit(-1) from None
        raise typer.Exit()

    # Disable flashing for subcommands.
    light.flash = 0

    ctx.obj = light


@cli.command("fli")
def fli_subcommand(
    ctx: typer.Context,
    interval: float = typer.Option(
        0.1, "--interval", "-n", help="Seconds between flashes.", show_default=True,
    ),
    intensity: int = typer.Option(
        255, "--intensity", "-i", help="Integer range: 0 - 255", show_default=True,
    ),
):
    """Flash Light Impressively.

    This mode cycles light color red, blue, green and then repeats. The
    user can specify the interval between color changes and the intesity
    of the colors. Color values specified on the command-line are ignored.

    ## Examples

    \b
    ```console
    $ blync fli -n 1      # one second between color changes
    $ blync fli -i 128    # light intensity is half as bright
    ```

    This mode runs until the user interrupts.
    """

    light = ctx.obj

    color = deque([(0x0FF & intensity) >> 0, 0, 0])

    try:
        light.color = color
        light.on = True
        light.immediate = 1

        while True:
            color.rotate(1)
            light.color = color
            sleep(interval)

    except KeyboardInterrupt:
        light.off = True
        light.reset()


@cli.command("throbber")
def throbber_subcommand(
    ctx: typer.Context,
    fast: int = typer.Option(0, "--faster", "-f", help="Increases speed.", count=True,),
):
    """BlyncLight Intensifies.

    This mode increases the intensity of the light color starting with
    the specified red, green and blue values and ramping the color
    intensity up and down and repeating. The user can increase the rate
    of ramp by adding more -f options to the command line:

    ## Examples

    \b
    ```console
    $ blync throbber -f   # a little faster
    $ blync throbber -ff  # a little more faster
    $ blync -G throbber   # throb with a green color
    ```

    This mode runs until the user interrupts.
    """

    light = ctx.obj

    if light.color == (0, 0, 0):
        light.red = 255

    try:
        step = 8 * (min(max(0, fast), 24) + 1)
        colors = Gradient(
            0, 255, step, light.red, light.green, light.blue, reverse=True
        )
        light.color = (0, 0, 0)
        light.immediate = 1

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
        1,
        "--slow",
        "-s",
        help="Increase color cycle interval by 0.1 seconds.",
        is_flag=True,
        count=True,
    ),
):
    """BlyncLights Love Rainbows.

    Smoothly transition the color of the light using a rainbow sequence.
    The user can slow the speed of the color cycling by adding more
    --slow options to the command line:

    ## Examples

    \b
    ```console
    $ blync rainbow -s   # slow cycling by 0.1 seconds
    $ blync rainbow -ss  # slow cycling by 0.15 seconds
    ```

    This mode runs until the user interrupts.
    """

    light = ctx.obj

    try:
        colors = [rgb for rgb in Spectrum(steps=255)]
        interval = speed * 0.05

        light.on = True
        light.color = (0, 0, 0)
        light.immediate = 1

        for color in cycle(colors):
            light.color = color
            sleep(interval)

    except KeyboardInterrupt:
        light.off = True
        light.reset()
