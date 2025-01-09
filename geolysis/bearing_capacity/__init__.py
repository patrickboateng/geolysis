from collections import UserDict
from typing import TypedDict

__all__ = ["SoilProperties", "Soil", "abc_4_cohl_soils", "hansen_ubc",
           "terzaghi_ubc", "vesic_ubc"]


class SoilProperties(TypedDict):
    friction_angle: float
    cohesion: float
    moist_unit_wgt: float


class Soil(UserDict):

    def __getattr__(self, name: str):
        if name in self.data:
            return self.data[name]
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'")


from .abc_4_soils import abc_4_cohl_soils
from .ubc_4_soils import hansen_ubc, vesic_ubc, terzaghi_ubc
