import pytest
from ucs_aashto.ucs_aashto import foo, bar, baz


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (2, 4),
        (3, 9),
        (100, 10000),
        (1.2, 1.44),
        (-1, 1),
        (-2, 4),
        (-50, 2500),
    ],
)
def test_foo(test_input, expected):
    assert foo(test_input) == expected
