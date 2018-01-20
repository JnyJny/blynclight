'''python bindings for Embrava BlyncLight devices.

This module provides python bindings for interacting with the Embrava
BlyncLight family of devices.

Control lights directly:

> from blynclight import BlyncLightControl
> b = BlyncLightControl.getLight(0)
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

from .blynclight import BlyncLightControl, BlyncLight
from .color import ColorToRGB, HexToRGB, RGBToHex
from .constants import (Color, DeviceType, DeviceInfo, FlashSpeed)
from .proxy import Proxy as BlyncLightProxy

__all__ = [
    'BlyncLight',
    'BlyncLightControl',
    'ColorToRGB',
    'HexToRGB',
    'RGBToHex',
    'Color',
    'DeviceType',
    'DeviceInfo',
    'FlashSpeed',
    'BlyncLightProxy',
]


            
    
