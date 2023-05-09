import functools
from typing import Callable, TypeVar, cast

import numpy as np

from .exceptions import FoundationTypeError, PIValueError, PSDValueError

VERSION = "0.1.0"


F = TypeVar("F", bound=Callable[[float], float])


def deg2rad(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        phi = kwargs["phi"]
        kwargs["phi"] = np.deg2rad(phi)

        return func(*args, **kwargs)
        # return func(np.deg2rad(phi))

    return cast(F, wrapper)


@deg2rad
def Kp(*, phi: float) -> float:
    r"""Coefficient of passive earth pressure ($K_p$).

    $$\dfrac{1 + \sin \phi}{1 - \sin \phi}$$

    Args:
        phi: Internal angle of friction (degrees).

    Returns:
        Passive earth pressure coefficient.

    """
    return (1 + np.sin(phi)) / (1 - np.sin(phi))
