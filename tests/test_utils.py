import pytest

from pytleap.utils import normalize_mac


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("aa:bb:cc:dd:ee:ff", "aa:bb:cc:dd:ee:ff"),
        ("AA-BB-CC-DD-EE-FF", "aa:bb:cc:dd:ee:ff"),
        (None, None),
    ],
)
def test_normalize_mac(test_input, expected):
    assert normalize_mac(test_input) == expected
