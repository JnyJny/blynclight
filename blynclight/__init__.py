"""bindings for Embrava BlyncLight devices.

This module provides python bindings for interacting with the Embrava
BlyncLight family of devices via Human Input Device Application
Programming Interface (HIDAPI). HIDAPI is a C language library that
provides access to USB devices.

You can control Embrava BlyncLight devices directly:

> from blynclight import BlyncLight
> b = BlyncLight.get_light()
> b.color = (0, 255, 0)                         # set color to blue
> b.on = True                                   # turn light on
> b.color = (255, 0, 0)                         # set color to red
> b.on = False                                  # turn light off

"""

from .blynclight import BlyncLight

from .constants import FlashSpeed, MusicSelections

from .exceptions import BlyncLightNotFound, BlyncLightUnknownDevice, BlyncLightInUse

__all__ = [
    "BlyncLight",
    "BlyncLightNotFound",
    "BlyncLightInUse",
    "BlyncLightUnknownDevice",
    "FlashSpeed",
    "MusicSelections",
]
