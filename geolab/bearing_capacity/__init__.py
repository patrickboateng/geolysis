"""This module provides functions for bearing capacity analysis."""

import enum
from dataclasses import dataclass


@dataclass(slots=True)
class FootingSize:
    width: float
    length: float


@dataclass(slots=True)
class FoundationSize:
    footing_size: FootingSize
    depth: float

    @property
    def width(self) -> float:
        return self.footing_size.width

    @property
    def length(self) -> float:
        return self.footing_size.length

    @property
    def depth_2_width_ratio(self) -> float:
        return self.depth / self.width


class FootingShape(enum.IntEnum):
    CIRCULAR = enum.auto()
    RECTANGULAR = enum.auto()
    SQUARE = enum.auto()
    STRIP = enum.auto()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"
