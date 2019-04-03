"""bindings for Embrava BlyncLight devices.

This module provides python bindings for interacting with the Embrava
BlyncLight family of devices via PyUSB.

You can control Embrava BlyncLight devices directly:

> from blynclight import BlyncLight
> b = BlyncLight.first_light()
> b.color = (0, 255, 0)                         # set color to blue
> b.on = True                                   # turn light on
> b.color = (255, 0, 0)                         # set color to red
> b.on = False                                  # turn light off

Or control the device via http API:

> from blynclight import BlyncLightProxy
> proxy = BlyncLightProxy('http://yourhost:port')
> available = proxy.status()
> proxy.on(0)
> proxy.red(0, 255)
> proxy.green(0, 0)
> proxy.blue(0, 255)
> proxy.color(0, (255,255,255))
> proxy.off(0)

The BlyncLightProxy method of control requires a HTTP server that
provides the expected REST interface. This is somewhat more involved
than talking to the light directly, but allows more flexibility.
"""


from .blynclight import BlyncLight

from .constants import DeviceType, FlashSpeed, MusicSelections, MusicVolume

from .proxy import Proxy as BlyncLightProxy


__all__ = [
    "BlyncLight",
    "BlyncLightProxy",
    "DeviceType",
    "FlashSpeed",
    "MusicSelections",
    "MusicVolume",
]
