import enum

import pint


class DecimalPlacesRegistry:
    _DEFAULT = 4

    __slots__ = ("DECIMAL_PLACES",)

    def __init__(self):
        self.DECIMAL_PLACES = self._DEFAULT

    def reset(self) -> None:
        """Resets decimal places to the default value."""
        self.DECIMAL_PLACES = self._DEFAULT


class CustomQuantity(pint.UnitRegistry.Quantity):
    pass


class CustomUnit(pint.UnitRegistry.Unit):
    pass


class UnitRegistry(
    pint.registry.GenericUnitRegistry[CustomQuantity, CustomUnit]
):
    Quantity = CustomQuantity
    Unit = CustomUnit


class UnitSystem(enum.StrEnum):
    CGS = "cgs"
    MKS = "mks"
    BRITISH_IMPERIAL = "imperial"
    US_IMPERIAL = "US"
    SI = "SI"


DecimalPlacesReg = DecimalPlacesRegistry()
UnitReg = UnitRegistry(system=UnitSystem.SI, cache_folder=":auto:")
Quantity = UnitReg.Quantity
