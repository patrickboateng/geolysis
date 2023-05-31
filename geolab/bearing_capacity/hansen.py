"""Hansen Bearing Capacity Analysis."""

from typing import Optional

import numpy as np

from geolab import DECIMAL_PLACES, deg2rad
from geolab.bearing_capacity import AbstractBCF, depth_factor, FootingShape
from geolab.utils import cos, exp, pi, sin, tan


class HansenBCF(AbstractBCF):
    """Hansen Bearing Capacity Factors."""

    @deg2rad
    def __init__(self, *, friction_angle: float) -> None:
        self.phi = friction_angle

    @property
    def ngamma(self) -> float:
        _ngamma = 1.8 * (self._nq(self.phi) - 1) * tan(self.phi)
        return np.round(_ngamma, DECIMAL_PLACES)


class MSF:
    """Hansen Shape Factors."""

    def __init__(
        self,
        footing_shape: FootingShape,
        foundation_width: Optional[float] = None,
        foundation_length: Optional[float] = None,
    ) -> None:
        if not isinstance(footing_shape, FootingShape):
            raise TypeError(
                f"Available foundation shapes are {','.join(list(FootingShape))}"
            )

        if footing_shape is FootingShape.STRIP_FOOTING:
            self.sc = 1
            self.sq = 1
            self.sgamma = 1

        elif footing_shape is FootingShape.SQUARE_FOOTING:
            self.sc = 1.3
            self.sq = 1.2
            self.sgamma = 0.8

        elif footing_shape is FootingShape.CIRCULAR_FOOTING:
            self.sc = 1.3
            self.sq = 1.2
            self.sgamma = 0.6

        else:
            if foundation_width is None:
                raise ValueError(f"Foundation width cannot be None for {footing_shape}")
            if foundation_length is None:
                raise ValueError(
                    f"Foundation length cannot be None for {footing_shape}"
                )

            self.w2l = foundation_width / foundation_length
            self.sc = self.sq = 1 + 0.2 * self.w2l
            self.sgamma = 1 - 0.4 * self.w2l

            del self.w2l


class HDF:
    """Hansen Depth Factors."""

    def __init__(self, foundation_depth: float, foundation_width: float) -> None:
        self.d2w = foundation_depth / foundation_width
        self.dc = 1 + 0.35 * self.d2w
        self.dq = self.dc
        self.dgamma = 1

        del self.d2w


class HIF:
    """Hansen Inclination Factors."""

    def __init__(self, beta: float, friction_angle: float) -> None:
        self.beta = beta
        self.phi = friction_angle

    @staticmethod
    @functools.cache
    def _ic(beta) -> float:
        return (1 - beta / 90) ** 2

    def ic(self) -> float:
        return round(self._ic(self.beta), DECIMAL_PLACES)

    def iq(self) -> float:
        return round(self._ic(self.beta), DECIMAL_PLACES)

    def igamma(self) -> float:
        _igamma = (1 - self.beta / self.phi) ** 2
        return round(_igamma, DECIMAL_PLACES)


# class MBC:
#     """Hansen Bearing Capacity."""

#     def __init__(
#         self,
#         n_design: float,
#         foundation_depth: float,
#         foundation_width: float,
#         foundation_length: float,
#         friction_angle: float,
#         beta: float,
#         actual_settlement: float,
#     ) -> None:
#         """
#         :param n_design: average corrected number of blows from ``SPT N-value``
#         :type n_design: float
#         :param foundation_depth: depth of foundation (m)
#         :type foundation_depth: float
#         :param foundation_width: width of foundation (m)
#         :type foundation_width: float
#         :param foundation_length: length of foundation (m)
#         :type foundation_length: float
#         :param friction_angle: internal angle of friction (degrees)
#         :type friction_angle: float
#         ::param beta: inclination of the load on the foundation with
#                       respect to the vertical (degrees)
#         :type beta: float
#         :param actual_settlement: foundation settlement (mm)
#         :type actual_settlement: float
#         :raises AllowableSettlementError: Raised when `allow_settlement` is greater than `25.4mm`
#         """

#         self.n_design = n_design
#         self.fd = foundation_depth
#         self.fw = foundation_width
#         # self.fl = foundation_length
#         # self.phi = friction_angle
#         # self.beta = beta
#         self.se = actual_settlement

#     def allow_bearing_capacity(self) -> float:
#         r"""Allowable bearing capacity :math:`q_{a(net)}` for a given tolerable
#         settlement proposed by Meyerhoff.

#         :return: Allowable bearing capacity
#         :rtype: float
#         """
#         math_expr = (
#             self.n_design
#             * depth_factor(self.fd, self.fw)
#             * (self.se / self.ALLOWABLE_SETTLEMENT)
#         )
#         if self.fw <= 1.22:
#             _abc = 19.16 * math_expr  # allow_bearing_capacity
#             return round(_abc, DECIMAL_PLACES)

