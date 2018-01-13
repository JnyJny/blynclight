'''python bindings for Embrava BlyncLight devices.

This module provides python bindings for Embrava BlyncLight family of
devices.

> from blynclight import BlyncLightControl
> b = BlyncLightControl.getLight(0)
> b.color = (255, 0, 0)
> b.on()
> b.off()

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


            
    
