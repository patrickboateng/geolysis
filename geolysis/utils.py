import functools
import math
from math import ceil, exp, isclose, log10
from math import pi as PI
from math import sqrt
from statistics import fmean as mean
from typing import Callable, TypeAlias

from typing_extensions import SupportsFloat, SupportsIndex

_SupportsFloatOrIndex: TypeAlias = SupportsFloat | SupportsIndex


def deg2rad(__x: _SupportsFloatOrIndex, /) -> float:
    """
    Convert angle x from degrees to radians.
    """
    return math.radians(__x)


def rad2deg(__x: _SupportsFloatOrIndex, /) -> float:
    """
    Convert angle x from radians to degrees.
    """
    return math.degrees(__x)


def tan(__x: _SupportsFloatOrIndex, /) -> float:
    """
    Return the tangent of x (measured in degrees).
    """
    return math.tan(deg2rad(__x))


def cot(__x: _SupportsFloatOrIndex, /) -> float:
    """
    Return the cotangent of x (measured in degrees).
    """
    return 1 / tan(__x)


def sin(__x: _SupportsFloatOrIndex, /) -> float:
    """
    Return the sine of x (measured in degrees).
    """
    return math.sin(deg2rad(__x))


def cos(__x: _SupportsFloatOrIndex, /) -> float:
    """
    Return the cosine of x (measured in degrees).
    """
    return math.cos(deg2rad(__x))


def arctan(__x: _SupportsFloatOrIndex, /) -> float:
    """
    Return the arc tangent (measured in degrees) of x.
    """
    return rad2deg(math.atan(__x))


def round_(ndigits: int) -> Callable:
    """
    A decorator that rounds the result of a function to a specified number of
    decimal places.

    :param int ndigits: The number of decimal places to round to.

    :return: A decorator that rounds the result of the wrapped function.
    :rtype: Callable[..., float]

    :raises TypeError: If precision is not an int.

    .. note::

        This decorator can only be used with functions that return a float or a
        datatype that implements ``__round__``.
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

    if isinstance(ndigits, int):
        return functools.partial(dec, ndigits=ndigits)  # return decorator

    err_msg = "ndigits should be an int."
    raise TypeError(err_msg)
