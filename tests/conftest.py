import pytest

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

from typer.testing import CliRunner


@pytest.fixture(scope="module")
def Runner() -> CliRunner:
    """Module scoped :class: `typer.testing.CliRunner` instance."""
    return CliRunner()


@pytest.fixture
def Light():
    """Function scoped :class: `blynclight.BlyncLight` instance.

    Returns the first BlyncLight found.

    If no light is available, a BlyncLight is assembled
    with a mocked device property and product_id of 0xffff.
    """

    try:
        return BlyncLight.get_light()
    except BlyncLightNotFound:
        pass

    class MockDevice:
        def write(self, data):
            return COMMAND_LENGTH

        def close(self):
            pass

    # pass in immediate=False to suppress writes to the device
    # until the device attribute has been successfully updated
    # with the mock object.

    b = BlyncLight(EMBRAVA_VENDOR_IDS[0], 0xFFFF, immediate=False)
    b._device = MockDevice()
    return b
