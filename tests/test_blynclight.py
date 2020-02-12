"""Test Embrava BlyncLight Functionality

These tests can be executed whether or not a phyiscal BlyncLight device
is present. If a device is not present, writes to the physical device
are intercepted by a mock object which pretends to successfully write
the in-memory model to the device. If a light is present, the writes
go to the device. 
"""

import pytest
from dataclasses import dataclass

from blynclight import (
    BlyncLight,
    BlyncLightNotFound,
    BlyncLightUnknownDevice,
    BlyncLightInUse,
)

from blynclight.constants import (
    EMBRAVA_VENDOR_IDS,
    END_OF_COMMAND,
    COMMAND_LENGTH,
    PAD_VALUE,
)


@dataclass
class FieldToTest:
    """Encapsulates field name, a value to set and the expected value when
    the field is read.
    """

    name: str
    value: int
    expected: int


### BlyncLights are controlled by a command word that is composed of
### bit fields. We build a list of fields to test where each Field
### entry has a name, a value to use setting the field and the
### expected value when we read the field again.  Some fields are
### invariant and return the same value regardless of the setting
### value: eoc, report and pads zero thru three.


@pytest.fixture(
    params=[
        FieldToTest("immediate", 0, 0),
        FieldToTest("immediate", 1, 1),
        FieldToTest("report", 1, 0),
        FieldToTest("red", 0xFF, 0xFF),
        FieldToTest("blue", 0xFF, 0xFF),
        FieldToTest("green", 0xFF, 0xFF),
        FieldToTest("off", 0, 0),
        FieldToTest("off", 1, 1),
        FieldToTest("on", 0, 0),
        FieldToTest("on", 1, 1),
        FieldToTest("dim", 1, 1),
        FieldToTest("dim", 0, 0),
        FieldToTest("flash", 1, 1),
        FieldToTest("flash", 0, 0),
        FieldToTest("speed", 1 << 0, 1 << 0),
        FieldToTest("speed", 1 << 1, 1 << 1),
        FieldToTest("speed", 1 << 2, 1 << 2),
        FieldToTest("speed", 0, 0),
        FieldToTest("pad0", 1, PAD_VALUE),
        FieldToTest("music", 1, 1),  # XXX not sure how many music values there are
        FieldToTest("music", 0, 0),
        FieldToTest("play", 1, 1),
        FieldToTest("play", 0, 0),
        FieldToTest("repeat", 1, 1),
        FieldToTest("repeat", 0, 0),
        FieldToTest("pad1", 1, PAD_VALUE),
        FieldToTest("volume", 1, 1),
        FieldToTest("volume", 2, 2),
        FieldToTest("volume", 3, 3),
        FieldToTest("volume", 4, 4),
        FieldToTest("volume", 5, 5),
        FieldToTest("volume", 6, 6),
        FieldToTest("volume", 7, 7),
        FieldToTest("volume", 8, 8),
        FieldToTest("volume", 9, 9),
        FieldToTest("volume", 0, 0),
        FieldToTest("pad2", 1, PAD_VALUE),
        FieldToTest("mute", 1, 1),
        FieldToTest("mute", 0, 0),
        FieldToTest("eoc", 0, END_OF_COMMAND),
        FieldToTest("pad3", 1, PAD_VALUE),
    ]
)
def a_field(request):
    """This fixture presents a list of FieldToTest objects to test
    setting fields on the BlyncLight and making sure that the value
    can be read back. 
    """
    return request.param


@pytest.fixture(
    params=[
        FieldToTest("immediate", 0, 0),
        FieldToTest("report", 1, 0),
        FieldToTest("red", 0xFF, 0),
        FieldToTest("blue", 0xFF, 0),
        FieldToTest("green", 0xFF, 0),
        FieldToTest("off", 0, 1),
        FieldToTest("dim", 1, 0),
        FieldToTest("flash", 1, 0),
        FieldToTest("speed", 1, 0),
        FieldToTest("pad0", 1, PAD_VALUE),
        FieldToTest("music", 1, 0),
        FieldToTest("play", 1, 0),
        FieldToTest("repeat", 1, 0),
        FieldToTest("pad1", 1, PAD_VALUE),
        FieldToTest("volume", 1, 0),
        FieldToTest("pad2", 1, PAD_VALUE),
        FieldToTest("mute", 1, 0),
        FieldToTest("eoc", 0, END_OF_COMMAND),
        FieldToTest("pad3", 1, PAD_VALUE),
        FieldToTest("immediate", 1, 0),
    ]
)
def reset_field(request):
    """This fixture presents a list of FieldToTest objects for the
    purpose of testing the BlyncLight.reset() method. The fields
    are set to the given value and after reset should match the
    expected value.
    """
    return request.param


