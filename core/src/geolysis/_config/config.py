import enum

import pint


class UnitSystem(enum.StrEnum):
    CGS = "cgs"
    MKS = "mks"
    BRITISH_IMPERIAL = "imperial"
    US_IMPERIAL = "US"
    SI = "SI"


class DecimalPlacesRegistry:
    DEFAULT_DECIMAL_PLACES = 2

    __slots__ = ("_decimal_places",)

    def __init__(self):
        self._decimal_places = self.DEFAULT_DECIMAL_PLACES

    @property
    def decimal_places(self) -> int:
        return self._decimal_places

    @decimal_places.setter
    def decimal_places(self, val: int) -> None:
        if isinstance(val, int):
            self._decimal_places = val
        else:
            raise ValueError("val must be an int")

    def reset(self) -> None:
        """Resets decimal places to the default value."""
        self._decimal_places = self.DEFAULT_DECIMAL_PLACES


class CustomQuantity(pint.UnitRegistry.Quantity):
    pass


class CustomUnit(pint.UnitRegistry.Unit):
    pass


class UnitRegistry(
    pint.registry.GenericUnitRegistry[CustomQuantity, CustomUnit]
):
    DEFAULT_UNIT_SYSTEM = UnitSystem.SI
    Quantity = CustomQuantity
    Unit = CustomUnit

    def reset(self) -> None:
        self.default_system = self.DEFAULT_UNIT_SYSTEM


DecimalPlacesReg = DecimalPlacesRegistry()
UnitReg = UnitRegistry(system=UnitSystem.SI)
Quantity = UnitReg.Quantity
