#!/usr/bin/env python3

'''
'''

import math
from blynclight import *
from time import sleep
from argparse import ArgumentParser


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
        r = int((math.sin(frequency[0] * i + phase[0]) * width) + center)
        g = int((math.sin(frequency[1] * i + phase[1]) * width) + center)
        b = int((math.sin(frequency[2] * i + phase[2]) * width) + center)
        yield (r,g,b)

if __name__ == '__main__':
    '''
    '''

    parser = ArgumentParser()
    
    parser.add_argument('-l','--light-id',
                        type=int,
                        default=0)    

    args = parser.parse_args()

    colors = [rgb for rgb in Spectrum(steps=256)]

    colors.extend(list(reversed(colors)))

    b = BlyncLightControl.getLight(args.light_id, color=(0,0,0))
    
    try:
        b.on = True
        while True:
            b.cycle(colors, interval_ms=0)
    except KeyboardInterrupt:
        pass
    b.on = False

    
            
        
