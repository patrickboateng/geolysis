import enum
import functools
from typing import Callable

from .math import *
from . import math as m

__all__ = ["AbstractStrEnum", "round_"] + m.__all__


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
