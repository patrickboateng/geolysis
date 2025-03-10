import pytest
from geolysis.utils.validators import le


def test_le():
    class C:

        def __init__(self, foo):
            self.foo = foo

        @property
        def foo(self):
            return self._foo

        @foo.setter
        @le(25.4)
        def foo(self, val):
            self._foo = val

    c = C(22.0)

    with pytest.raises(ValueError):
        foo = c.foo + 22.0
        c.foo = foo
