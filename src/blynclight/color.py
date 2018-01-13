'''
'''

from enum import Enum

class Color(Enum):
    RED    = 0
    GREEN  = 1
    YELLOW = 2
    PURPLE = 3
    CYAN   = 4
    BLUE   = 5
    WHITE  = 6
    ORANGE = 7
    OFF    = 8

def ColorToRGB(color):
    '''
    '''
    if color == Color.RED:
        return (255, 0, 0)
    if color == Color.GREEN:
        return (0, 255, 0)
    if color == Color.YELLOW:
        return (255, 255, 0)
    if color == Color.PURPLE:
        return (148, 0, 211)
    if color == Color.CYAN:
        return (0, 255, 255)
    if color == Color.BLUE:
        return (0, 0, 255)
    if color == Color.WHITE:
        return (255, 255, 255)
    if color == Color.ORANGE:
        return (255, 127, 0)
    if color == Color.OFF:
        return (0, 0, 0)
    
    raise ValueError(f'unsupported color {color}')

def HexToRGB(hexValue):
    '''
    '''
    hexStr = hex(hexValue)[2:]

    if len(hexStr) == 6:
        return tuple(map(int, [hexStr[:2], hexStr[2:4], hexStr[4:]]))

    raise ValueError(f'hex value out of bounds {hexValue}')
