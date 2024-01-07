from dataclasses import dataclass

from geolysis.utils import PI, round_


@dataclass
class CircularFooting:
    """Circular Footing Size.

    :param float width: Diameter of foundation footing (m)
    """

    width: float


@dataclass
class SquareFooting:
    """Square Footing Size.

    :param float width: Width of foundation footing (m)
    """

    width: float


@dataclass
class RectangularFooting:
    """Rectangular Footing Size.

    :param float length: Length of foundation footing (m)
    :param float width: Width of foundation footing (m)
    """

    length: float
    width: float


@dataclass
class FoundationSize:
    """A simple class representing a foundation.

    :param float depth: Depth of foundation (m)
    :param footing_size:Represents the type of footing size i.e. :class:`SquareFooting`,
        :class:`RectangularFooting` or :class:`CircularFooting`
    :type footing_size: SquareFooting | RectangularFooting | CircularFooting
    """

    depth: float
    footing_size: SquareFooting | RectangularFooting | CircularFooting
