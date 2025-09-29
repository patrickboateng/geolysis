import math
from math import exp, inf, isclose, log10, pi, sqrt, isinf, atan
from statistics import fmean as mean

__all__ = [
    "atan",
    "inf",
    "isinf",
    "pi",
    "deg2rad",
    "rad2deg",
    "tandeg",
    "cotdeg",
    "sindeg",
    "cosdeg",
    "arctandeg",
    "mean",
    "exp",
    "isclose",
    "log10",
    "sqrt",
]


def deg2rad(x: float, /) -> float:
    """Convert angle x from degrees to radians."""
    return math.radians(x)


def rad2deg(x: float, /) -> float:
    """Convert angle x from radians to degrees."""
    return math.degrees(x)


def tandeg(x: float, /) -> float:
    """Return the tangent of x (measured in degrees)."""
    return math.tan(deg2rad(x))


def cotdeg(x: float, /) -> float:
    """Return the cotangent of x (measured in degrees)."""
    return 1 / tandeg(x)


def sindeg(x: float, /) -> float:
    """Return the sine of x (measured in degrees)."""
    return math.sin(deg2rad(x))


def cosdeg(x: float, /) -> float:
    """Return the cosine of x (measured in degrees)."""
    return math.cos(deg2rad(x))


def arctandeg(x: float, /) -> float:
    """Return the arc tangent (measured in degrees) of x."""
    return rad2deg(math.atan(x))
