'''
'''

from .constants import Color

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
    if isinstance(hexValue, str):
        hexStr = hexValue[2:]
    else:
        hexStr = hex(hexValue)[2:]

    f = lambda v: int(v, 16)

    if len(hexStr) == 6:
        return tuple(map(f, [hexStr[:2], hexStr[2:4], hexStr[4:]]))

    raise ValueError(f'hex value out of bounds {hexValue}')

def RGBToHex(rgb):
    '''
    '''
    return f'0x{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
