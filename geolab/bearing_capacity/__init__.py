"""This module provides functions for bearing capacity analysis."""

from abc import ABC, abstractmethod

import numpy as np

from geolab import DECIMAL_PLACES


class BCF(ABC):
    @abstractmethod
    def nq(self):
        ...

    @abstractmethod
    def nc(self):
        ...

    @abstractmethod
    def ngamma(self):
        ...


def depth_factor(foundation_depth: float, foundation_width: float) -> float:
    """Depth factor used in estimating the allowable bearing capacity of a soil.

    .. math::

        $$k = 1 + 0.33 \\frac{D_f}{B}$$

    :param foundation_depth: Depth of foundation (m)
    :type foundation_depth: float
    :param foundation_width: Width of foundation (m)
    :type foundation_width: float
    :return: Depth factor
    :rtype: float
    """
    _depth_factor = 1 + 0.33 * (foundation_depth / foundation_width)
    return np.round(_depth_factor, DECIMAL_PLACES) if _depth_factor <= 1.33 else 1.33
