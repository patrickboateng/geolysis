import numpy as np

from geolab import DECIMAL_PLACES, deg2rad
from geolab.bearing_capacity import BCF, depth_factor
from geolab.exceptions import AllowableSettlementError


def check_foundation_settlement(actual_settlement: float, allow_settlement: float):
    """Checks if actual settlement is in the required range.

    :param actual_settlement: foundation settlement (mm)
    :type actual_settlement: float
    :param allow_settlement: allowable foundation settlement (mm)
    :type allow_settlement: float
    :raises AllowableSettlementError: Raised when actual settlement is greater than
                                      allowable settlement
    """
    if actual_settlement > allow_settlement:
        raise AllowableSettlementError(
            f"actual_settlement: {actual_settlement} cannot be greater than {allow_settlement}"
        )


class MeyerhoffBCF(BCF):
    """Meyerhoff Bearing Capacity Factors."""

    @staticmethod
    def _nq(friction_angle: float) -> float:
        return np.tan(np.deg2rad(45) + friction_angle / 2) * np.exp(
            np.pi * np.tan(friction_angle)
        )

    @property
    def nq(self) -> float:
        r"""Vesic Bearing Capacity factor :math:`N_q`.

        .. math::

            \tan^2 \left(45^{\circ} + \frac{\phi}{2} \right)e^{\pi \tan \phi}

        :param friction_angle: Internal angle of friction (degrees)
        :type friction_angle: float
        :return: A `float` representing the bearing capacity factor :math:`N_q`
        :rtype: float
        """
        _nq = self._nq(self.friction_angle)
        return round(_nq, 2)

    @property
    def nc(self) -> float:
        """Vesic Bearing Capacity factor :math:`N_c`.

        .. math::


        :param friction_angle: Internal angle of friction (degrees)
        :type friction_angle: float
        :return: A `float` representing the bearing capacity factor :math:`N_c`
        :rtype: float
        """
        _nc = (1 / np.tan(self.friction_angle)) * (self._nq(self.friction_angle) - 1)
        return round(_nc, 2)

    @property
    def ngamma(self) -> float:
        r"""Vesic Bearing Capacity factor :math:`N_\gamma`.

        :param friction_angle: Internal angle of friction (degrees)
        :type friction_angle: float
        :return: A `float` representing the bearing capacity factor :math:`N_\gamma`
        :rtype: float
        """
        _ngamma = 2 * (self._nq(self.friction_angle) + 1) * np.tan(self.friction_angle)
        return np.round(_ngamma, DECIMAL_PLACES)


class MDF:
    """Meyerhoff Depth Factors."""


class MSF:
    """Meyerhoff Shape Factors."""

    def __init__(
        self, foundation_width: float, foundation_length: float, friction_angle: float
    ) -> None:
        self.foundation_width = foundation_width
        self.foundation_length = foundation_length
        self.friction_angle = friction_angle

    def sc(
        cls, foundation_width: float, foundation_length: float, friction_angle: float
    ) -> float:
        """Shape factor :math:`S_c`.

        :param foundation_width: width of foundation
        :type foundation_width: float
        :param foundation_length: length of foundation
        :type foundation_length: float
        :param friction_angle: Internal angle of friction (degrees)
        :type friction_angle: float
        :return: A `float` representing the shape factor :math:`S_c`
        :rtype: float
        """
        phi = np.rad2deg(friction_angle)
        _sc = 1 + (
            (foundation_width * cls._nq(friction_angle))
            / (foundation_length * cls.nc(friction_angle=phi))
        )
        return round(_sc, DECIMAL_PLACES)

    def sq(
        foundation_width: float, foundation_length: float, *, friction_angle: float
    ) -> float:
        """Shape factor :math:`S_q`.

        :param foundation_width: width of foundation
        :type foundation_width: float
        :param foundation_length: length of foundation
        :type foundation_length: float
        :param friction_angle: Internal angle of friction (degrees)
        :type friction_angle: float
        :return: A `float` representing the shape factor :math:`S_q`
        :rtype: float
        """
        _sq = 1 + ((foundation_width / foundation_length) * np.tan(friction_angle))
        return round(_sq, DECIMAL_PLACES)

    @staticmethod
    def sgamma(foundation_width: float, foundation_length: float) -> float:
        r"""Shape factor :math:`S_\gamma`.

        :param foundation_width: foundation_width of foundation
        :type foundation_width: float
        :param foundation_length: foundation_length of foundation
        :type foundation_length: float
        :return: A `float` representing the shape factor :math:`S_\gamma`
        :rtype: float
        """
        _sgamma = 1 - 0.4 * (foundation_width / foundation_length)
        return round(_sgamma, DECIMAL_PLACES)


