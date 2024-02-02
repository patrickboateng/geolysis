from dataclasses import dataclass
from typing import TypeAlias

__all__ = [
    "CircularFooting",
    "SquareFooting",
    "RectangularFooting",
    "FoundationSize",
]


@dataclass
class CircularFooting:
    """
    Circular Footing Size.

    :param float width: Diameter of foundation footing. (m)
    """

    width: float


@dataclass
class SquareFooting:
    """
    Square Footing Size.

    :param float width: Width of foundation footing. (m)
    """

    width: float


@dataclass
class RectangularFooting:
    """
    Rectangular Footing Size.

    :param float length: Length of foundation footing. (m)
    :param float width: Width of foundation footing. (m)
    """

    length: float
    width: float


_FootingShape: TypeAlias = SquareFooting | RectangularFooting | CircularFooting


@dataclass
class FoundationSize:
    """
    A simple class representing a foundation structure.

    :param float depth: Depth of footing. (m)
    :param FootingShape footing_shape: Represents the shape of the footing.
    """

    depth: float
    footing_shape: _FootingShape

    @property
    def width(self):
        return self.footing_shape.width
