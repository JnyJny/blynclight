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
def DEV():
    return 0


def test_blynclight_api_init(blynclight_api):
    '''
    '''
    assert blynclight_api._instance == blynclight_api


def test_blynclight_api_methods(blynclight_api):
    '''
    '''
    for func in blynclight_api._funcs.keys():
        assert getattr(blynclight_api, func)


def test_blynclight_api_dev_nlights(blynclight_api):
    '''
    '''
    assert blynclight_api.nlights == 1


def test_blynclight_api_dev_unique_device(blynclight_api):
    '''
    '''
    assert blynclight_api.unique_device_id(DEV) != 0


def test_blynclight_api_dev_device_type(blynclight_api):
    '''
    '''
    assert blynclight_api.device_type(DEV) == DeviceType.INVALID


def test_blynclight_api_dev_light_on(blynclight_api):
    '''
    '''
    assert blynclight_api.light_on(DEV, 0, 0, 0) == 1


def test_blynclight_api_dev_light_off(blynclight_api):
    '''
    '''
    assert blynclight_api.light_on(DEV, 0, 0, 0) == 1


def test_blynclight_api_dev_bright(blynclight_api):
    '''
    '''
    assert blynclight_api.bright(DEV, 0) == 1
    assert blynclight_api.bright(DEV, 1) == 1


def test_blynclight_api_dev_flash(blynclight_api):
    '''
    '''
    assert blynclight_api.flash(DEV, 0) == 1
    assert blynclight_api.flash(DEV, 1) == 1


def test_blynclight_api_dev_flash_speed(blynclight_api):
    '''
    '''
    for speed in range(FlashSpeed):
        assert blynclight_api.flash_speed(DEV, speed) == 1


def test_blynclight_api_dev_music(blynclight_api):
    '''
    '''
    assert blynclight_api.music(DEV, 0) == 1
    assert blynclight_api.music(DEV, 1) == 1


def test_blynclight_api_dev_music_repeat(blynclight_api):
    '''
    '''
    assert blynclight_api.music_repeat(DEV, 0) == 1
    assert blynclight_api.music_repeat(DEV, 1) == 1


def test_blynclight_api_dev_music_volume(blynclight_api):
    '''
    '''
    for volume in range(MusicVolume):
        assert blynclight_api.music_volume(DEV, volume.value) == 1


def test_blynclight_api_dev_music_select(blynclight_api):
    '''
    '''
    for m in range(10):
        assert blynclight_api.music_select(DEV, m) == 1


def test_blynclight_api_dev_mute(blynclight_api):
    '''
    '''
    assert blynclight_api.mute(DEV, 0) == 1
    assert blynclight_api.mute(DEV, 1) == 1
