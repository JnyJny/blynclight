"""
"""


class BlyncLightException(Exception):
    pass


class BlyncLightNotFound(BlyncLightException):
    pass


class BlyncLightInUse(BlyncLightException):
    pass


class BlyncLightUnknownDevice(BlyncLightException):
    pass
