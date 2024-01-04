"""
.. currentmodule:: geolab.utils

======================================
Utility Function (:mod:`geolab.utils`)
======================================

.. autosummary:: 

    exp
    deg2rad
    rad2deg
    tan
    sin
    cos
    arctan
    log10
    sqrt
    prod
    round_

.. autodecorator:: round_

"""

import functools
import math
import statistics
from typing import Callable

PI = math.pi
exp = math.exp
isclose = math.isclose
mean = statistics.fmean


def deg2rad(x: float | int, /) -> float:
    """Convert angle x from degrees to radians."""
    return math.radians(x)


def rad2deg(x: float | int, /) -> float:
    """Convert angle x from radians to degrees."""
    return math.degrees(x)


def tan(x: float | int, /) -> float:
    """Return the tangent of x (measured in degrees)."""
    return math.tan(deg2rad(x))


def cot(x: float | int, /) -> float:
    """Return the cotangent of x (measured in degrees)."""
    return 1 / tan(x)


def sin(x: float | int, /) -> float:
    """Return the sine of x (measured in degrees)."""
    return math.sin(deg2rad(x))


def cos(x: float | int, /) -> float:
    """Return the cosine of x (measured in degrees)."""
    return math.cos(deg2rad(x))


def arctan(x: float | int, /) -> float:
    """Return the arc tangent (measured in degrees) of x."""
    return rad2deg(math.atan(x))


def log10(x: float | int, /) -> float:
    """Return the base 10 logarithm of x."""
    return math.log10(x)


def sqrt(x: float | int, /) -> float:
    """Return the square root of x."""
    return math.sqrt(x)


def round_(ndigits: int) -> Callable:
    """A decorator that rounds the result of a function to
    a specified number of decimal places.

    This decorator can be used with functions that return
    a float.

    .. code::

        from math import pi

        from geolab.utils import round_

        @round_(precision=3)
        def area_of_circle(radius: float) -> float:
            return pi * radius**2

        # area_of_circle will return a value rounded to 3 d.p

    :param int ndigits:
        The number of decimal places to round to. It can be
        an integer or a function that returns a float.

    :return:
        A decorator that rounds the result of the wrapped
        function.
    :rtype: Callable[..., float]

    :raises TypeError: If precision is not an integer.
    """

    def dec(
        func: Callable[..., float],
        /,
        *,
        ndigits: int,
    ) -> Callable[..., float]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> float:
            return round(func(*args, **kwargs), ndigits=ndigits)

        return wrapper

    if isinstance(ndigits, int):  # type: ignore
        return functools.partial(dec, ndigits=ndigits)  # return decorator

    msg = "ndigits should be an int."
    raise TypeError(msg)