#         _abc = 11.98 * ((3.28 * self.fw + 1) / (3.28 * self.fw) ** 2)
#         return round(_abc, DECIMAL_PLACES)

#     @property
#     def nq(self) -> float:
#         r"""Vesic Bearing Capacity factor :math:`N_q`.

#         .. math::

#             \tan^2 \left(45^{\circ} + \frac{\phi}{2} \right)e^{\pi \tan \phi}

#         :return: A `float` representing the bearing capacity factor :math:`N_q`
#         :rtype: float
#         """
#         return self._bearing_cap_factors.nq()

#     @property
#     def nc(self) -> float:
#         """Vesic Bearing Capacity factor :math:`N_c`.

#         .. math::

#         :return: A `float` representing the bearing capacity factor :math:`N_c`
#         :rtype: float
#         """
#         return self._bearing_cap_factors.nc()

#     @property
#     def ngamma(self) -> float:
#         r"""Vesic Bearing Capacity factor :math:`N_\gamma`.

#         :return: A `float` representing the bearing capacity factor :math:`N_\gamma`
#         :rtype: float
#         """
#         return self._bearing_cap_factors.ngamma()

#     @property
#     def dq(self) -> float:
#         r"""Depth factor :math:`d_q`.

#         .. math::

#             if \, \frac{D_f}{B} \le 1:

#                 1 + 2 \tan \phi (1 - \sin \phi)^2 \frac{D_f}{B}


#             if \, \frac{D_f}{B} \gt 1:

#                 1 + 2\tan\phi (1-\sin \phi)^2\tan^{-1}\frac{D_f}{B}\times \frac{\pi}{180}

#         :return: A `float` representing the depth factor :math:`d_q`
#         :rtype: float
#         """
#         return self._depth_factors.dq()

#     @property
#     def dc(self) -> float:
#         r"""Depth factor :math:`d_c`.

#         .. math::

#             if \, \frac{D_f}{B} \le 1:

#                 1 + 0.4 \frac{D_f}{B}

#             if \, \frac{D_f}{B} \gt 1:

#                 1 + 0.4 \tan^{-1} (\frac{D_f}{B}) \times \frac{\pi}{180}

#         :return: A `float` representing the depth factor :math:`d_c`
#         :rtype: float
#         """
#         return self._depth_factors.dc()

#     @property
#     def dgamma(self) -> float:
#         r"""Depth factor :math:`d_\gamma`.

#         :return: A `float` representing the depth factor :math:`d_\gamma`
#         :rtype: float
#         """
#         return self._depth_factors.dgamma()

#     @property
#     def sq(self) -> float:
#         r"""Shape factor :math:`S_q`.

#         .. math::

#             S_q = 1 + \frac{B}{L} \tan \phi

#         :return: A `float` representing the shape factor :math:`S_q`
#         :rtype: float
#         """
#         return self._shape_factors.sq()

#     @property
#     def sc(self) -> float:
#         r"""Shape factor :math:`S_c`.

#         .. math::

#             S_c = 1 + \frac{B N_q}{L N_c}

#         :return: A `float` representing the shape factor :math:`S_c`
#         :rtype: float
#         """
#         return self._shape_factors.sc(self.nq, self.nc)

#     @property
#     def sgamma(self) -> float:
#         r"""Shape factor :math:`S_\gamma`.

#         .. math::

#             S_\gamma = 1 - 0.4\frac{B}{L}

#         :return: A `float` representing the shape factor :math:`S_\gamma`
#         :rtype: float
#         """
#         return self._shape_factors.sgamma()

#     @property
#     def iq(self) -> float:
#         r"""Inclination factor :math:`i_q`.

#         .. math::

#             \left(1 - \dfrac{\beta^\circ}{90^\circ} \right)^2

#         :return: A `float` representing the inclination factor :math:`i_q`
#         :rtype: float
#         """
#         return self._incl_factors.iq()

#     @property
#     def ic(self) -> float:
#         r"""Inclination factor :math:`i_c`.

#         .. math::

#             \left(1 - \dfrac{\beta^\circ}{90^\circ} \right)^2

#         :return: A `float` representing the inclination factor :math:`i_c`
#         :rtype: float
#         """
#         return self._incl_factors.ic()

#     @property
#     def igamma(self) -> float:
#         r"""Inclination factor :math:`i_\gamma`.

#         .. math::

#             \left(1 - \dfrac{\beta}{\phi} \right)^2

#         :return: A `float` representing the inclination factor :math:`i_\gamma`
#         :rtype: float
#         """
#         return self._incl_factors.igamma()
