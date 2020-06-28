import pytest

from unittest import mock

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

    with mock.patch("hid.device") as MockHelper:
        b = BlyncLight(EMBRAVA_VENDOR_IDS[0], 0xFFFF, immediate=False)

    return b
