"""
"""

import pytest

from blynclight.__version__ import __version__
from blynclight.__main__ import blync_cli, fli_cli, rainbow_cli, throbber_cli

cli_s = [blync_cli, fli_cli, rainbow_cli, throbber_cli]


@pytest.mark.parametrize("cli", cli_s)
def test_common_cli_version(cli, Runner):
    result = Runner.invoke(blync_cli, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


@pytest.mark.parametrize("cli", cli_s)
def test_common_cli_help(cli, Runner):
    result = Runner.invoke(blync_cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output


@pytest.mark.parametrize("cli", cli_s)
def test_common_cli_list_available_lights(cli, Runner):
    result = Runner.invoke(blync_cli, ["--list-available"])
    assert result.exit_code == 0
    assert "KEY:ID:VALUE" in result.output
