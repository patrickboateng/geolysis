from abc import ABC, abstractmethod

from geolysis.foundation import FoundationSize
from geolysis.utils import inf, arctan, tan
from geolysis import validators

__all__ = ["UltimateBearingCapacity",
           "TerzaghiUBC4StripFooting",
           "TerzaghiUBC4CircularFooting",
           "TerzaghiUBC4RectangularFooting",
           "TerzaghiBearingCapacityFactor",
           "TerzaghiUBC4SquareFooting",
           "HansenUltimateBearingCapacity",
           "HansenBearingCapacityFactor",
           "HansenShapeFactor",
           "HansenInclinationFactor",
           "HansenDepthFactor",
           "VesicUltimateBearingCapacity",
           "VesicBearingCapacityFactor",
           "VesicShapeFactor",
           "VesicInclinationFactor",
           "VesicDepthFactor",
           "VesicInclinationFactor"]


class UltimateBearingCapacity(ABC):
    def __init__(self, friction_angle: float,
                 cohesion: float,
                 moist_unit_wgt: float,
                 foundation_size: FoundationSize,
                 load_angle=0.0,
                 ground_water_level=inf,
                 apply_local_shear=False) -> None:
        r"""
        :param friction_angle: Internal angle of friction for general shear 
                               failure. (degree)
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

        :param ground_water_level: Depth of the water below ground level (mm), 
                                   defaults to inf.
        :type ground_water_level: float, optional

        :param apply_local_shear: Indicate whether bearing capacity failure is 
                                  general or local shear failure, defaults to 
                                  False.
        :type apply_local_shear: bool, optional
        """
        self.friction_angle = friction_angle
        self.cohesion = cohesion
        self.moist_unit_wgt = moist_unit_wgt
        self.load_angle = load_angle
        self.ground_water_level = ground_water_level
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
            return (2 / 3) * self._cohesion
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
    def ground_water_level(self) -> float:
        return self._ground_water_level

    @ground_water_level.setter
    @validators.ge(0.0)
    def ground_water_level(self, val: float):
        self._ground_water_level = val

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

    def bearing_capacity(self):
        return (self._cohesion_term(1.0)
                + self._surcharge_term()
                + self._embedment_term(0.5))

    def _cohesion_term(self, coef: float = 1.0) -> float:
        return coef * self.cohesion * self.n_c * self.s_c * self.d_c * self.i_c

    def _surcharge_term(self) -> float:
        depth = self.foundation_size.depth

        if self.ground_water_level == inf:
            water_corr = 1.0  # water correction
        else:
            # water level above the base of the foundation
            a = max(depth - self.ground_water_level, 0.0)
            water_corr = min(1 - 0.5 * a / depth, 1)

        # effective overburden pressure (surcharge)
        eop = self.moist_unit_wgt * depth
        return eop * self.n_q * self.s_q * self.d_q * self.i_q * water_corr

    def _embedment_term(self, coef: float = 0.5) -> float:
        depth = self.foundation_size.depth
        width = self.foundation_size.effective_width

        if self.ground_water_level == inf:
            # water correction
            water_corr = 1.0
        else:
            #: b -> water level below the base of the foundation
            b = max(self.ground_water_level - depth, 0)
            water_corr = min(0.5 + 0.5 * b / width, 1)

        return (coef * self.moist_unit_wgt * width * self.n_gamma
                * self.s_gamma * self.d_gamma * self.i_gamma * water_corr)

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


from .terzaghi_ubc import (TerzaghiUBC4StripFooting,
                           TerzaghiUBC4CircularFooting,
                           TerzaghiUBC4SquareFooting,
                           TerzaghiUBC4RectangularFooting,
                           TerzaghiBearingCapacityFactor)

from .hansen_ubc import (HansenUltimateBearingCapacity,
                         HansenDepthFactor,
                         HansenBearingCapacityFactor,
                         HansenShapeFactor,
                         HansenInclinationFactor)

from .vesic_ubc import (VesicUltimateBearingCapacity,
                        VesicDepthFactor,
                        VesicBearingCapacityFactor,
                        VesicShapeFactor,
                        VesicInclinationFactor)
