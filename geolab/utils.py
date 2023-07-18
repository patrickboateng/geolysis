import functools
import math
from typing import Callable, Union

from geolab import DECIMAL_PLACES

exp = math.exp
PI = math.pi


def deg2rad(x: float) -> float:
    return math.radians(x)


def rad2deg(x: float) -> float:
    return math.degrees(x)


def tan(x: float) -> float:
    return math.tan(deg2rad(x))


def sin(x: float) -> float:
    return math.sin(deg2rad(x))


def cos(x: float) -> float:
    return math.cos(deg2rad(x))


def arctan(x: float) -> float:
    return rad2deg(math.atan(x))


def log10(x: float) -> float:
    return math.log10(x)


def sqrt(x: float) -> float:
    return math.sqrt(x)


CallableOrPrecision = Union[Callable, int]


def round_(
    precision: CallableOrPrecision,
):
    def dec(func, /, *, precision=DECIMAL_PLACES):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return round(func(*args, **kwargs), ndigits=precision)

        return wrapper

    if callable(precision):
        return dec(precision)  # return wrapper

    if isinstance(precision, int):
        return functools.partial(dec, precision=precision)  # return decorator

    msg = "f should be a function or an int"
    raise TypeError(msg)


def mul(*args) -> float:
    """Calculate the product of all the elements in the input iterable."""
    return math.prod(args)