@pytest.fixture()
def number_of_lights():
    """Number of physical Embrava BlyncLight devices detected.
    """
    return len(BlyncLight.available_lights())


def test_blynclight_available_lights():
    """Checks that the BlyncLight.available_lights() class method returns
    a list of dictionaries, one dictionary for each BlyncLight device
    discovered.
    """
    info = BlyncLight.available_lights()
    assert isinstance(info, list)
    for entry in info:
        assert isinstance(entry, dict)
        assert entry.get("vendor_id", None)
        assert entry.get("product_id", None)


def test_blynclight_get_light(number_of_lights):
    """Test the BlyncLight.get_light() class method to ensure that it
    returns a BlyncLight object if the specified light is available.
    The test also makes sure BlyncLightNotFound is raised when a
    nonexistent light is requested.

    :param number_of_lights: integer fixture
    """

    assert number_of_lights >= 0

    if number_of_lights > 0:
        assert isinstance(BlyncLight.get_light(), BlyncLight)
        assert isinstance(BlyncLight.get_light(0), BlyncLight)
        with pytest.raises(BlyncLightNotFound):
            BlyncLight.get_light(number_of_lights)
        return

    # We get here if no lights are currently available
    assert number_of_lights == 0

    with pytest.raises(BlyncLightNotFound):
        BlyncLight.get_light()
        BlyncLight.get_light(0)


def test_blynclight_unknown_device():
    """Tests the BlyncLight.__init__ method to make sure that
    BlyncLightUnknownDevice is raised if we feed it a bogus vendor
    identifier.
    """
    bogus = 0xFFFF
    assert bogus not in EMBRAVA_VENDOR_IDS

    with pytest.raises(BlyncLightUnknownDevice):
        BlyncLight(bogus, bogus)


def test_blynclight_vendor(Light):
    """:param light: BlyncLight fixture

    Double check that the BlycnLight's vendor_id property is
    in the list of the known Embrava vendor identifiers. This
    check occurs in the BlyncLight __init__ so maybe not
    needed here.
    """
    assert Light.vendor_id in EMBRAVA_VENDOR_IDS


def test_blynclight_product_id(Light):
    """:param Light: BlyncLight fixture

    Double check that the BlyncLight's product_id property is
    non-zero (it's a hidapi wildcard value).
    """
    assert Light.product_id != 0


def test_blynclight_device(Light):
    """:param Light: BlyncLight fixture

    Check to make sure the BlyncLight's device property is not None.
    """
    assert Light.device


def test_blynclight_length(Light):
    """:param Light: BlyncLight fixture
    
    Check to make sure the BlyncLight's length is COMMAND_LENGTH.
    """
    assert len(Light) == COMMAND_LENGTH


def test_blynclight_command_property(Light):
    """:param Light: BlyncLight fixture

    Check to make sure the BlyncLight command property is a
    list of strings.
    """
    assert isinstance(Light.commands, list)
    for command in Light.commands:
        assert isinstance(command, str)


def test_bitfield(Light, a_field):
    """:param Light: BlyncLight fixture
    :param a_field: FieldToTest fixture

    Tests a BlyncLight field by setting the light's
    field to value and then comparing the attribute's
    value to the expected value. All the fields specified in
    the a_field fixture are tested, regardless of whether the
    field is a valid 'command' or a padding or control field.
    """
    setattr(Light, a_field.name, a_field.value)
    value = getattr(Light, a_field.name)
    assert value == a_field.expected


def test_color_property_tuple(Light):
    """:param Light: BlyncLight fixture

    The BlyncLight color property is a synthetic property that
    suspends device updates while the red, blue and green fields
    are updated. Once the red, blue, and green fields are set
    in-memory, updates to the hardware are re-enabled.

    This test sets the color property using a three-tuple of 8-bit
    integers, e.g.:

    > light.color = (0xaa, 0xbb, 0xcc)

    The color property getter is compared to the three-tuple and
    the individual color fields are checked to make sure they
    were updated with expected values.
    """
    Light.color = (0xAA, 0xBB, 0xCC)
    assert Light.color == (0xAA, 0xBB, 0xCC)
    assert Light.red == 0xAA
    assert Light.blue == 0xBB
    assert Light.green == 0xCC


