"""Meyerhoff Bearing Capacity Analysis."""

import functools

import numpy as np

from geolab import DECIMAL_PLACES, deg2rad
from geolab.bearing_capacity import BCF, depth_factor
from geolab.exceptions import AllowableSettlementError


def _check_foundation_settlement(actual_settlement: float, allow_settlement: float):
    if actual_settlement > allow_settlement:
        raise AllowableSettlementError(
            f"actual_settlement: {actual_settlement} cannot be greater than {allow_settlement}"
        )


class MeyerhoffBCF(BCF):
    """Meyerhoff Bearing Capacity Factors."""

    def __init__(self, friction_angle: float) -> None:
        self.friction_angle = friction_angle

    @staticmethod
    def _nq(friction_angle: float) -> float:
        return np.tan(np.deg2rad(45) + friction_angle / 2) * np.exp(
            np.pi * np.tan(friction_angle)
        )

    def nq(self) -> float:
        _nq = self._nq(self.friction_angle)
        return round(_nq, 2)

    def nc(self) -> float:
        _nc = (1 / np.tan(self.friction_angle)) * (self._nq(self.friction_angle) - 1)
        return round(_nc, 2)

    def ngamma(self) -> float:
        _ngamma = 2 * (self._nq(self.friction_angle) + 1) * np.tan(self.friction_angle)
        return np.round(_ngamma, DECIMAL_PLACES)


class MDF:
    """Meyerhoff Depth Factors."""

    def __init__(
        self, foundation_depth: float, foundation_width: float, friction_angle: float
    ) -> None:
        self.fd = foundation_depth
        self.fw = foundation_width
        self.phi = friction_angle
        self.d2w = self.fd / self.fw

    def dc(self) -> float:
        if self.d2w <= 1:
            _dc = 1 + 0.4 * self.d2w
            return round(_dc, 2)

        _dc = 1 + 0.4 * np.arctan(self.d2w) * (np.pi / 180)
        return round(_dc, 2)

    def dq(self) -> float:
        mid_expr = 2 * np.tan(self.phi) * np.power(1 - np.sin(self.phi), 2)
        if self.d2w <= 1:
            _dq = 1 + mid_expr * self.d2w
            return round(_dq, 2)

        last_expr = np.arctan(self.d2w) * (np.pi / 180)
        _dq = 1 + mid_expr * last_expr

        return round(_dq, 2)

    @staticmethod
    def dgamma() -> float:
        return 1.0


class MSF:
    """Meyerhoff Shape Factors."""

    def __init__(
        self, foundation_width: float, foundation_length: float, friction_angle: float
    ) -> None:
        self.fw = foundation_width
        self.fl = foundation_length
        self.phi = friction_angle
        self.w2l = self.fw / self.fl

    def sc(self, nq, nc) -> float:
        _sc = 1 + ((self.fw * nq) / (self.fl * nc))
        return round(_sc, DECIMAL_PLACES)

    def sq(self) -> float:
        _sq = 1 + self.w2l * np.tan(self.phi)
        return round(_sq, DECIMAL_PLACES)

    def sgamma(self) -> float:
        _sgamma = 1 - 0.4 * self.w2l
        return round(_sgamma, DECIMAL_PLACES)


class MIF:
    """Meyerhoff Inclination Factors."""

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


