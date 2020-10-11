import json

import pytest

from pytleap import Client

from .common import load_fixture


@pytest.fixture
def clients():
    c = load_fixture("status.client.user_good.json")
    client_json = json.loads(c)
    return [Client(c) for c in client_json["data"]]


def test_parse_data(clients):
    assert len(clients) == 4
    assert {
        ("11:22:33:44:55:66", "112233445566"),
        ("00:aa:11:bb:33:cc", None),
        ("ff:11:ee:22:dd:33", "A-True-Hostname"),
        ("ff:55:ee:44:dd:33", "K9"),
    } == {(c.mac_address, c.hostname) for c in clients}
