'''
'''

import pytest
from blynclight import (BlyncLight_API,
                        DeviceType,
                        MusicVolume,
                        FlashSpeed)


@pytest.fixture
def blynclight_api():
    return BlyncLight_API()


@pytest.fixture
def blynclight():
    return BlyncLight_API.first_light()


@pytest.fixture
def NODEV():
    return BlyncLight_API().ndevices


def test_blynclight_api_init(blynclight_api):
    '''
    '''
    assert blynclight_api._instance == blynclight_api


def test_blynclight_api_methods(blynclight_api):
    '''
    '''
    for func in blynclight_api._funcs.keys():
        assert getattr(blynclight_api, func)


def test_blynclight_api_nodev_nlights(blynclight_api):
    '''
    '''
    assert blynclight_api.nlights == 0


def test_blynclight_api_nodev_unique_device(blynclight_api):
    '''
    '''
    assert blynclight_api.unique_device_id(NODEV) != 0


def test_blynclight_api_nodev_device_type(blynclight_api):
    '''
    '''
    assert blynclight_api.device_type(NODEV) == DeviceType.INVALID


def test_blynclight_api_nodev_light_on(blynclight_api):
    '''
    '''
    assert blynclight_api.light_on(NODEV, 0, 0, 0) == 0


def test_blynclight_api_nodev_light_off(blynclight_api):
    '''
    '''
    assert blynclight_api.light_on(NODEV, 0, 0, 0) == 0


def test_blynclight_api_nodev_bright(blynclight_api):
    '''
    '''
    assert blynclight_api.bright(NODEV, 0) == 0
    assert blynclight_api.bright(NODEV, 1) == 0


def test_blynclight_api_nodev_flash(blynclight_api):
    '''
    '''
    assert blynclight_api.flash(NODEV, 0) == 0
    assert blynclight_api.flash(NODEV, 1) == 0


def test_blynclight_api_nodev_flash_speed(blynclight_api):
    '''
    '''
    for speed in range(FlashSpeed):
        assert blynclight_api.flash_speed(NODEV, speed) == 0


def test_blynclight_api_nodev_music(blynclight_api):
    '''
    '''
    assert blynclight_api.music(NODEV, 0) == 0
    assert blynclight_api.music(NODEV, 1) == 0


def test_blynclight_api_nodev_music_repeat(blynclight_api):
    '''
    '''
    assert blynclight_api.music_repeat(NODEV, 0) == 0
    assert blynclight_api.music_repeat(NODEV, 1) == 0


def test_blynclight_api_nodev_music_volume(blynclight_api):
    '''
    '''
    for volume in range(MusicVolume):
        assert blynclight_api.music_volume(NODEV, volume.value) == 0


def test_blynclight_api_nodev_music_select(blynclight_api):
    '''
    '''
    for m in range(10):
        assert blynclight_api.music_select(NODEV, m) == 0


def test_blynclight_api_nodev_mute(blynclight_api):
    '''
    '''
    assert blynclight_api.mute(NODEV, 0) == 0
    assert blynclight_api.mute(NODEV, 1) == 0
