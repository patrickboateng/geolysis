import enum
from typing import Optional, Annotated

from func_validator import MustBeMemberOf, validate_params

from geolysis.foundation import Shape, create_foundation
from geolysis.utils import AbstractStrEnum, inf

from ._core import UltimateBearingCapacity
from ._terzaghi_ubc import (
    TerzaghiUBC4CircularFooting,
    TerzaghiUBC4RectangularFooting,
    TerzaghiUBC4SquareFooting,
    TerzaghiUBC4StripFooting,
)
from ._vesic_ubc import VesicUltimateBearingCapacity

__all__ = [
    "TerzaghiUBC4StripFooting",
    "TerzaghiUBC4CircularFooting",
    "TerzaghiUBC4RectangularFooting",
    "TerzaghiUBC4SquareFooting",
    "VesicUltimateBearingCapacity",
    "UBCType",
    "create_ubc_4_all_soil_types",
]


class UBCType(AbstractStrEnum):
    """Enumeration of available ultimate bearing capacity methods.

    Each member represents a different method for determining
    the ultimate bearing capacity of soil.
    """

    TERZAGHI = enum.auto()
    """Terzaghi's method for calculating ultimate bearing capacity."""

    VESIC = enum.auto()
    """Vesic's method for calculating ultimate bearing capacity."""


ubc_classes = {
    UBCType.TERZAGHI: {
        Shape.STRIP: TerzaghiUBC4StripFooting,
        Shape.CIRCLE: TerzaghiUBC4CircularFooting,
        Shape.SQUARE: TerzaghiUBC4SquareFooting,
        Shape.RECTANGLE: TerzaghiUBC4RectangularFooting,
    },
    UBCType.VESIC: VesicUltimateBearingCapacity,
}


@validate_params
def create_ubc_4_all_soil_types(
    friction_angle: float,
    cohesion: float,
    moist_unit_wgt: float,
    depth: float,
    width: float,
    length: Optional[float] = None,
    factor_of_safety: float = 3.0,
    saturated_unit_wgt: float = 20.5,
    eccentricity: float = 0.0,
    ground_water_level: Optional[float] = inf,
    load_angle: float = 0.0,
    apply_local_shear: bool = False,
    shape: Shape | str = "square",
    ubc_type: Annotated[UBCType | str, MustBeMemberOf(UBCType)] = "vesic",
) -> UltimateBearingCapacity:
    r"""A factory function that encapsulate the creation of ultimate
    bearing capacity.

    :param friction_angle: Internal angle of friction for general shear
                           failure (degree).

    :param cohesion: Cohesion of soil ($kPa$).
    :param moist_unit_wgt: Moist unit weight of soil ($kN/m^3$).
    :param depth: Depth of foundation (m).
    :param width: Width of foundation footing (m).
    :param length: Length of foundation footing (m).
    :param factor_of_safety: Factor of safety.
    :param saturated_unit_wgt: Saturated unit weight of soil ($kN/m^3$).
    :param eccentricity: The deviation of the foundation load from the
                         center of gravity of the foundation footing.
    :param ground_water_level: Depth of water below ground level (m).
    :param load_angle: Inclination of the applied load with the  vertical
                       ($\alpha^{\circ}$).
    :param apply_local_shear: Indicate whether bearing capacity failure
                              is general or local shear failure.
    :param shape: Shape of foundation footing.
    :param ubc_type: Type of allowable bearing capacity calculation to
                     apply.

    :raises ValidationError: Raised if ubc_type is not supported.
    :raises ValidationError: Raised if an invalid footing shape is
                             provided.
    :raises ValidationError: Raised when length is not provided for a
                             rectangular footing.
    """
    ubc_type = UBCType(ubc_type)

    # exception from create_foundation will automatically propagate
    # no need to catch and handle it.
    fnd_size = create_foundation(
        depth=depth,
        width=width,
        length=length,
        eccentricity=eccentricity,
        load_angle=load_angle,
        ground_water_level=ground_water_level,
        shape=shape,
    )
    ubc_class = ubc_classes[ubc_type]

    if ubc_type == UBCType.TERZAGHI:
        ubc_class = ubc_classes[ubc_type][fnd_size.footing_shape]

    return ubc_class(
        friction_angle=friction_angle,
        cohesion=cohesion,
        moist_unit_wgt=moist_unit_wgt,
        factor_of_safety=factor_of_safety,
        saturated_unit_wgt=saturated_unit_wgt,
        foundation_size=fnd_size,
        apply_local_shear=apply_local_shear,
    )
