import functools
import math
import statistics
from typing import Callable, Iterable, SupportsRound

from geolysis.core._conf import Q_, UnitSystem, get_option

__all__ = [
    "exp",
    "log10",
    "sqrt",
    "mean",
    "deg2rad",
    "rad2deg",
    "tan",
    "cot",
    "sin",
    "cos",
    "arctan",
    "round_",
    "quantity",
]

PI = math.pi
INF = math.inf


isclose = math.isclose


def exp(x: float, /) -> float:
    """Return e to the power of x"""
    return math.exp(x)


def log10(x: float, /) -> float:
    """Return the base 10 logarithm of x."""
    return math.log10(x)


def sqrt(x: float, /) -> float:
    """Return the square root of x."""
    return math.sqrt(x)


def mean(data: Iterable[float]) -> float:
    """Compute the arithmetic mean of data."""
    return statistics.fmean(data=data)


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
    """A decorator that rounds the result of a callable to a specified
    number of decimal places.

    The returned value of the callable shoud support the ``__round__``
    dunder method and should be a numeric value. ``ndigits`` can either
    be an int which will indicates the number of decimal places to round
    to or a callable. If ``ndigits`` is callable the default decimal
    places is 4.

    TypeError is raised when ``ndigits`` is neither an int or a callable.

    Examples
    --------
    >>> @round_(ndigits=2)
    ... def area_of_circle(radius: float):
    ...     return PI * (radius**2)

    >>> area_of_circle(radius=2.0)
    12.57

    By default the function is rounded to 4 decimal places.

    >>> @round_
    ... def area_of_circle(radius: float):
    ...     return PI * (radius**2)

    >>> area_of_circle(radius=2.0)
    12.5664

    >>> @round_(ndigits=2.0)
    ... def area_of_square(width: float):
    ...     return width**2
    Traceback (most recent call last):
        ...
    TypeError: ndigits should be an int or a callable.
    """

    def dec(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs) -> float:
            if not callable(ndigits):
                dp = ndigits
            else:
                dp = get_option("dp")

            res = fn(*args, **kwargs)
            return round(res, ndigits=dp)

        return wrapper

    # See if we're being called as @round_ or @round_().
    if isinstance(ndigits, int):
        # We're called with parens.
        return dec
    if callable(ndigits):
        # We're called as @round_ without parens.
        f = ndigits
        return dec(f)

    err_msg = "ndigits should be an int or a callable."
    raise TypeError(err_msg)


def quantity(quant: str):
    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            default_unit = getattr(UnitSystem.SI, quant)
            unit_system = get_option("unit_system")
            preffered_unit = getattr(unit_system, quant)
            ret = fn(*args, **kwargs)
            return Q_(ret, default_unit).to_compact(preffered_unit)

        return wrapper

    return decorator
