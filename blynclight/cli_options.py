"""
"""

from .__version__ import __version__
from .blynclight import BlyncLight
from typer import Option, Exit


def typer_callback(function):
    """Typer callback function decorator. If the value passed
    in evaluates True, function is called and typer.Exit is
    raised. Otherwise the function returns.
    """

    def wrapper(ctx, param, value):
        if value:
            function()
            raise Exit()

    return wrapper


@typer_callback
def report_version():
    print(f"version: {__version__}")


@typer_callback
def list_lights():
    BlyncLight.report_available()


version_option = Option(
    False,
    "--version",
    is_eager=True,
    callback=report_version,
    help="Report version and exit.",
)

list_available_option = Option(
    False,
    "--list-available",
    "-a",
    is_eager=True,
    callback=list_lights,
    help="List available lights and exit.",
)

light_id_option = Option(0, "--light-id", "-i", help="Integer light identifier.")
red_option = Option(0, "--red", "-r", help="Integer range: 0 - 255")
blue_option = Option(0, "--blue", "-b", help="Integer range: 0 - 255")
green_option = Option(0, "--green", "-g", help="Integer range: 0 - 255")
dim_option = Option(False, "--dim", "-d", help="Toggle bright mode.")
verbose_option = Option(False, "--verbose", "-v")
