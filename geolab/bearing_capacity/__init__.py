"""This module provides functions for bearing capacity analysis."""

import enum
from dataclasses import dataclass

from geolab import DECIMAL_PLACES


BearingCapacityFactors = dict[str, float]


@dataclass
class FootingSize:
    width: float
    length: float


@dataclass
class FoundationSize:
    footing_size: FootingSize
    depth: float


class FootingShape(enum.IntEnum):
    CIRCULAR_FOOTING = enum.auto()
    RECTANGULAR_FOOTING = enum.auto()
    SQUARE_FOOTING = enum.auto()
    STRIP_FOOTING = enum.auto()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


def depth_factor(foundation_depth: float, foundation_width: float) -> float:
    r"""Depth factor used in estimating the allowable bearing capacity of a soil.

    .. math::

        k = 1 + 0.33 \frac{D_f}{B}

    :param foundation_depth: Depth of foundation (m)
    :type foundation_depth: float
    :param foundation_width: Width of foundation (m)
    :type foundation_width: float
    :return: Depth factor
    :rtype: float
    """
    _depth_factor = 1 + 0.33 * (foundation_depth / foundation_width)
    return (
        round(_depth_factor, DECIMAL_PLACES) if _depth_factor <= 1.33 else 1.33
    )


def _check_footing_dimension(width, length):
    if (width is None) or (length is None):
        msg = "Foundation dimension cannot be None"
        raise ValueError(msg)


def _check_footing_shape(footing_shape):
    if not isinstance(footing_shape, FootingShape):
        msg = f"Available foundation shapes are {','.join(list(FootingShape))}"
        raise TypeError(msg)
