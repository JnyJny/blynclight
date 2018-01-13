#!/usr/bin/env python3

'''Flash Lights Impressively
'''

from blynclight import BlyncLightControl

if __name__ == '__main__':

    light = BlyncLightControl.getLight(0)

    colors = [ (255,0,0), (0,0,255) ]

    light.on()
    try:
        while True:
            light.cycle(colors, interval_ms=0)
    except KeyboardInterrupt:
        pass
