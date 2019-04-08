"""Test blynclight.hid.HidDevice

These tests do not depend on the existence of a particular
USB device but it does require *some* USB devices to act
upon.

These tests focus on enumerating, opening, and closing
devices. The read and write functions are not tested
since that requires some specific knowledge about the
device we are attempting to perform I/O on.

"""

import pytest
from blynclight.hid import HidDevice


@pytest.fixture(scope="session")
def devices():
    """List of dictionaries fixture returned from the class method
    blynclight.hid.HidDevice.enumerate(). The enumerate method makes
    no guarantees about device ordering between invocations, so we use
    session scope for this fixture to keep repeated uses consistent
    between tests.

    """
    return HidDevice.enumerate()


@pytest.fixture(scope="session")
def hid_device(devices):
    """A blynclight.hid.HidDevice fixture that represents the last device
    in the 'devices' fixture. Tests often use the first device in
    devices so using the last device avoids attempting to open a
    device that is already open while still making a HidDevice
    available. This fixture has session scope.

    """
    device = HidDevice.from_dict(devices[-1])
    yield device


def test_classmethod_enumerate():
    """Ensure that the output of blynclight.hid.HidDevice.enumerate
    returns a list of dictionaries and spot checks the dictionary
    contents for the keys 'vendor_id' and 'product_id'.

    """
    devices = HidDevice.enumerate()
    assert devices
    assert isinstance(devices, list)

    for device in devices:
        assert device
        assert isinstance(device, dict)
        assert "vendor_id" in device.keys()
        assert "product_id" in device.keys()


def test_classmethod_from_dict_good_data(devices):
    """:param devices: list of dictionaries fixture

    Tests the blynclight.hid.HidDevice.from_dict convenience method
    using presumably good device information dictionaries sourced from
    the enumerate class method.

    """
    try:
        device = HidDevice.from_dict(devices[0])
        assert isinstance(device, HidDevice)
        assert device.vendor_id == devices[0]["vendor_id"]
        assert device.product_id == devices[0]["product_id"]
        del (device)
    except KeyError:
        pass


def test_classmethod_from_dict_bad_data():
    """Tests the blynclight.hid.HidDevice.from_dict convenience method
    using synthetic bad data, specifically:

    - an empty dictionary
    - a dictionary with only a vendor_id key
    - a dictionary with only a product_id key

    """

    with pytest.raises(LookupError):
        HidDevice.from_dict({})

    with pytest.raises(LookupError):
        HidDevice.from_dict({"vendor_id": None})

    with pytest.raises(LookupError):
        HidDevice.from_dict({"product_id": None})


def test_hiddevice_init(devices):
    """:param devices: list of dictionaries fixture

    Tests creating a blynclight.hid.HidDevice and ensures that the
    HidDevice is configured with the specified vendor_id and
    product_id.

    """

    device = HidDevice(devices[0]["vendor_id"], devices[0]["product_id"])
    assert isinstance(device, HidDevice)
    assert device.vendor_id == devices[0]["vendor_id"]
    assert device.product_id == devices[0]["product_id"]


def test_hiddevice_open_twice(devices):
    """:param devices: list of dictionaries fixture

    The hidapi library does not allow a USB device to be opened twice
    in the same process, so we test for that by opening the first
    device twice.

    """

    device = HidDevice.from_dict(devices[0])

    with pytest.raises(ValueError):
        HidDevice(device.vendor_id, device.product_id)
