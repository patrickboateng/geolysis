import enum

from pint import UnitRegistry


UNIT_REGISTRY = UnitRegistry()
Q_ = UNIT_REGISTRY.Quantity


class UnitSystem(enum.StrEnum):
    """Physical unit systems."""

    CGS = "cgs"
    MKS = "mks"
    IMPERIAL = "imperial"
    SI = "SI"

    @property
    def Pressure(self):
        match self:
            case self.CGS:
                unit = "barye"
            case self.MKS | self.SI:
                unit = "kN/m**2"
            case self.IMPERIAL:
                unit = "psi"
            case _:
                unit = ""
        return unit
