from dataclasses import dataclass

from geolysis.exceptions import AllowableSettlementError
from geolysis.utils import PI, round_


def _chk_settlement(actual_settlement: float, allowable_settlement: float):
    if actual_settlement > allowable_settlement:
        msg = f"Settlement: {actual_settlement} should be less than or equal \
                Allowable Settlement: {allowable_settlement}"
        raise AllowableSettlementError(msg)


@dataclass
class CircularFooting:
    """Circular Footing Size.

    :param float width: Diameter of foundation footing (m)
    """

    width: float

    @property
    @round_(ndigits=2)
    def area_of_footing(self):
        return PI * self.width**2 / 4


@dataclass
class SquareFooting:
    """Square Footing Size.

    :param float width: Width of foundation footing (m)
    """

    width: float

    @property
    @round_(ndigits=2)
    def area_of_footing(self):
        return self.width**2


@dataclass
class RectangularFooting:
    """Rectangular Footing Size.

    :param float length: Length of foundation footing (m)
    :param float width: Width of foundation footing (m)
    """

    length: float
    width: float

    @property
    @round_(ndigits=2)
    def area_of_footing(self):
        return self.length * self.width


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
