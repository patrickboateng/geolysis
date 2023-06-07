import math

import numpy as np


exp = np.exp
pi = np.pi


def tan(x: float):
    return np.tan(np.deg2rad(x))


def sin(x: float):
    return np.sin(np.deg2rad(x))


def cos(x: float):
    return np.cos(np.deg2rad(x))


def product(*args) -> float:
    """Calculate the product of all the elements in the input iterable.

    :return: The products of all elements in `args`
    :rtype: float
    """
    return math.prod(args)
