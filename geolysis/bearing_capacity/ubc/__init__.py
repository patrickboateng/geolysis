""" Ultimate bearing capacity estimation package

Enum
====

.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    UBC_TYPE

Functions
=========

.. autosummary::
    :toctree: _autosummary

    create_ultimate_bearing_capacity
"""
import enum
from typing import Optional

from geolysis.foundation import Shape, create_foundation
from geolysis.utils import enum_repr

from ._core import UltimateBearingCapacity
from .hansen_ubc import HansenUltimateBearingCapacity
from .terzaghi_ubc import (TerzaghiUBC4CircularFooting,
                           TerzaghiUBC4RectangularFooting,
                           TerzaghiUBC4SquareFooting, TerzaghiUBC4StripFooting)
from .vesic_ubc import VesicUltimateBearingCapacity

__all__ = ["UBC_TYPE",
           "TerzaghiUBC4StripFooting",
           "TerzaghiUBC4CircularFooting",
           "TerzaghiUBC4RectangularFooting",
           "TerzaghiUBC4SquareFooting",
           "HansenUltimateBearingCapacity",
           "VesicUltimateBearingCapacity",
           "create_ultimate_bearing_capacity"]


@enum_repr
class UBC_TYPE(enum.StrEnum):
    """Enumeration of available ultimate bearing capacity types."""
    HANSEN = enum.auto()
    TERZAGHI = enum.auto()
    VESIC = enum.auto()


def create_ultimate_bearing_capacity(friction_angle: float,
                                     cohesion: float,
                                     moist_unit_wgt: float,
                                     depth: float,
                                     width: float,
                                     length: Optional[float] = None,
                                     eccentricity: float = 0.0,
                                     ground_water_level: Optional[
                                         float] = None,
                                     shape: Shape | str = Shape.SQUARE,
                                     load_angle=0.0,
                                     apply_local_shear=False,
                                     ubc_type: Optional[UBC_TYPE | str] = None,
                                     ) -> UltimateBearingCapacity:
    r"""A factory function that encapsulate the creation of ultimate bearing
    capacity.

    :param friction_angle: Internal angle of friction for general shear
                           failure. (degree)
    :type friction_angle: float

    :param cohesion: Cohesion of soil. (kPa)
    :type cohesion: float

    :param moist_unit_wgt: Moist unit weight of soil. (:math:`kN/m^3`)
    :type moist_unit_wgt: float

    :param depth: Depth of foundation. (m)
    :type depth: float

    :param width: Width of foundation footing. (m)
    :type width: float

    :param length: Length of foundation footing. (m)
    :type length: float, optional

    :param eccentricity: The deviation of the foundation load from the
                         center of gravity of the foundation footing,
                         defaults to 0.0. This means that the foundation
                         load aligns with the center of gravity of the
                         foundation footing. (m)
    :type eccentricity: float, optional

    :param ground_water_level: Depth of water below ground level. (m)
    :type ground_water_level: float, optional

    :param shape: Shape of foundation footing, defaults to "SQUARE".
    :type shape: Shape | str, optional

    :param load_angle: Inclination of the applied load with the  vertical
                       (:math:`\alpha^{\circ}`), defaults to 0.0.
    :type load_angle: float, optional

    :param apply_local_shear: Indicate whether bearing capacity failure is
                              general or local shear failure, defaults to
                              False.
    :type apply_local_shear: bool, optional

    :param ubc_type: Type of allowable bearing capacity calculation to apply.
                     Available values are: "HANSEN", "TERZAGHI", "VESIC".
                     defaults to None.
    :type ubc_type:  UBC_TYPE | str, optional

    :raises ValueError: Raised if ubc_type is not supported.
    :raises ValueError: Raised when length is not provided for a rectangular
                        footing.
    :raises ValueError: Raised if an invalid footing shape is provided.
    """
    msg = (f"{ubc_type=} is not supported, Supported "
           f"types are: {list(UBC_TYPE)}")

    if ubc_type is None:
        raise ValueError(msg)

    try:
        ubc_type = UBC_TYPE(str(ubc_type).casefold())
    except ValueError as e:
        raise ValueError(msg) from e

    # exception from create_foundation will automaatically propagate
    # no need to catch and handle it.
    fnd_size = create_foundation(depth=depth,
                                 width=width,
                                 length=length,
                                 eccentricity=eccentricity,
                                 ground_water_level=ground_water_level,
                                 shape=shape)
    ubc_classes = {
        UBC_TYPE.HANSEN: HansenUltimateBearingCapacity,
        UBC_TYPE.TERZAGHI: {Shape.STRIP: TerzaghiUBC4StripFooting,
                            Shape.CIRCLE: TerzaghiUBC4CircularFooting,
                            Shape.SQUARE: TerzaghiUBC4SquareFooting,
                            Shape.RECTANGLE: TerzaghiUBC4RectangularFooting},
        UBC_TYPE.VESIC: VesicUltimateBearingCapacity,
    }

    if ubc_type == UBC_TYPE.TERZAGHI:
        ubc_class = ubc_classes[ubc_type][fnd_size.footing_shape]
    else:
        ubc_class = ubc_classes[ubc_type]

    ubc = ubc_class(friction_angle=friction_angle,
                    cohesion=cohesion,
                    moist_unit_wgt=moist_unit_wgt,
                    foundation_size=fnd_size,
                    load_angle=load_angle,
                    apply_local_shear=apply_local_shear)
    return ubc
