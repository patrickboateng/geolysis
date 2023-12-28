from dataclasses import dataclass

from geolysis.exceptions import AllowableSettlementError


def _chk_settlement(actual_settlement: float, allowable_settlement: float):
    if actual_settlement > allowable_settlement:
        msg = f"Settlement: {actual_settlement} should be less than or equal \
                Allowable Settlement: {allowable_settlement}"
        raise AllowableSettlementError(msg)


@dataclass
class CircularFooting:
    """Circular Footing Size.

    :param float width:
        Diameter of foundation footing
    """

    width: float


@dataclass
class SquareFooting:
    """Square Footing Size.

    :param float width:
        Width of foundation footing
    """

    width: float


@dataclass
class RectangularFooting:
    """Rectangular Footing Size.

    :param float length:
        Length of foundation footing
    :param float width:
        Width of foundation footing
    """

    length: float
    width: float


@dataclass
class FoundationSize:
    """A simple class representing a foundation.

    :param float depth:
        Depth of foundation.
    :param footing_size:
        Represents the type of footing size i.e. :class:`SquareFooting`,
        :class:`RectangularFooting` or :class:`CircularFooting`
    :type footing_size: SquareFooting | RectangularFooting | CircularFooting
    """

    depth: float
    footing_size: SquareFooting | RectangularFooting | CircularFooting
