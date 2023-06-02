import functools
import math
import re
from typing import Callable, Iterable, TypeVar, Union, cast

import numpy as np


tan = np.tan
sin = np.sin
cos = np.cos
exp = np.exp
pi = np.pi

F = TypeVar("F", bound=Callable[..., float])


def update_kwargs(key, kwargs):
    kwargs[key] = np.deg2rad(kwargs[key])
    return kwargs


def deg2rad(*deg: Union[Iterable, Callable]) -> Callable[[F], F]:
    """A decorator that converts ``deg`` from degree to radians.

    :raises TypeError: raised when ``deg`` is not a valid type
    :return: a decorator or a decorated wrapper
    :rtype: Callable[[F], F]
    """

    if not deg:
        raise TypeError("deg should be a non-empty tuple")

    if callable(deg[0]):
        func = deg[0]

        @functools.wraps(func)
        def regex_wrapper(*args, **kwargs):
            keys = kwargs.keys()
            regex_pattern = re.compile(r"\w*angle\w*", re.IGNORECASE)
            for key in keys:
                match_pattern = regex_pattern.search(key)
                if match_pattern is None:
                    continue
                kwargs = update_kwargs(key, kwargs)
            return func(*args, **kwargs)

        return regex_wrapper

    # If actual arguments were passed to the function
    def dec(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for key in deg:
                kwargs = update_kwargs(key, kwargs)
            return func(*args, **kwargs)

        return cast(F, wrapper)

    return dec


def product(*args) -> float:
    """Calculate the product of all the elements in the input iterable.

    :return: The products of all elements in `args`
    :rtype: float
    """
    return math.prod(args)
