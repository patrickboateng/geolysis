import functools
import math
from math import exp, isclose, log, log10, pi, sqrt
from statistics import fmean
from typing import Callable

from geolysis.constants import DECIMAL_PLACES

__all__ = [
    "deg2rad",
    "rad2deg",
    "tan",
    "cot",
    "sin",
    "cos",
    "arctan",
    "round_",
]

PI = pi

mean = fmean


def deg2rad(__x: float, /) -> float:
    """Convert angle x from degrees to radians."""
    return math.radians(__x)


def rad2deg(__x: float, /) -> float:
    """Convert angle x from radians to degrees."""
    return math.degrees(__x)


def tan(__x: float, /) -> float:
    """Return the tangent of x (measured in degrees)."""
    return math.tan(deg2rad(__x))


def cot(__x: float, /) -> float:
    """Return the cotangent of x (measured in degrees)."""
    return 1 / tan(__x)


def sin(__x: float, /) -> float:
    """Return the sine of x (measured in degrees)."""
    return math.sin(deg2rad(__x))


def cos(__x: float, /) -> float:
    """Return the cosine of x (measured in degrees)."""
    return math.cos(deg2rad(__x))


def arctan(__x: float, /) -> float:
    """Return the arc tangent (measured in degrees) of x."""
    return rad2deg(math.atan(__x))


def round_(ndigits: int | Callable) -> Callable:
    """A decorator that rounds the result of a callable to a specified number
    of decimal places.

    The returned value of the callable shoud support the ``__round__`` dunder
    method and should be a numeric value. ``ndigits`` can either be an int
    which will indicates the number of decimal places to round to or a callable,
    which by default rounds the returned value to 4 decimal places.

    TypeError is raised when ``ndigits`` is neither an int or a callable.

    Examples
    --------
    >>> @round_(ndigits=2)
    ... def area_of_circle(radius: float):
    ...   return PI * (radius ** 2)

    >>> area_of_circle(radius=2.0)
    12.57

    By default the function is rounded to 4 decimal places.

    >>> @round_
    ... def area_of_circle(radius: float):
    ...   return PI * (radius ** 2)

    >>> area_of_circle(radius=2.0)
    12.5664

    >>> @round_(ndigits=2.0)
    ... def area_of_square(width: float):
    ...   return width ** 2
    Traceback (most recent call last):
        ...
    TypeError: ndigits should be an int or a callable.
    """

    def dec(
        func: Callable[..., float],
        ndigits: int = DECIMAL_PLACES,
    ) -> Callable[..., float]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> float:
            return round(func(*args, **kwargs), ndigits=ndigits)

        return wrapper

    # See if we're being called as @round_ or @round_().
    if isinstance(ndigits, int):
        # We're called with parens.
        return functools.partial(dec, ndigits=ndigits)
    if callable(ndigits):
        # We're called as @round_ without parens.
        f = ndigits
        return dec(f)
    else:
        err_msg = "ndigits should be an int or a callable."
        raise TypeError(err_msg)
