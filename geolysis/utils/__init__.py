import enum
import functools
from typing import Callable

from func_validator import ValidationError

from .math import *
from . import math as m

__all__ = ["AbstractStrEnum", "ValidationError", "add_repr", "round_"] + m.__all__


class StrEnumMeta(enum.EnumMeta):
    def __contains__(cls, item) -> bool:
        if isinstance(item, (str, cls)):
            return str(item) in (member.value for member in cls)
        return NotImplemented

    def __repr__(cls) -> str:
        return str([member.value for member in cls])


class AbstractStrEnum(enum.StrEnum, metaclass=StrEnumMeta):
    """An abstract string enumeration class that inherits from StrEnum.

    This class can be used as a base class for creating string
    enumerations.
    """


def add_repr(cls):
    """A class decorator that adds a __repr__ method to the class."""

    def __repr__(self) -> str:
        inst_attrs = self.__dict__
        attrs = (f"{key.strip('_')}={val}" for key, val in inst_attrs.items())
        return f"{type(self).__name__}({', '.join(attrs)})"

    def __str__(self) -> str:
        return repr(self)

    cls.__repr__ = __repr__
    cls.__str__ = __str__

    return cls


def round_(ndigits: int) -> Callable:
    """A decorator that rounds the result of a callable to a specified
    number of decimal places.

    The returned value of the callable should support the `__round__`
    dunder method and should be a numeric value.

    TypeError is raised when `ndigits` is not an int.
    """

    if not isinstance(ndigits, int):
        raise TypeError("ndigits must be an int")

    def dec(fn) -> Callable[..., float]:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs) -> float:
            res = fn(*args, **kwargs)
            return round(res, ndigits=ndigits)

        return wrapper

    return dec
