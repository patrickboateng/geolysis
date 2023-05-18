import functools
from typing import Callable, Iterable, TypeVar, cast

import numpy as np

F = TypeVar("F", bound=Callable[..., float])


def deg2rad(*deg: Iterable) -> Callable[[F], F]:
    """A decorator that converts `deg` from degree to radians.

    Args:
        deg: registered keyword arguments to convert.

    Returns:
        A decorator.
    """

    def dec(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for key in deg:
                angle = kwargs[key]
                kwargs[key] = np.deg2rad(angle)
            return func(*args, **kwargs)

        return cast(F, wrapper)

    return dec
