'''python bindings for Embrava BlyncLight devices.

This module provides python bindings for interacting with the Embrava
BlyncLight family of devices.

Control lights directly:

> from blynclight import BlyncLight_API
> b = BlyncLight_API.first_light()
> b.color = (0, 255, 0)                         # set color to green
> b.on = True                                   # turn light on
> b.color = (255, 0, 0)                         # set color to red
> b.on = False                                  # turn light off

Control lights via http API:

> from blynclight import BlyncLightProxy
> proxy = BlyncLightProxy('http://yourhost:port')
> available = proxy.status()
> proxy.on(0)
> proxy.red(0, 255)
> proxy.green(0, 0)
> proxy.blue(0, 255)
> proxy.color(0, (255,255,255))
> proxy.off(0)

'''


from .blynclight import BlyncLight
from .constants import (DeviceType, FlashSpeed,
                        MusicSelections, MusicVolume)
from .proxy import Proxy as BlyncLightProxy

__all__ = [
    'BlyncLight',
    'FlashSpeed', 'DeviceType',
    'MusicSelections', 'MusicVolume',
    'BlyncLightProxy',
]
