from unittest.mock import patch

import pytest
from pexpect import pxssh

from pytleap import Eap, PytleapError


@pytest.fixture
def eap():
    """Initialize EAP device."""
    return Eap("localhost", "admin", "1234")


@patch("pexpect.pxssh.pxssh.login")
def test_failed_to_connect(mock_login, eap):
    """Testing exception at login."""
    from pexpect import exceptions

    mock_login.side_effect = exceptions.EOF("Test")
    with pytest.raises(PytleapError):
        eap.connect()


@patch("pexpect.pxssh.pxssh.logout")
@patch("pexpect.pxssh.pxssh.login", autospec=True)
@patch("pexpect.pxssh.pxssh.prompt")
@patch("pexpect.pxssh.pxssh.sendline")
def test_fail_to_retrieve_wlanconfig(
    mock_sendline, mock_prompt, mock_login, mock_logout, eap
):
    """Testing exception in get_wifi_clients."""

    mock_prompt.side_effect = pxssh.ExceptionPxssh("Test")
    with pytest.raises(PytleapError):
        eap.get_wifi_clients()
