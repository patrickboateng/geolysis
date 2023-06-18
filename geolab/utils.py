import math


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


exp = math.exp
pi = math.pi


def mul(*args) -> float:
    """Calculate the product of all the elements in the input iterable.

    :return: The products of all elements in `args`
    :rtype: float
    """
    return math.prod(args)
