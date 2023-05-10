import functools

import numpy as np

from .exceptions import FoundationTypeError, PIValueError, PSDValueError

VERSION = "0.1.0"


def deg2rad(*deg):
    def dec(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for key in deg:
                angle = kwargs[key]
                kwargs[key] = np.deg2rad(angle)
            return func(*args, **kwargs)

        return wrapper

    return dec


@deg2rad("phi")
def Kp(*, phi: float) -> float:
    r"""Coefficient of passive earth pressure ($K_p$).

    $$\dfrac{1 + \sin \phi}{1 - \sin \phi}$$

    Args:
        phi: Internal angle of friction (degrees).

    Returns:
        Passive earth pressure coefficient.

    """
    return (1 + np.sin(phi)) / (1 - np.sin(phi))
