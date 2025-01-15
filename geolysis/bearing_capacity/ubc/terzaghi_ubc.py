from abc import ABC

from geolysis.bearing_capacity.ubc import UltimateBearingCapacity
from geolysis.utils import (inf, pi, cos, cot, deg2rad, exp, isclose, round_,
                            tan)

__all__ = ["TerzaghiBearingCapacityFactor", "TerzaghiUBC4StripFooting",
           "TerzaghiUBC4CircFooting", "TerzaghiUBC4SquareFooting",
           "TerzaghiUBC4RectFooting"]


class TerzaghiBearingCapacityFactor:
    @classmethod
    @round_
    def n_c(cls, friction_angle: float) -> float:
        if isclose(friction_angle, 0.0):
            return 5.7
        return cot(friction_angle) * (cls.n_q(friction_angle) - 1.0)

    @classmethod
    @round_
    def n_q(cls, friction_angle: float) -> float:
        return exp((3 * pi / 2 - deg2rad(friction_angle)) * tan(friction_angle)
                   ) / (2 * (cos(45 + friction_angle / 2)) ** 2)

    @classmethod
    @round_
    def n_gamma(cls, friction_angle: float) -> float:
        return (cls.n_q(friction_angle) - 1) * tan(1.4 * friction_angle)


class TerzaghiShapeFactor:
    @classmethod
    def s_c(cls) -> float:
        return 1.0

    @classmethod
    def s_q(cls) -> float:
        return 1.0

    @classmethod
    def s_gamma(cls) -> float:
        return 1.0


class TerzaghiDepthFactor:
    @classmethod
    def d_c(cls) -> float:
        return 1.0

    @classmethod
    def d_q(cls) -> float:
        return 1.0

    @classmethod
    def d_gamma(cls) -> float:
        return 1.0


class TerzaghiInclinationFactor:
    @classmethod
    def i_c(cls) -> float:
        return 1.0

    @classmethod
    def i_q(cls) -> float:
        return 1.0

    @classmethod
    def i_gamma(cls) -> float:
        return 1.0


class TerzaghiUltimateBearingCapacity(UltimateBearingCapacity, ABC):

    @property
    def n_c(self) -> float:
        r"""Bearing capacity factor :math:`N_c`.

        .. math:: N_c = \cot \phi (N_q - 1)
        """
        return TerzaghiBearingCapacityFactor.n_c(self.friction_angle)

    @property
    def n_q(self) -> float:
        r"""Bearing capacity factor :math:`N_q`.

        .. math::

            N_q = \dfrac{e^{(\frac{3\pi}{2} - \phi)\tan\phi}}
                  {2\cos^2(45 + \frac{\phi}{2})}
        """
        return TerzaghiBearingCapacityFactor.n_q(self.friction_angle)

    @property
    def n_gamma(self) -> float:
        r"""Bearing capacity factor :math:`N_{\gamma}`.

        .. math:: N_{\gamma} =  (N_q - 1) \tan(1.4\phi)
        """
        return TerzaghiBearingCapacityFactor.n_gamma(self.friction_angle)

    @property
    def s_c(self) -> float:
        """Shape factor :math:`s_c`."""
        return TerzaghiShapeFactor.s_c()

    @property
    def s_q(self) -> float:
        """Shape factor :math:`s_q`."""
        return TerzaghiShapeFactor.s_q()

    @property
    def s_gamma(self) -> float:
        r"""Shape factor :math:`s_{\gamma}`."""
        return TerzaghiShapeFactor.s_gamma()

    @property
    def d_c(self) -> float:
        """Depth factor :math:`d_c`."""
        return TerzaghiDepthFactor.d_c()

    @property
    def d_q(self) -> float:
        """Depth factor :math:`d_q`."""
        return TerzaghiDepthFactor.d_q()

    @property
    def d_gamma(self) -> float:
        r"""Depth factor :math:`d_{\gamma}`."""
        return TerzaghiDepthFactor.d_gamma()

    @property
    def i_c(self) -> float:
        """Inclination factor :math:`i_c`."""
        return TerzaghiInclinationFactor.i_c()

    @property
    def i_q(self) -> float:
        """Inclination factor :math:`i_q`."""
        return TerzaghiInclinationFactor.i_q()

    @property
    def i_gamma(self) -> float:
        r"""Inclination factor :math:`i_{\gamma}`."""
        return TerzaghiInclinationFactor.i_gamma()


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


class TerzaghiUBC4CircFooting(TerzaghiUltimateBearingCapacity):
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


class TerzaghiUBC4RectFooting(TerzaghiUltimateBearingCapacity):
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


class TerzaghiUBC4SquareFooting(TerzaghiUBC4RectFooting):
    r"""Ultimate bearing capacity for square footing according to 
    ``Terzaghi 1943``.
    """

    def bearing_capacity(self):
        r"""Calcalates ultimate bearing capacity for square footing.
        
        .. math:: q_u = 1.3cN_c + qN_q + 0.4 \gamma BN_{\gamma}
        """
        return super().bearing_capacity()
