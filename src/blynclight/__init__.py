'''python bindings for Embrava BlyncLight devices.

This module provides python bindings for Embrava BlyncLight family of
devices.

> from blynclight import BlyncLightControl
> b = BlyncLightControl.getLight(0)
> b.color = (0, 255, 0)                         # set color to green
> b.on = True                                   # turn light on
> b.color = (255, 0, 0)                         # set color to red
> b.on = False                                  # turn light off

'''

from .blynclight import BlyncLightControl, BlyncLight, DeviceInfo
from .color import Color, ColorToRGB, HexToRGB
from .devicetype import DeviceType
from .flashspeed import FlashSpeed

__all__ = [ 'BlyncLight',
            'BlyncLightControl',
            'Color',
            'ColorToRGB',
            'DeviceInfo',
            'DeviceType',
            'FlashSpeed',
            'HexToRGB']


            
    
