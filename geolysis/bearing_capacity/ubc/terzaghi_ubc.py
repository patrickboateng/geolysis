from abc import ABC

from geolysis.bearing_capacity.ubc import UltimateBearingCapacity
from geolysis.utils import (inf, pi, cos, cot, deg2rad, exp, isclose, round_,
                            tan)

__all__ = ["TerzaghiBearingCapacityFactor", 
           "TerzaghiUBC4StripFooting",
           "TerzaghiUBC4CircularFooting", 
           "TerzaghiUBC4SquareFooting",
           "TerzaghiUBC4RectangularFooting"]


class TerzaghiBearingCapacityFactor:
    """ Bearing capacity factors for ultimate bearing capacity according to
    ``Terzaghi (1943)``."""

    @classmethod
    @round_
    def n_c(cls, friction_angle: float) -> float:
        r"""Bearing capacity factor :math:`N_c`.

        :param friction_angle: Angle of internal friction of the soil (degrees).
        :type friction_angle: float

        .. math:: N_c = \cot(\phi) \cdot (N_q - 1)
        """
        if isclose(friction_angle, 0.0):
            return 5.7
        return cot(friction_angle) * (cls.n_q(friction_angle) - 1.0)

    @classmethod
    @round_
    def n_q(cls, friction_angle: float) -> float:
        r"""Bearing capacity factor :math:`N_q`.

        :param friction_angle: Angle of internal friction of the soil (degrees).
        :type friction_angle: float

        .. math::

            N_q = \dfrac{e^{(\frac{3\pi}{2} - \phi)\tan\phi}}
                  {2\cos^2(45 + \frac{\phi}{2})}
        """
        return exp((3 * pi / 2 - deg2rad(friction_angle)) * tan(friction_angle)) \
               / (2 * (cos(45 + friction_angle / 2)) ** 2)

    @classmethod
    @round_
    def n_gamma(cls, friction_angle: float) -> float:
        r"""Bearing capacity factor :math:`N_{\gamma}`.
        
        :param friction_angle: Angle of internal friction of the soil (degrees).
        :type friction_angle: float

        .. math:: N_{\gamma} =  (N_q - 1) \cdot \tan(1.4\phi)
        """
        return (cls.n_q(friction_angle) - 1) * tan(1.4 * friction_angle)


class TerzaghiUltimateBearingCapacity(UltimateBearingCapacity, ABC):

    @property
    def n_c(self) -> float:
        return TerzaghiBearingCapacityFactor.n_c(self.friction_angle)

    @property
    def n_q(self) -> float:
        return TerzaghiBearingCapacityFactor.n_q(self.friction_angle)

    @property
    def n_gamma(self) -> float:
        return TerzaghiBearingCapacityFactor.n_gamma(self.friction_angle)

    
class TerzaghiUBC4StripFooting(TerzaghiUltimateBearingCapacity):
    """Ultimate bearing capacity for strip footing according to 
    ``Terzaghi 1943``.
    """

    @round_
    def bearing_capacity(self) -> float:
        r"""Calculates ultimate bearing capacity for strip footing.

        .. math:: q_u = cN_c + qN_q + 0.5 \gamma BN_{\gamma}
        """
        return self._cohesion_term(1.0) \
               + self._surcharge_term() \
               + self._embedment_term(0.5)


class TerzaghiUBC4CircularFooting(TerzaghiUltimateBearingCapacity):
    """Ultimate bearing capacity for circular footing according to 
    ``Terzaghi 1943``.
    """

    @round_
    def bearing_capacity(self) -> float:
        r"""Calculates ultimate bearing capacity for circular footing.

        .. math:: q_u = 1.3cN_c + qN_q + 0.3 \gamma BN_{\gamma}
        """
        return self._cohesion_term(1.3) \
               + self._surcharge_term() \
               + self._embedment_term(0.3)


class TerzaghiUBC4RectangularFooting(TerzaghiUltimateBearingCapacity):
    """Ultimate bearing capacity for rectangular footing according to 
    ``Terzaghi 1943``.
    """

    @round_
    def bearing_capacity(self) -> float:
        r"""Calculates ultimate bearing capacity for rectangular footing.

        .. math::

            q_u = \left(1 + 0.3 \dfrac{B}{L} \right) c N_c + qN_q
                  + \left(1 - 0.2 \dfrac{B}{L} \right) 0.5 B \gamma N_{\gamma}
        """
        f_w = self.foundation_size.width
        f_l = self.foundation_size.length
        coh_coef = 1 + 0.3 * (f_w / f_l)
        emb_coef = (1 - 0.2 * (f_w / f_l)) / 2.0

        return self._cohesion_term(coh_coef) \
               + self._surcharge_term() \
               + self._embedment_term(emb_coef)


class TerzaghiUBC4SquareFooting(TerzaghiUBC4RectangularFooting):
    r"""Ultimate bearing capacity for square footing according to 
    ``Terzaghi 1943``.
    """

    def bearing_capacity(self):
        r"""Calcalates ultimate bearing capacity for square footing.
        
        .. math:: q_u = 1.3cN_c + qN_q + 0.4 \gamma BN_{\gamma}
        """
        return super().bearing_capacity()
