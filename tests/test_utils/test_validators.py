import pytest
from geolysis.utils.validators import le, lt, eq, ne


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
        _val = c.foo + 22.0
        c.foo = _val


def test_lt():
    class C:

        def __init__(self, foo):
            self.foo = foo

        @property
        def foo(self):
            return self._foo

        @foo.setter
        @lt(25.4)
        def foo(self, val):
            self._foo = val

    c = C(22.0)

    with pytest.raises(ValueError):
        _val = c.foo + 22.0
        c.foo = _val


def test_eq():
    class C:

        def __init__(self, foo):
            self.foo = foo

        @property
        def foo(self):
            return self._foo

        @foo.setter
        @eq(22)
        def foo(self, val):
            self._foo = val

    c = C(22)

    with pytest.raises(ValueError):
        _val = c.foo
        c.foo = _val + 22


def test_ne():
    class C:

        def __init__(self, foo):
            self.foo = foo

        @property
        def foo(self):
            return self._foo

        @foo.setter
        @ne(22)
        def foo(self, val):
            self._foo = val

    c = C(28)

    with pytest.raises(ValueError):
        _val = c.foo  # Just to make the getter for foo run
        c.foo = 22
