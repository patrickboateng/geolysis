from geolysis.exceptions import AllowableSettlementError


def check_settlement(actual_settlement: float, allowable_settlement: float):
    if actual_settlement > allowable_settlement:
        msg = f"Settlement: {actual_settlement} should be less than or equal \
                Allowable Settlement: {allowable_settlement}"
        raise AllowableSettlementError(msg)


class CircularFooting:
    def __init__(self, diameter: float) -> None:
        self.diameter = diameter


class SquareFooting:
    def __init__(self, width: float) -> None:
        self.width = width


class RectangularFooting:
    def __init__(self, length: float, width: float) -> None:
        self.length = length
        self.width = width


class FoundationSize:
    def __init__(
        self,
        depth: float,
        footing_size: SquareFooting | RectangularFooting | CircularFooting,
    ):
        self.depth = depth
        self.footing_size = footing_size
