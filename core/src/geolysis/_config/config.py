import enum

import pint


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
