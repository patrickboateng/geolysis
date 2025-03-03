""" Ultimate bearing capacity estimation package

Enum
====

.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    UBC_TYPE

Modules
=======

.. autosummary::
    :toctree: _autosummary

    hansen_ubc
    vesic_ubc
    terzaghi_ubc

Functions
=========

.. autosummary::
    :toctree: _autosummary

    create_ultimate_bearing_capacity
"""
import statistics
import enum
from abc import ABC, abstractmethod
from typing import Optional

from geolysis import validators, error_msg_tmpl
from geolysis.foundation import FoundationSize, Shape, create_foundation
from geolysis.utils import arctan, enum_repr, inf, tan

__all__ = ["UltimateBearingCapacity",
           "TerzaghiUBC4StripFooting",
           "TerzaghiUBC4CircularFooting",
           "TerzaghiUBC4RectangularFooting",
           "TerzaghiUBC4SquareFooting",
           "HansenUltimateBearingCapacity",
           "VesicUltimateBearingCapacity",
           "create_ultimate_bearing_capacity"]


class UltimateBearingCapacity(ABC):
    def __init__(self, friction_angle: float,
                 cohesion: float,
                 moist_unit_wgt: float,
                 foundation_size: FoundationSize,
                 load_angle=0.0,
                 apply_local_shear=False) -> None:
        r"""
        :param friction_angle: Internal angle of friction for general shear 
                               failure. (degrees)
        :type friction_angle: float
        
        :param cohesion: Cohesion of soil. (kPa)
        :type cohesion: float

        :param moist_unit_wgt: Moist unit weight of soil. (:math:`kN/m^3`)
        :type moist_unit_wgt: float

        :param foundation_size: Size of the foundation.
        :type foundation_size: FoundationSize

        :param load_angle: Inclination of the applied load with the  vertical 
                           (:math:`\alpha^{\circ}`), defaults to 0.0.
        :type load_angle: float, optional

        :param apply_local_shear: Indicate whether bearing capacity failure is
                                  general shear or local shear failure,
                                  defaults to False.
        :type apply_local_shear: bool, optional
        """
        self.friction_angle = friction_angle
        self.cohesion = cohesion
        self.moist_unit_wgt = moist_unit_wgt
        self.load_angle = load_angle
        self.foundation_size = foundation_size
        self.apply_local_shear = apply_local_shear

    @property
    def friction_angle(self) -> float:
        """Return friction angle for local shear in the case of local shear
        failure or general shear in the case of general shear failure.
        """
        if self.apply_local_shear:
            return arctan((2 / 3) * tan(self._friction_angle))
        return self._friction_angle

    @friction_angle.setter
    @validators.ge(0.0)
    def friction_angle(self, val: float):
        self._friction_angle = val

    @property
    def cohesion(self) -> float:
        """Return cohesion for local shear in the case of local shear failure
        or general shear in the case of general shear failure.
        """
        if self.apply_local_shear:
            return (2.0 / 3.0) * self._cohesion
        return self._cohesion

    @cohesion.setter
    @validators.ge(0.0)
    def cohesion(self, val: float):
        self._cohesion = val

    @property
    def moist_unit_wgt(self) -> float:
        return self._moist_unit_wgt

    @moist_unit_wgt.setter
    @validators.gt(0.0)
    def moist_unit_wgt(self, val: float):
        self._moist_unit_wgt = val

    @property
    def load_angle(self) -> float:
        return self._load_angle

    @load_angle.setter
    @validators.le(90.0)
    @validators.ge(0.0)
    def load_angle(self, val: float):
        self._load_angle = val

    @property
    def s_c(self) -> float:
        return 1.0

    @property
    def s_q(self) -> float:
        return 1.0

    @property
    def s_gamma(self) -> float:
        return 1.0

    @property
    def d_c(self) -> float:
        return 1.0

    @property
    def d_q(self) -> float:
        return 1.0

    @property
    def d_gamma(self) -> float:
        return 1.0

    @property
    def i_c(self) -> float:
        return 1.0

    @property
    def i_q(self) -> float:
        return 1.0

    @property
    def i_gamma(self) -> float:
        return 1.0

    def _cohesion_term(self, coef: float = 1.0) -> float:
        return coef * self.cohesion * self.n_c * self.s_c * self.d_c * self.i_c

    def _surcharge_term(self) -> float:
        depth = self.foundation_size.depth
        water_level = self.foundation_size.ground_water_level

        if water_level is None:
            water_corr = 1.0  # water correction
        else:
            # water level above the base of the foundation
            a = max(depth - water_level, 0.0)
            water_corr = min(1 - 0.5 * a / depth, 1)

        # effective overburden pressure (surcharge)
        eop = self.moist_unit_wgt * depth
        return eop * self.n_q * self.s_q * self.d_q * self.i_q * water_corr

    def _embedment_term(self, coef: float = 0.5) -> float:
        depth = self.foundation_size.depth
        width = self.foundation_size.effective_width
        water_level = self.foundation_size.ground_water_level

        if water_level is None:
            # water correction
            water_corr = 1.0
        else:
            #: b -> water level below the base of the foundation
            b = max(water_level - depth, 0)
            water_corr = min(0.5 + 0.5 * b / width, 1)

        return (coef * self.moist_unit_wgt * width * self.n_gamma
                * self.s_gamma * self.d_gamma * self.i_gamma * water_corr)

    def bearing_capacity(self):
        return (self._cohesion_term(1.0)
                + self._surcharge_term()
                + self._embedment_term(0.5))

    @property
    @abstractmethod
    def n_c(self) -> float:
        ...

    @property
    @abstractmethod
    def n_q(self) -> float:
        ...

    @property
    @abstractmethod
    def n_gamma(self) -> float:
        ...


from .hansen_ubc import HansenUltimateBearingCapacity
from .terzaghi_ubc import (TerzaghiUBC4CircularFooting,
                           TerzaghiUBC4RectangularFooting,
                           TerzaghiUBC4SquareFooting,
                           TerzaghiUBC4StripFooting)
from .vesic_ubc import VesicUltimateBearingCapacity


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
    :type ground_water_level: float

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
    if ubc_type is None:
        msg = error_msg_tmpl(ubc_type, UBC_TYPE)
        raise ValueError(msg)

    ubc_type = str(ubc_type).casefold()

    try:
        ubc_type = UBC_TYPE(ubc_type)
    except ValueError as e:
        msg = error_msg_tmpl(ubc_type, UBC_TYPE)
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
