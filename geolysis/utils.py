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
from typing import Any, Callable

from geolysis import DECIMAL_PLACES

PI = math.pi
exp = math.exp
mean = statistics.mean
isclose = math.isclose


def deg2rad(x: float, /) -> float:
    """Convert angle x from degrees to radians."""
    return math.radians(x)


def rad2deg(x: float, /) -> float:
    """Convert angle x from radians to degrees."""
    return math.degrees(x)


def tan(x: float, /) -> float:
    """Return the tangent of x (measured in degrees)."""
    return math.tan(deg2rad(x))


def sin(x: float, /) -> float:
    """Return the sine of x (measured in degrees)."""
    return math.sin(deg2rad(x))


def cos(x: float, /) -> float:
    """Return the cosine of x (measured in degrees)."""
    return math.cos(deg2rad(x))


def arctan(x: float, /) -> float:
    """Return the arc tangent (measured in degrees) of x."""
    return rad2deg(math.atan(x))


def log10(x: float, /) -> float:
    """Return the base 10 logarithm of x."""
    return math.log10(x)


def sqrt(x: float, /) -> float:
    """Return the square root of x."""
    return math.sqrt(x)


def prod(*args: float | int) -> float:
    """Calculate the product of all the elements in the input iterable.

    The default start value for the product is 1.

    When the iterable is empty, return the start value. This function is
    intended specifically for use with numeric values and may reject non-
    numeric types.
    """
    return math.prod(args)


def round_(precision: Callable[..., float] | int) -> Callable:
    """A decorator that rounds the result of a function to a specified number
    of decimal places.

    This decorator can be used with functions that return a float.

    .. code::

        from math import pi

        from geolab.utils import round_

        @round_(precision=3)
        def area_of_circle(radius: float) -> float:
            return pi * radius**2


    :param precision: The number of decimal places to round to. It can be an
                      integer or a function that returns a float.
    :type precision: Callable[..., float] | int

    :return: A decorator that rounds the result of the wrapped function.
    :rtype: Callable[..., float]

    :raises TypeError: If precision is neither a function nor an integer.
    """

    def dec(
        func: Callable[..., float],
        /,
        *,
        precision: int = DECIMAL_PLACES,
    ) -> Callable[..., float]:
        # The inner decorator function that returns the wrapper function that
        # performs the rounding.

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> float:
            return round(func(*args, **kwargs), ndigits=precision)

        return wrapper

    if callable(precision):
        return dec(precision)  # return wrapper

    if isinstance(precision, int):  # type: ignore
        return functools.partial(dec, precision=precision)  # return decorator

    msg = "precision should be a function to be decorated or an int."
    raise TypeError(msg)