class MBC:
    """Meyerhoff Bearing Capacity.

    :attr ALLOWABLE_SETTLEMENT: maximum permissible settlement
    :type ALLOWABLE_SETTLEMENT: float
    """

    ALLOWABLE_SETTLEMENT: float = 25.4

    @deg2rad
    def __init__(
        self,
        *,
        n_design: float,
        foundation_depth: float,
        foundation_width: float,
        foundation_length: float,
        friction_angle: float,
        beta: float,
        actual_settlement: float,
    ) -> None:
        """
        :param n_design: average corrected number of blows from ``SPT N-value``
        :type n_design: float
        :param foundation_depth: depth of foundation (m)
        :type foundation_depth: float
        :param foundation_width: width of foundation (m)
        :type foundation_width: float
        :param foundation_length: length of foundation (m)
        :type foundation_length: float
        :param friction_angle: internal angle of friction (degrees)
        :type friction_angle: float
        ::param beta: inclination of the load on the foundation with
                      respect to the vertical (degrees)
        :type beta: float
        :param actual_settlement: foundation settlement (mm)
        :type actual_settlement: float
        :raises AllowableSettlementError: Raised when `allow_settlement` is greater than `25.4mm`
        """
        _check_foundation_settlement(actual_settlement, self.ALLOWABLE_SETTLEMENT)

        self.n_design = n_design
        self.fd = foundation_depth
        self.fw = foundation_width
        self.fl = foundation_length
        self.phi = friction_angle
        self.beta = beta
        self.actual_settlement = actual_settlement
        self._bearing_cap_factors = MeyerhoffBCF(self.phi)
        self._depth_factors = MDF(self.fd, self.fw, self.phi)
        self._shape_factors = MSF(self.fw, self.fl, self.phi)
        self._incl_factors = MIF(self.beta, self.phi)

    @property
    def nq(self) -> float:
        r"""Vesic Bearing Capacity factor :math:`N_q`.

        .. math::

            \tan^2 \left(45^{\circ} + \frac{\phi}{2} \right)e^{\pi \tan \phi}

        :return (float): A `float` representing the bearing capacity factor :math:`N_q`
        """
        return self._bearing_cap_factors.nq()

    @property
    def nc(self) -> float:
        """Vesic Bearing Capacity factor :math:`N_c`.

        .. math::

        :return (float): A `float` representing the bearing capacity factor :math:`N_c`
        """
        return self._bearing_cap_factors.nc()

    @property
    def ngamma(self) -> float:
        r"""Vesic Bearing Capacity factor :math:`N_\gamma`.

        :return (float): A `float` representing the bearing capacity factor :math:`N_\gamma`
        """
        return self._bearing_cap_factors.ngamma()

    @property
    def dq(self) -> float:
        r"""Depth factor :math:`d_q`.

        .. math::

            if \, \frac{D_f}{B} \le 1:

                1 + 2 \tan \phi (1 - \sin \phi)^2 \frac{D_f}{B}


            if \, \frac{D_f}{B} \gt 1:

                1 + 2\tan\phi (1-\sin \phi)^2\tan^{-1}\frac{D_f}{B}\times \frac{\pi}{180}

        :return: A `float` representing the depth factor :math:`d_q`
        :rtype: float
        """
        return self._depth_factors.dq()

    @property
    def dc(self) -> float:
        r"""Depth factor :math:`d_c`.

        .. math::

            if \, \frac{D_f}{B} \le 1:

                1 + 0.4 \frac{D_f}{B}

            if \, \frac{D_f}{B} \gt 1:

                1 + 0.4 \tan^{-1} (\frac{D_f}{B}) \times \frac{\pi}{180}

        :return: A `float` representing the depth factor :math:`d_c`
        :rtype: float
        """
        return self._depth_factors.dc()

    @property
    def dgamma(self) -> float:
        r"""Depth factor :math:`d_\gamma`.

        :return: A `float` representing the depth factor :math:`d_\gamma`
        :rtype: float
        """
        return self._depth_factors.dgamma()

    @property
    def sq(self) -> float:
        r"""Shape factor :math:`S_q`.

        .. math::

            S_q = 1 + \frac{B}{L} \tan \phi

        :return: A `float` representing the shape factor :math:`S_q`
        :rtype: float
        """
        return self._shape_factors.sq()

    @property
    def sc(self) -> float:
        r"""Shape factor :math:`S_c`.

        .. math::

            S_c = 1 + \frac{B N_q}{L N_c}

        :return: A `float` representing the shape factor :math:`S_c`
        :rtype: float
        """
        return self._shape_factors.sc(self.nq, self.nc)

    @property
    def sgamma(self) -> float:
        r"""Shape factor :math:`S_\gamma`.

        .. math::

            S_\gamma = 1 - 0.4\frac{B}{L}

        :return: A `float` representing the shape factor :math:`S_\gamma`
        :rtype: float
        """
        return self._shape_factors.sgamma()

    @property
    def iq(self) -> float:
        r"""Inclination factor :math:`i_q`.

        .. math::

            \left(1 - \dfrac{\beta^\circ}{90^\circ} \right)^2

        :return: A `float` representing the inclination factor :math:`i_q`
        :rtype: float
        """
        return self._incl_factors.iq()

    @property
    def ic(self) -> float:
        r"""Inclination factor :math:`i_c`.

        .. math::

            \left(1 - \dfrac{\beta^\circ}{90^\circ} \right)^2

        :return: A `float` representing the inclination factor :math:`i_c`
        :rtype: float
        """
        return self._incl_factors.ic()

    @property
    def igamma(self) -> float:
        r"""Inclination factor :math:`i_\gamma`.

        .. math::

            \left(1 - \dfrac{\beta}{\phi} \right)^2

        :return: A `float` representing the inclination factor :math:`i_\gamma`
        :rtype: float
        """
        return self._incl_factors.igamma()

    def allow_bearing_capacity(self) -> float:
        r"""Allowable bearing capacity :math:`q_{a(net)}` for a given tolerable
        settlement proposed by Meyerhoff.

        :return (float): Allowable bearing capacity
        """
        if self.foundation_width <= 1.22:
            _allow_bearing_capacity = (
                19.16
                * self.n_design
                * depth_factor(self.foundation_depth, self.foundation_width)
                * (self.n_design / 25.4)
            )
            return round(_allow_bearing_capacity, DECIMAL_PLACES)

        _allow_bearing_capacity = (
            11.98
            * self.n_design
            * np.power(
                (3.28 * self.foundation_width + 1) / (3.28 * self.foundation_width), 2
            )
            * depth_factor(self.foundation_depth, self.foundation_width)
            * (self.actual_settlement / 25.4)
        )
        return round(_allow_bearing_capacity, DECIMAL_PLACES)
