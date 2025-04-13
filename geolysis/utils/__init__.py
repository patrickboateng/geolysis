import functools
import math
from math import exp, inf, isclose, log10, pi, sqrt
from statistics import fmean as mean
from typing import (Any, Callable, NotRequired, Optional, SupportsRound,
                    TypedDict, Unpack)

from . import validators

__all__ = ["ErrorMsg",
           "enum_repr",
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
           "validators"]


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


def enum_repr(cls):
    cls.__repr__ = lambda self: f"{self.value}"
    return cls


def round_(ndigits: int | Callable[..., SupportsRound]) -> Callable:
    """A decorator that rounds the result of a callable to a specified number
    of decimal places.

    The returned value of the callable should support the ``__round__`` dunder
    method and should be a numeric value. ``ndigits`` can either be an int
    which will indicate the number of decimal places to round to or a
    callable. If ``ndigits`` is callable the default decimal places is 2.

    TypeError is raised when ``ndigits`` is neither an int nor a callable.
    """

    def dec(fn) -> Callable[..., float]:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs) -> float:
            res = fn(*args, **kwargs)
            return round(res, ndigits=ndigits)

        return wrapper

    return dec
