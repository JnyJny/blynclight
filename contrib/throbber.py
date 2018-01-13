#!/usr/bin/env python3

'''
'''

import math
from blynclight import *
from time import sleep
from argparse import ArgumentParser

def Gradient(start, stop, step, red=True, green=False, blue=False):
    '''
    '''
    colors = []
    for i in range(start, stop, step):
        colors.append((i if red else 0,i if green else 0,i if blue else 0))
    return colors

if __name__ == '__main__':
    '''
    '''
    parser = ArgumentParser()
    
    parser.add_argument('-l','--light-id',
                        type=int,
                        default=0)    
    parser.add_argument('-r','--red',
                        action='store_true',
                        default=True)
    parser.add_argument('-g','--green',
                        action='store_true',
                        default=False)
    parser.add_argument('-b','--blue',
                        action='store_true',
                        default=False)
    parser.add_argument('-w','--white',
                        action='store_true',
                        default=False)
    parser.add_argument('-f','--fast',
                        action='count', default=0)
    parser.add_argument('-d','--dim',
                        action='store_true',
                        default=False)

    args = parser.parse_args()

    if args.white:
        args.red = True
        args.green = True
        args.blue = True    
    
    step = 8 * (min(args.fast, 24)+1)

    colors = Gradient(0, 255, step, args.red, args.green, args.blue)

    colors.extend(list(reversed(colors)))

    b = BlyncLightControl.getLight(args.light_id, color=(0,0,0))

    b.dim = args.dim
    
    try:
        b.on()
        while True:
            b.cycle(colors, interval_ms=0)
    except KeyboardInterrupt:
        pass
    b.off()

    
            
        
