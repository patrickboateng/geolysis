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
mean = statistics.fmean
isclose = math.isclose


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


def prod(*floats_or_ints) -> float:
    """Calculate the product of all the elements in the
    input iterable.

    The default start value for the product is 1.

    When the iterable is empty, return the start value.
    This function is intended specifically for use with
    numeric values and may reject non-numeric types.
    """
    return math.prod(floats_or_ints)


def round_(ndigits: Callable[..., float] | int) -> Callable:
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

    :Example:
        >>>

    :param Callable[..., float] | int precision:
        The number of decimal places to round to. It can be
        an integer or a function that returns a float.

    :return:
        A decorator that rounds the result of the wrapped
        function.
    :rtype:
        Callable[..., float]

    :raises TypeError:
        If precision is neither a function nor an integer.
    """

    def dec(
        func: Callable[..., float],
        /,
        *,
        ndigits: int = 2,
    ) -> Callable[..., float]:
        # The inner decorator function that returns the wrapper function that
        # performs the rounding.

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> float:
            return round(func(*args, **kwargs), ndigits=ndigits)

        return wrapper

    if callable(ndigits):
        return dec(ndigits)  # return wrapper

    if isinstance(ndigits, int):  # type: ignore
        return functools.partial(dec, ndigits=ndigits)  # return decorator

    msg = "precision should be a function to be decorated or an int."
    raise TypeError(msg)