class MBC:
    """Meyerhoff Bearing Capacity."""

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
        :param n_design: Average corrected number of blows from ``SPT N-value``
        :type n_design: float
        :param foundation_depth: Depth of foundation (m)
        :type foundation_depth: float
        :param foundation_width: Width of foundation (m)
        :type foundation_width: float
        :param foundation_length: Length of foundation (m)
        :type foundation_length: float
        :param friction_angle: Internal angle of friction (degrees)
        ::param beta: inclination of the load on the foundation with
                     respect to the vertical (degrees)
        :type beta: floattype friction_angle: float
        :param actual_settlement: foundation settlement (mm)
        :type allow_settlement: float
        :raises AllowableSettlementError: Raised when `allow_settlement` is greater than `25.4mm`
        """
        check_foundation_settlement(actual_settlement, self.ALLOWABLE_SETTLEMENT)

        self.n_design = n_design
        self.foundation_depth = foundation_depth
        self.foundation_width = foundation_width
        self.foundation_length = foundation_length
        self.friction_angle = friction_angle
        self.beta = beta
        self.actual_settlement = actual_settlement

    def allow_bearing_capacity(self) -> float:
        r"""Allowable bearing capacity :math:`q_{a(net)}` for a given tolerable
        settlement proposed by Meyerhoff.

        :return: Allowable bearing capacity.
        :rtype: float
        """
        if self.foundation_width <= 1.22:
            _allow_settlement = (
                19.16
                * self.n_design
                * depth_factor(self.foundation_depth, self.foundation_width)
                * (self.n_design / 25.4)
            )
            return round(_allow_settlement, DECIMAL_PLACES)

        _allow_settlement = (
            11.98
            * self.n_design
            * np.power(
                (3.28 * self.foundation_width + 1) / (3.28 * self.foundation_width), 2
            )
            * depth_factor(self.foundation_depth, self.foundation_width)
            * (self.allow_settlement / 25.4)
        )
        return round(_allow_settlement, DECIMAL_PLACES)

    @staticmethod
    def _ic(beta: float) -> float:
        return (1 - beta / 90) ** 2

    @classmethod
    def ic(cls, *, beta: float) -> float:
        """Inclination factor :math:`i_c`.

        :param beta: inclination of the load on the foundation with
                     respect to the vertical (degrees)
        :type beta: float
        :return: A `float` representing the inclination factor :math:`i_c`
        :rtype: float
        """
        _ic = cls._ic(beta)
        return round(_ic, DECIMAL_PLACES)

    @classmethod
    def iq(cls, beta: float) -> float:
        """Inclination factor :math:`i_q`.

        :param beta: inclination of the load on the foundation with
                     respect to the vertical (degrees)
        :type beta: float
        :return: A `float` representing the inclination factor :math:`i_q`
        :rtype: float
        """
        _ic = cls._ic(beta)
        return round(_ic, DECIMAL_PLACES)

    @staticmethod
    def igamma(beta: float, friction_angle: float) -> float:
        r"""Inclination factor :math:`i_\gamma`.

        :param beta: inclination of the load on the foundation with
                     respect to the vertical (degrees)
        :type beta: float
        :param friction_angle: internal angle of friction (degrees)
        :type friction_angle: float
        :return: A `float` representing the inclination factor :math:`i_\gamma`
        :rtype: float
        """
        _igamma = (1 - beta / friction_angle) ** 2
        return round(_igamma, DECIMAL_PLACES)

    @staticmethod
    def dc(foundation_width: float, foundation_depth: float) -> float:
        r"""Depth factor :math:`d_c`.

        :param foundation_width: width of foundation (m)
        :type foundation_width: float
        :param foundation_depth: depth of foundation (m)
        :type foundation_depth: float
        :return: A `float` representing the depth factor :math:`d_c`
        :rtype: float
        """
        if foundation_depth / foundation_width <= 1:
            _dc = 1 + 0.4 * (foundation_depth / foundation_width)
            return round(_dc, 2)

        _dc = 1 + 0.4 * np.arctan(foundation_depth / foundation_width) * (np.pi / 180)
        return round(_dc, 2)

    @staticmethod
    @deg2rad
    def dq(
        foundation_width: float, foundation_depth: float, *, friction_angle: float
    ) -> float:
        r"""Depth factor :math:`d_q`.

        :param foundation_width: width of foundation
        :type foundation_width: float
        :param foundation_depth: depth of foundation
        :type foundation_depth: float
        :param friction_angle: internal angle of friction (degrees)
        :type friction_angle: float
        :return: A `float` representing the depth factor :math:`d_q`
        :rtype: float
        """

        if (foundation_depth / foundation_width) <= 1:
            _dq = (
                1
                + 2
                * np.tan(friction_angle)
                * ((1 - np.sin(friction_angle)) ** 2)
                * foundation_depth
                / foundation_width
            )
            return round(_dq, 2)

        _dq = 1 + 2 * np.tan(friction_angle) * (
            (1 - np.sin(friction_angle)) ** 2
        ) * np.arctan(foundation_depth / foundation_width) * (np.pi / 180)

        return round(_dq, 2)

    @staticmethod
    def dgamma() -> float:
        r"""Depth factor :math:`d_\gamma`.

        :return: A `float` representing the depth factor :math:`d_\gamma`
        :rtype: float
        """
        return 1.0
