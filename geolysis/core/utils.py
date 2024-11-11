import functools
import math
from math import exp, isclose, log10, sqrt
from math import inf as INF
from math import pi as PI
from statistics import fmean as mean
from typing import (
    Callable,
    Final,
    Optional,
    SupportsRound,
)

from geolysis.core._config.config import DecimalPlacesReg, Quantity

__all__ = [
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
    """A decorator that rounds the result of a callable to a specified number of
    decimal places.

    The returned value of the callable shoud support the ``__round__`` dunder
    method and should be a numeric value. ``ndigits`` can either be an int which
    will indicates the number of decimal places to round to or a callable. If
    ``ndigits`` is callable the default decimal places is 4.

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
                dp = DecimalPlacesReg.DECIMAL_PLACES
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

    raise TypeError("ndigits should be an int or a callable.")


def quantity(unit):
    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return (
                Quantity(fn(*args, **kwargs), unit)
                .to_base_units()
                .to_compact()
            )

        return wrapper

    return decorator


def field(*, attr: str, obj: Optional[str] = None, doc: Optional[str] = None):
    """A field that reference another field."""
    return _Attribute(attr=attr, obj=obj, doc=doc)


class _Attribute:
    def __init__(
        self,
        *,
        attr: str,
        obj: Optional[str] = None,
        doc: Optional[str] = None,
    ):
        self.ref_attr = attr
        self.ref_obj = obj
        self.fget: Final = getattr
        self.fset: Final = setattr
        self.fdel: Final = delattr
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if self.ref_obj is not None:
            ref_obj = self.fget(obj, self.ref_obj)
            return self.fget(ref_obj, self.ref_attr)
        return self.fget(obj, self.ref_attr)

    def __set__(self, obj, value) -> None:
        if self.ref_obj is not None:
            ref_obj = self.fget(obj, self.ref_obj)
            self.fset(ref_obj, self.ref_attr, value)
        else:
            self.fset(obj, self.ref_attr, value)

    #: TODO: check deleter
    def __delete__(self, obj) -> None:
        self.fdel(obj, self.property_name)

    def __set_name__(self, objtype, property_name) -> None:
        self.property_name = property_name
