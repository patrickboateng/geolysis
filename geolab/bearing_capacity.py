"""This module provides functions for bearing capacity analysis."""

from abc import ABC, abstractmethod

import numpy as np

from geolab import DECIMAL_PLACES, deg2rad, passive_earth_pressure_coef
from geolab.utils import product
from geolab.exceptions import AllowableSettlementError


def check_foundation_settelement():
    ...


def depth_factor(foundation_depth: float, foundation_width: float) -> float:
    """Depth factor used in estimating the allowable bearing capacity of a soil.

    .. math::

        $$k = 1 + 0.33 \\frac{D_f}{B}$$

    :param foundation_depth: Depth of foundation (m)
    :type foundation_depth: float
    :param foundation_width: Width of foundation (m)
    :type foundation_width: float
    :return: Depth factor
    :rtype: float
    """
    _depth_factor = 1 + 0.33 * (foundation_depth / foundation_width)
    return np.round(_depth_factor, DECIMAL_PLACES) if _depth_factor <= 1.33 else 1.33


class BearingCapacityFactors(ABC):
    @property
    @abstractmethod
    def nq(self):
        ...

    @property
    @abstractmethod
    def nc(self):
        ...

    @property
    @abstractmethod
    def ngamma(self):
        ...


class DepthFactors:
    ...


class ShapeFactors:
    ...


class Terzaghi(BearingCapacityFactors):
    """Terzaghi Bearing Capacity."""

    @deg2rad
    def __init__(
        self,
        *,
        cohesion: float,
        friction_angle: float,
        unit_weight_of_soil: float,
        foundation_depth: float,
        foundation_width: float,
    ) -> None:
        """
        :param cohesion: cohesion of foundation soil :math:`(kN/m^2)`
        :type cohesion: float
        :param friction_angle: internal angle of friction :math:`(\phi)`
        :type friction_angle: float
        :param unit_weight_of_soil: unit weight of soil :math:`(kN/m^3)`
        :type unit_weight_of_soil: float
        :param foundation_depth: depth of foundation :math:`d_f` (m)
        :type foundation_depth: float
        :param foundation_width: width of foundation (**b**) (m)
        :type foundation_width: float
        :return: ultimate bearing capacity of the soil :math:`(q_{ult})`
        :rtype: float
        """
        self.cohesion = cohesion
        self.friction_angle = friction_angle
        self.unit_weight_of_soil = unit_weight_of_soil
        self.foundation_depth = foundation_depth
        self.foundation_width = foundation_width

    @staticmethod
    def _nq(friction_angle: float) -> float:
        num = np.exp(((3 * np.pi) / 2 - friction_angle) * np.tan(friction_angle))
        den = 2 * (np.cos(np.deg2rad(45) + (friction_angle / 2)) ** 2)

        return num / den

    @property
    def nq(self) -> float:
        r"""Terzaghi Bearing Capacity factor :math:`N_q`.

        .. math::

            \frac{e^{(\frac{3\pi}{2}-\phi)\tan\phi}}{2\cos^2\left(45^{\circ}+\frac{\phi}{2}\right)}

        :return: The bearing capacity factor :math:`N_q`
        :rtype: float
        """
        return np.round(self._nq(self.friction_angle), DECIMAL_PLACES)

    @property
    def nc(self) -> float:
        r"""Terzaghi Bearing Capacity factor :math:`N_c`.

        .. math::

            \cot \phi \left(N_q - 1 \right)

        :return: The bearing capacity factor :math:`N_c`
        :rtype: float
        """
        if np.isclose(self.friction_angle, 0.0):
            return 5.70

        _nc = (1 / np.tan(self.friction_angle)) * (self._nq(self.friction_angle) - 1)

        return np.round(_nc, DECIMAL_PLACES)

    @property
    def ngamma(self) -> float:
        r"""Terzaghi Bearing Capacity factor :math:`N_\gamma`.

        .. math::

            \frac{1}{2}\left(\frac{K_p}{\cos^2 \phi} - 1 \right)\tan \phi

        :return: The bearing capacity factor :math:`N_\gamma`
        :rtype: float
        """
        phi = np.rad2deg(self.friction_angle)
        num = passive_earth_pressure_coef(friction_angle=phi)
        den = np.cos(self.friction_angle) ** 2
        mid_expr = (num / den) - 1

        _ngamma = 0.5 * (mid_expr) * np.tan(self.friction_angle)

        return np.round(_ngamma, DECIMAL_PLACES)

    def qult_4_strip_footing(self) -> float:
        r"""Ultimate bearing capacity according to ``Terzaghi`` for ``strip footing``.

        .. math::

            q_u = cN_c + \gamma D_f N_q + 0.5 \gamma B N_\gamma

        :return: ultimate bearing capacity of the soil :math:`(q_{ult})`
        :rtype: float
        """
        qult = (
            product(self.cohesion, self.nc)
            + product(self.unit_weight_of_soil, self.foundation_depth, self.nq)
            + product(0.5, self.unit_weight_of_soil, self.foundation_width, self.ngamma)
        )

        return np.round(qult, DECIMAL_PLACES)

    def qult_4_square_foundation(self):
        r"""Ultimate bearing capacity according to ``Terzaghi`` for ``square footing``.

        .. math::

            q_u = 1.2cN_c + \gamma D_f N_q + 0.4 \gamma B N_\gamma

        :return: ultimate bearing capacity of the soil :math:`(q_{ult})`
        :rtype: float
        """
        qult = (
            product(1.2, self.cohesion, self.nc)
            + product(self.unit_weight_of_soil, self.foundation_depth, self.nq)
            + product(0.4, self.unit_weight_of_soil, self.foundation_width, self.ngamma)
        )

        return np.round(qult, DECIMAL_PLACES)

    def qult_4_circular_foundation(self):
        r"""Ultimate bearing capacity according to ``Terzaghi`` for ``circular footing``.

        .. math::

            q_u = 1.2cN_c + \gamma D_f N_q + 0.3 \gamma B N_{\gamma}

        :return: ultimate bearing capacity of the soil :math:`(q_{ult})`
        :rtype: float
        """
        qult = (
            product(1.2, self.cohesion, self.nc)
            + product(self.unit_weight_of_soil, self.foundation_depth, self.nq)
            + product(0.3, self.unit_weight_of_soil, self.foundation_width, self.ngamma)
        )

        return np.round(qult, DECIMAL_PLACES)


