import pytest
from aioresponses import aioresponses

from pytleap import Eap
from pytleap.error import AuthenticationError, PytleapError

from .common import load_fixture


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


@pytest.fixture
def eap(event_loop, mock_aioresponse):
    """Create and connect an EAP device."""
    eap = Eap("http://localhost", "admin", "1234")
    mock_aioresponse.get("http://localhost", status=200, body="")
    mock_aioresponse.post("http://localhost", status=200, body="")
    mock_aioresponse.get(
        "http://localhost/data/status.device.json?operation=read",
        status=200,
        body=load_fixture("status.device_good.json"),
        headers={"content-type": "text/html"},
    )
    event_loop.run_until_complete(eap.connect())
    yield eap
    event_loop.run_until_complete(eap.disconnect())


def test_connect_ok(event_loop, mock_aioresponse):
    eap = Eap("http://localhost", "admin", "1234")
    mock_aioresponse.get("http://localhost", status=200, body="")
    mock_aioresponse.post("http://localhost", status=200, body="")
    mock_aioresponse.get(
        "http://localhost/data/status.device.json?operation=read",
        status=200,
        body=load_fixture("ok.json"),
        headers={"content-type": "text/html"},
    )
    event_loop.run_until_complete(eap.connect())
    assert eap.is_connected
    event_loop.run_until_complete(eap.disconnect())
    assert not eap.is_connected


def test_failed_to_connect(event_loop, mock_aioresponse):
    eap = Eap("http://localhost", "admin", "1234")
    mock_aioresponse.get("http://localhost", status=200, body="")
    mock_aioresponse.post("http://localhost", status=200, body="")
    mock_aioresponse.get(
        "http://localhost/data/status.device.json?operation=read",
        status=200,
        body=load_fixture("timeout.json"),
        headers={"content-type": "text/html"},
    )
    with pytest.raises(PytleapError) as excinfo:
        event_loop.run_until_complete(eap.connect())
    assert type(excinfo.value) == AuthenticationError


def test_retrieve_eap_data(eap):
    assert eap.mac_address == "aa:bb:cc:dd:ee:ff"
    assert eap.name == "EAP245-AA-BB-CC-DD-EE-FF"


def test_get_wifi_clients(event_loop, mock_aioresponse, eap):
    mock_aioresponse.get(
        "http://localhost/data/status.client.user.json?operation=load",
        status=200,
        body=load_fixture("status.client.user_good.json"),
        headers={"content-type": "text/html"},
    )
    clients = event_loop.run_until_complete(eap.get_wifi_clients())
    assert len(clients) == 4
    assert {
        "11:22:33:44:55:66",
        "00:aa:11:bb:33:cc",
        "ff:11:ee:22:dd:33",
        "ff:55:ee:44:dd:33",
    } == {c.mac_address for c in clients}
