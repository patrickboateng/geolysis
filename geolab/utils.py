import math

import numpy as np


exp = np.exp
pi = np.pi


deg2rad = lambda x: np.deg2rad(x)

rad2deg = lambda x: np.rad2deg(x)

tan = lambda x: np.tan(deg2rad(x))

sin = lambda x: np.sin(deg2rad(x))

cos = lambda x: np.cos(deg2rad(x))


def product(*args) -> float:
    """Calculate the product of all the elements in the input iterable.

    :return: The products of all elements in `args`
    :rtype: float
    """
    return math.prod(args)
