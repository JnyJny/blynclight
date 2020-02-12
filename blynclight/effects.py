"""
"""
from typing import List, Tuple
import math


def Gradient(
    start: int, stop: int, step: int, red=True, green=False, blue=False
) -> List[Tuple[int, int, int]]:
    """
    """
    colors = []
    for i in range(start, stop, step):
        colors.append((i if red else 0, i if blue else 0, i if green else 0))
    return colors


def Spectrum(
    steps: int = 64,
    frequency: Tuple[float, float, float] = None,
    phase: Tuple[int, int, int] = None,
    center: int = 128,
    width: int = 127,
) -> Tuple[float, float, float]:
    """Generator function that returns 'steps' (red,green,blue) tuples.

        steps: optional integer, default=64
    frequency: optional 3-tuple for rbg frequency, default=(.3,.3,.3)
        phase: optional 3-tuple for rbg phase, default=(0,2,4)
       center: optional integer, default=128
        width: optional integer, default=127

    Returns (r, b, g) where each member is a value between 0 and 255.
    """

    frequency = frequency or (0.3, 0.3, 0.3)
    phase = phase or (0, 2, 4)

    for i in range(steps):
        r = int((math.sin(frequency[0] * i + phase[0]) * width) + center)
        b = int((math.sin(frequency[2] * i + phase[2]) * width) + center)
        g = int((math.sin(frequency[1] * i + phase[1]) * width) + center)
        yield (r, b, g)
