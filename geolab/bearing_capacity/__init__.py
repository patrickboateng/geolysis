"""This module provides functions for bearing capacity analysis."""

import enum
from abc import ABC, abstractproperty
from dataclasses import dataclass

from geolab.utils import mul, round_


class SoilProperties:
    cohesion: float
    soil_unit_weight: float


@dataclass(slots=True)
class FootingSize:
    width: float
    length: float


@dataclass(slots=True)
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


class BearingCapacity(ABC):
    def __init__(
        self,
        cohesion: float,
        soil_unit_weight: float,
        foundation_size: FoundationSize,
        friction_angle: float,
        beta: float,
        footing_shape: FootingShape = FootingShape.SQUARE_FOOTING,
    ) -> None:
        _check_footing_shape(footing_shape)

        self.cohesion = cohesion
        self.soil_unit_weight = soil_unit_weight
        self.foundation_size = foundation_size
        self.friction_angle = friction_angle
        self.beta = beta
        self.footing_shape = footing_shape

    @round_
    def ultimate_bearing_capacity(self) -> float:
        expr_1 = mul(self.cohesion, self.nc, self.sc, self.dc, self.ic)
        expr_2 = mul(
            self.soil_unit_weight,
            self.foundation_size.depth,
            self.nq,
            self.sq,
            self.dq,
            self.iq,
        )
        expr_3 = mul(
            self.soil_unit_weight,
            self.foundation_size.footing_size.width,
            self.ngamma,
            self.sgamma,
            self.dgamma,
            self.igamma,
        )
        return expr_1 + expr_2 + (0.5 * expr_3)

    @abstractproperty
    def nc(self):
        ...

    @abstractproperty
    def nq(self):
        ...

    @abstractproperty
    def ngamma(self):
        ...

    @abstractproperty
    def dc(self):
        ...

    @abstractproperty
    def dq(self):
        ...

    @abstractproperty
    def dgamma(self):
        ...

    @abstractproperty
    def sc(self):
        ...

    @abstractproperty
    def sq(self):
        ...

    @abstractproperty
    def sgamma(self):
        ...

    @abstractproperty
    def ic(self):
        ...

    @abstractproperty
    def iq(self):
        ...

    @abstractproperty
    def igamma(self):
        ...


@dataclass(slots=True)
class BearingCapacityFactors:
    nc: float
    nq: float
    ngamma: float


@round_
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
    return min(_depth_factor, 1.33)


def _check_footing_dimension(width, length):
    if (width is None) or (length is None):
        msg = "Foundation dimension cannot be None"
        raise ValueError(msg)


def _check_footing_shape(footing_shape):
    if not isinstance(footing_shape, FootingShape):
        msg = f"Available foundation shapes are {','.join(list(FootingShape))}"
        raise TypeError(msg)