class Meyerhoff(BearingCapacityFactors):
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
        allow_settlement: float,
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
        :param allow_settlement: Tolerable settlement (mm)
        :type allow_settlement: float
        :raises AllowableSettlementError: Raised when `allow_settlement` is greater than `25.4mm`
        """
        if allow_settlement > self.ALLOWABLE_SETTLEMENT:
            raise AllowableSettlementError(
                f"allow_settlement: {allow_settlement} cannot be greater than 25.4mm"
            )

        self.n_design = n_design
        self.foundation_depth = foundation_depth
        self.foundation_width = foundation_width
        self.foundation_length = foundation_length
        self.friction_angle = friction_angle
        self.beta = beta
        self.allow_settlement = allow_settlement

    @classmethod
    def allow_bearing_capacity(
        cls,
        n_design: float,
        foundation_depth: float,
        foundation_width: float,
        allow_settlement: float,
    ) -> float:
        r"""Allowable bearing capacity :math:`q_{a(net)}` for a given tolerable
        settlement proposed by Meyerhoff.

        :return: Allowable bearing capacity.
        :rtype: float
        """

        if foundation_width <= 1.22:
            _allow_settlement = (
                19.16
                * n_design
                * depth_factor(foundation_depth, foundation_width)
                * (n_design / 25.4)
            )
            return round(_allow_settlement, DECIMAL_PLACES)

        _allow_settlement = (
            11.98
            * n_design
            * np.power((3.28 * foundation_width + 1) / (3.28 * foundation_width), 2)
            * depth_factor(foundation_depth, foundation_width)
            * (allow_settlement / 25.4)
        )
        return round(_allow_settlement, DECIMAL_PLACES)

    @staticmethod
    def _nq(friction_angle: float) -> float:
        return np.tan(np.deg2rad(45) + friction_angle / 2) * np.exp(
            np.pi * np.tan(friction_angle)
        )

    @classmethod
    @deg2rad
    def nq(cls, *, friction_angle: float) -> float:
        r"""Vesic Bearing Capacity factor :math:`N_q`.

        .. math::

            \tan^2 \left(45^{\circ} + \frac{\phi}{2} \right)e^{\pi \tan \phi}

        :param friction_angle: Internal angle of friction (degrees)
        :type friction_angle: float
        :return: A `float` representing the bearing capacity factor :math:`N_q`
        :rtype: float
        """
        _nq = cls._nq(friction_angle)
        return round(_nq, 2)

    @classmethod
    @deg2rad
    def nc(cls, *, friction_angle: float) -> float:
        """Vesic Bearing Capacity factor :math:`N_c`.

        .. math::


        :param friction_angle: Internal angle of friction (degrees)
        :type friction_angle: float
        :return: A `float` representing the bearing capacity factor :math:`N_c`
        :rtype: float
        """
        _nc = (1 / np.tan(friction_angle)) * (cls._nq(friction_angle) - 1)
        return round(_nc, 2)

    @classmethod
    @deg2rad
    def ngamma(cls, *, friction_angle: float) -> float:
        r"""Vesic Bearing Capacity factor :math:`N_\gamma`.

        :param friction_angle: Internal angle of friction (degrees)
        :type friction_angle: float
        :return: A `float` representing the bearing capacity factor :math:`N_\gamma`
        :rtype: float
        """
        _ngamma = 2 * (cls._nq(friction_angle) + 1) * np.tan(friction_angle)
        return np.round(_ngamma, DECIMAL_PLACES)

    @classmethod
    @deg2rad
    def sc(
        cls, foundation_width: float, foundation_length: float, *, friction_angle: float
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

    @staticmethod
    @deg2rad
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
