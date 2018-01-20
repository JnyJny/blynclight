#!/usr/bin/env python3

'''BlyncLights Love Rainbows.
'''

from blynclight import BlyncLightProxy
from argparse import ArgumentParser
from time import sleep
from math import sin

def Spectrum(steps=64, frequency=None, phase=None, center=128, width=127):
    '''generator function that returns 'steps' rgb tuples.

        steps: optional integer, default=64
    frequency: optional 3-tuple for rgb frequency, default=(.3,.3,.3)
        phase: optional 3-tuple for rgb phase, default=(0,2,4)
       center: optional integer, default=128
        width: optional integer, default=127

    Returns a 3-tuple (r,g,b) where each member is a value between 0 and
    255.

    '''
    frequency = frequency or (.3, .3, .3)
    phase = phase or (0, 2, 4)

    for i in range(steps):
        r = int((sin(frequency[0] * i + phase[0]) * width) + center)
        g = int((sin(frequency[1] * i + phase[1]) * width) + center)
        b = int((sin(frequency[2] * i + phase[2]) * width) + center)
        yield (r,g,b)

if __name__ == '__main__':
    '''
    '''

    parser = ArgumentParser()
    
    parser.add_argument('-l','--light-id',
                        type=int,
                        default=0)
    
    parser.add_argument('-s','--speed',
                        action='count',
                        default=0)

    args = parser.parse_args()

    colors = [rgb for rgb in Spectrum(255)]

    colors.extend(list(reversed(colors)))

    interval = (args.speed * 100)

    proxy = BlyncLightProxy()

    # XXX need to get available light_id's and validate the user's request
    
    try:
        proxy.on(args.light_id)
        while True:
            for color in colors:
                proxy.color(args.light_id, color)
                sleep(interval)
    except KeyboardInterrupt:
        pass
    proxy.off(args.light_id)

    
            
        