def test_color_property_hex(Light):
    """:param light: BlyncLight fixture

    The BlyncLight color property is a synthetic property that
    suspends device updates while the red, blue and green fields
    are updating. Once the red, blue, and green fields are set
    in-memory, updates to the hardware are re-enabled.

    This test sets the color property using a 24-bit integer:

    > Light.color = 0x112233

    The color property getter is compared to the expected three-tuple
    and the individual color fields are checked to make sure they were
    updated with expected values.
    """
    Light.color = 0x112233
    assert Light.color == (0x11, 0x22, 0x33)
    assert Light.red == 0x11
    assert Light.blue == 0x22
    assert Light.green == 0x33


def test_updates_paused_context_manager(Light):
    """:param light: BlyncLight fixture

    By default, a BlyncLight object writes it's in-memory
    representation of the command word to the device whenever
    a field is written. The updates_paused() method is a
    context manager that will suspend updates to the device
    for the duration of the context manager's execution.

    This method sets the immediate field to a known value,
    starts a context manager, checks that immediate is zero
    and then checks that immediate is restored to it's
    original value when the context manager exits.
    """
    for value in [True, False]:
        Light.immediate = value
        assert Light.immediate == value
        with Light.updates_paused():
            assert Light.immediate == False
        assert Light.immediate == value


def test_on_property(Light):
    """:param light: BlyncLight fixture

    The BlyncLight 'on' property is a synthetic negative logic accessor
    for the 'off' field in the command word. It made more sense to me
    to turn a light on with:

    light.on = 1

    instead of:

    light.off = 0

    Those statements are equivalent, the test makes sure that manipulating
    'on' sets 'off' appropriately and vice-versa
    """
    for value in [False, True]:
        Light.off = value
        assert Light.off == value
        assert Light.on == (not value)

        Light.on = value
        assert Light.on == value
        assert Light.off == (not value)


def test_bright_property(Light):
    """:param light: Blynclight fixture

    The BlyncLight 'bright' property is a synthetic opposite logic
    accessor for the 'dim' field in the command word. It made more sense
    to me to make the light bright with:

    light.bright = 1

    instead of

    light.dim = 0
    
    Those statements are equivalent, the test makes sure that manipulating
    'bright' sets 'dim' appropriately and vice-versa.
    """

    for value in [False, True]:
        Light.dim = value
        assert Light.dim == value
        assert Light.bright == (not value)

        Light.bright = value
        assert Light.bright == value
        assert Light.dim == (not value)


def test_open_same_device(number_of_lights):
    """:param number_of_lights: integer fixture

    Two BlyncLight objects cannot open the same device, so here we
    test that BlyncLightInUse is raised when that is attempted. This
    only works if there are physical lights to test against, which is
    controlled with the number_of_lights fixture.
    """

    if number_of_lights <= 0:
        return

    a_light = BlyncLight.get_light()
    assert isinstance(a_light, BlyncLight)

    with pytest.raises(BlyncLightInUse):
        b_light = BlyncLight.get_light()

    del a_light

    c_light = BlyncLight.get_light()
    assert isinstance(c_light, BlyncLight)


def test_reseting_light(Light, reset_field):
    """:param light: BlyncLight fixture
    :param reset_field: FieldToTest fixture

    Dirties up the light and then resets() it to a known state.

    Each time a field in the light is altered, reset() is called and
    the reset field value compared to the expected value.
    """

    setattr(Light, reset_field.name, reset_field.value)

    Light.reset(flush=False)

    value = getattr(Light, reset_field.name)
    assert value == reset_field.expected


def test_status_property(Light):
    """:param light: BlyncLight fixture
    
    Confirms that the BlyncLight property 'status' is a
    dictionary, that keys of the dictionary are those
    enumerated by the commands property and that the
    values of the commands are integers.
    """

    status = Light.status
    assert isinstance(status, dict)
    for command in Light.commands:
        assert command in status.keys()
        value = status[command]
        assert isinstance(value, int)
