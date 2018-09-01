'''
'''

import pytest
from blynclight import (BlyncLight,
                        DeviceType,
                        MusicVolume,
                        FlashSpeed)


@pytest.fixture
def blynclight():
    return BlyncLight.first_light()


def test_blynclight_classmethods():

    assert len(BlyncLight.available_lights()) != 0
    assert BlyncLight.first_light()


def test_blynclight_init(blynclight):

    assert blynclight.report == 0
    assert blynclight.red == 0
    assert blynclight.blue == 0
    assert blynclight.green == 0
    assert blynclight.off == 1
    assert blynclight.dim == 0
    assert blynclight.flash == 0
    assert blynclight.speed == 0
    assert blynclight.pad0 == 0
    assert blynclight.mute == 0
    assert blynclight.music == 0
    assert blynclight.start == 0
    assert blynclight.repeat == 0
    assert blynclight.pad1 == 0
    assert blynclight.volume == 0
    assert blynclight.pad2 == 0
    assert blynclight.eom == 0xffff
    assert blynclight.vendor_id == 0x2c0d
    assert blynclight.product_id > 0
    assert blynclight._handle
    assert blynclight.immediate


def test_blynclight_bitfields(blynclight):

    blynclight.immediate = False
    assert not blynclight.immediate
    blynclight.report = 1
    assert blynclight.report == 0
    blynclight.red = 0x11
    assert blynclight.red == 0x11
    blynclight.blue = 0x22
    assert blynclight.blue == 0x22
    blynclight.green = 0x33
    assert blynclight.green == 0x33
    blynclight.off = 0
    assert blynclight.off == 0
    blynclight.off = 1
    assert blynclight.off == 1
    blynclight.on = 0
    assert blynclight.off == 1
    blynclight.on = 1
    assert blynclight.off == 0
    blynclight.dim = 1
    assert blynclight.dim == 1
    blynclight.dim = 0
    assert blynclight.dim == 0
    blynclight.bright = 0
    assert blynclight.dim == 1
    blynclight.bright = 1
    assert blynclight.dim == 0
    blynclight.flash = 1
    assert blynclight.flash == 1
    blynclight.flash = 0
    assert blynclight.flash == 0
    for i in range(0, 3):
        blynclight.speed = 1 << i
        assert blynclight.speed == 1 << i
    blynclight.pad0 = 1
    assert blynclight.pad0 == 0
    blynclight.mute = 1
    assert blynclight.mute == 1
    blynclight.mute = 0
    assert blynclight.mute == 0
    for i in range(0, 11):
        blynclight.music = i
        assert blynclight.music == i
    blynclight.start = 1
    assert blynclight.start == 1
    blynclight.start = 0
    assert blynclight.start == 0
    blynclight.repeat = 1
    assert blynclight.repeat == 1
    blynclight.repeat = 0
    assert blynclight.repeat == 0
    blynclight.pad1 = 1
    assert blynclight.pad1 == 0
    for i in range(0, 11):
        blynclight.volume = i
        assert blynclight.volume == i
    blynclight.pad2 = 1
    assert blynclight.pad2 == 0
    blynclight.eom = 0
    assert blynclight.eom == 0xffff
    assert blynclight.vendor_id == 0x2c0d
    assert blynclight.product_id > 0
    assert blynclight._handle
    blynclight.immediate = True
    assert blynclight.immediate
