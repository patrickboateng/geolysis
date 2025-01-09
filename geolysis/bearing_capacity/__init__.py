from collections import UserDict
from typing import TypedDict

__all__ = ["SoilProperties", "Soil"]


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
