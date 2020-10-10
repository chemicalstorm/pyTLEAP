import os

from pytleap.utils import process_wlanconfig


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()


def test_parse_wlanconfig_ok():
    """Test that the output of `wlanconfig` parses correctly."""
    client_list = process_wlanconfig(load_fixture("wlanconfig_3clients.txt"))
    assert len(client_list) == 3
    assert {c.mac_address for c in client_list} == {
        "aa:bb:cc:dd:ee:ff",
        "ff:ee:dd:cc:bb:aa",
        "00:11:22:33:44:55",
    }


def test_bad_response_returns_empty():
    """Test that invalid output of `wlanconfig` does not generate any error."""
    assert process_wlanconfig("") == []
    assert process_wlanconfig("ERROR") == []
    assert process_wlanconfig(load_fixture("wlanconfig_empty.txt")) == []
