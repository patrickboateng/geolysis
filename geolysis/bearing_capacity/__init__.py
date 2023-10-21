"""This module provides functions for bearing capacity analysis."""

import enum
from dataclasses import dataclass, field


@dataclass(slots=True)
class FootingSize:
    width: float
    length: float

    @property
    def w2l(self) -> float:
        return self.width / self.length


@dataclass(slots=True)
class FoundationSize:
    width: float
    length: float
    depth: float
    footing_size: FootingSize = field(init=False, repr=False)

    def __post_init__(self):
        self.footing_size = FootingSize(self.width, self.length)

    @property
    def d2w(self) -> float:
        return self.depth / self.width

    @property
    def w2l(self) -> float:
        return self.width / self.length


class FootingShape(enum.IntFlag):
    CIRCULAR = 1
    RECTANGULAR = 2
    SQUARE = 4
    STRIP = 8

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"
