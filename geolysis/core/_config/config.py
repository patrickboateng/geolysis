import enum

import pint


class DecimalPlacesRegistry:
    DEFAULT_DECIMAL_PLACES = 4

    __slots__ = ("decimal_places",)

    def __init__(self):
        self.decimal_places = self.DEFAULT_DECIMAL_PLACES

    def reset(self) -> None:
        """Resets decimal places to the default value."""
        self.decimal_places = self.DEFAULT_DECIMAL_PLACES


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
