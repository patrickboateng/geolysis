import functools
import math
from enum import StrEnum
from math import exp, inf, isclose, log10, pi, sqrt
from statistics import fmean as mean
from typing import Callable

__all__ = [
    "AbstractStrEnum",
    "inf",
    "pi",
    "deg2rad",
    "rad2deg",
    "tan",
    "cot",
    "sin",
    "cos",
    "arctan",
    "round_",
    "mean",
    "exp",
    "isclose",
    "log10",
    "sqrt",
]


class AbstractStrEnum(StrEnum):
    """An abstract string enumeration class that inherits from StrEnum.

    This class can be used as a base class for creating string enumerations.
    """

    # def __contains__(self, item: str) -> bool:
    #     return item.casefold() in (member.value for member in self.__class__)

    def __repr__(self):
        return f"{self.value}"

    def __contains__(self, item):
        return item in (member.value for member in self.__class__)


def deg2rad(x: float, /) -> float:
    """Convert angle x from degrees to radians."""
    return math.radians(x)


def rad2deg(x: float, /) -> float:
    """Convert angle x from radians to degrees."""
    return math.degrees(x)


def tan(x: float, /) -> float:
    """Return the tangent of x (measured in degrees)."""
    return math.tan(deg2rad(x))


def cot(x: float, /) -> float:
    """Return the cotangent of x (measured in degrees)."""
    return 1 / tan(x)


def sin(x: float, /) -> float:
    """Return the sine of x (measured in degrees)."""
    return math.sin(deg2rad(x))


def cos(x: float, /) -> float:
    """Return the cosine of x (measured in degrees)."""
    return math.cos(deg2rad(x))


def arctan(x: float, /) -> float:
    """Return the arc tangent (measured in degrees) of x."""
    return rad2deg(math.atan(x))


def round_(ndigits: int) -> Callable:
    """A decorator that rounds the result of a callable to a specified number
    of decimal places.

    The returned value of the callable should support the ``__round__`` dunder
    method and should be a numeric value.

    TypeError is raised when ``ndigits`` is not an int.
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
