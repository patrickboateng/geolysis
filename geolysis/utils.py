import functools
import math
from typing import Callable, SupportsRound
from math import exp, isclose, log10, sqrt, inf, pi
from statistics import fmean as mean

__all__ = ["inf", "pi", "deg2rad", "rad2deg", "tan", "cot", "sin", "cos",
           "arctan", "round_", "mean", "exp", "isclose", "log10", "sqrt"]


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


def round_(ndigits: int | Callable[..., SupportsRound]) -> Callable:
    """A decorator that rounds the result of a callable to a specified number
    of decimal places.

    The returned value of the callable shoud support the ``__round__`` dunder
    method and should be a numeric value. ``ndigits`` can either be an int
    which will indicates the number of decimal places to round to or a
    callable. If ``ndigits`` is callable the default decimal places is 4.

    TypeError is raised when ``ndigits`` is neither an int nor a callable.
    """

    default = 2

    def dec(fn) -> Callable[..., float]:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs) -> float:
            if not callable(ndigits):
                dp = ndigits
            else:
                # Default decimal places is 2.
                dp = default
            res = fn(*args, **kwargs)
            return round(res, ndigits=dp)

        return wrapper

    # See if we're being called as @round_ or @round_().
    if isinstance(ndigits, int):
        # We're called with parens.
        return dec
    if callable(ndigits):
        # We're called as @round_ without parens.
        return dec(ndigits)

    raise TypeError("ndigits should be an int or a callable.")
