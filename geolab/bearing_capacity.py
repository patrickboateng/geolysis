"""This module provides functions for bearing capacity analysis."""

import numpy as np

from geolab import DECIMAL_PLACES, deg2rad, passive_earth_pressure_coef
from geolab.utils import product


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


class Terzaghi:
    """Terzaghi Bearing Capacity."""

    @staticmethod
    def _nq(friction_angle: float) -> float:
        num = np.exp(((3 * np.pi) / 2 - friction_angle) * np.tan(friction_angle))
        den = 2 * (np.cos(np.deg2rad(45) + (friction_angle / 2)) ** 2)

        return num / den

    @staticmethod
    @deg2rad("friction_angle")
    def nq(*, friction_angle: float) -> float:
        r"""Terzaghi Bearing Capacity factor :math:`N_q`.

        .. math::

            \frac{e^{(\frac{3\pi}{2} - \phi)\tan \phi}}{2 \cos^2 \left(45^{\circ} + \frac{\phi}{2} \right)}$$

        :param friction_angle: Internal angle of friction (degrees)
        :type friction_angle: float
        :return: The bearing capacity factor :math:`N_q`
        :rtype: float
        """
        return np.round(Terzaghi._nq(friction_angle), DECIMAL_PLACES)

    @staticmethod
    @deg2rad("friction_angle")
    def nc(*, friction_angle: float) -> float:
        r"""Terzaghi Bearing Capacity factor :math:`N_c`.

        .. math::

            \cot \phi \left(N_q - 1 \right)

        :param friction_angle: Internal angle of friction (degrees)
        :type friction_angle: float
        :return: The bearing capacity factor :math:`N_c`
        :rtype: float
        """
        if np.isclose(friction_angle, 0.0):
            return 5.70

        _nc = (1 / np.tan(friction_angle)) * (Terzaghi._nq(friction_angle) - 1)

        return np.round(_nc, DECIMAL_PLACES)

    @staticmethod
    @deg2rad("friction_angle")
    def ngamma(*, friction_angle: float) -> float:
        r"""Terzaghi Bearing Capacity factor :math:`N_\gamma`.

        .. math::

            \frac{1}{2}\left(\frac{K_p}{\cos^2 \phi} - 1 \right)\tan \phi

        :param friction_angle: Internal angle of friction (degrees)
        :type friction_angle: float
        :return: The bearing capacity factor :math:`N_\gamma`
        :rtype: float
        """
        phi = np.rad2deg(friction_angle)
        num = passive_earth_pressure_coef(friction_angle=phi)
        den = np.cos(friction_angle) ** 2
        mid_expr = (num / den) - 1

        _ngamma = 0.5 * (mid_expr) * np.tan(friction_angle)

        return np.round(_ngamma, DECIMAL_PLACES)

    @staticmethod
    def qult_4_strip_footing(
        cohesion: float,
        friction_angle: float,
        unit_weight_of_soil: float,
        foundation_depth: float,
        foundation_width: float,
    ) -> float:
        r"""Ultimate bearing capacity according to ``Terzaghi`` for ``strip footing``.

        .. math::

            q_u = cN_c + \gamma D_f N_q + 0.5 \gamma B N_\gamma

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
        qult = (
            product(cohesion, Terzaghi.nc(friction_angle=friction_angle))
            + product(
                unit_weight_of_soil,
                foundation_depth,
                Terzaghi.nq(friction_angle=friction_angle),
            )
            + product(
                0.5,
                unit_weight_of_soil,
                foundation_width,
                Terzaghi.ngamma(friction_angle=friction_angle),
            )
        )

        return np.round(qult, DECIMAL_PLACES)

    @staticmethod
    def qult_4_square_foundation(
        cohesion: float,
        friction_angle: float,
        unit_weight_of_soil: float,
        foundation_depth: float,
        foundation_width: float,
    ):
        r"""Ultimate bearing capacity according to ``Terzaghi`` for ``square footing``.

        .. math::

            q_u = 1.2cN_c + \gamma D_f N_q + 0.4 \gamma B N_\gamma

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
        qult = (
            product(1.2, cohesion, Terzaghi.nc(friction_angle=friction_angle))
            + product(
                unit_weight_of_soil,
                foundation_depth,
                Terzaghi.nq(friction_angle=friction_angle),
            )
            + product(
                0.4,
                unit_weight_of_soil,
                foundation_width,
                Terzaghi.ngamma(friction_angle=friction_angle),
            )
        )

        return np.round(qult, DECIMAL_PLACES)

    @staticmethod
    def qult_4_circular_foundation(
        cohesion: float,
        friction_angle: float,
        unit_weight_of_soil: float,
        foundation_depth: float,
        foundation_width: float,
    ):
        r"""Ultimate bearing capacity according to ``Terzaghi`` for ``circular footing``.

        .. math::

            q_u = 1.2cN_c + \gamma D_f N_q + 0.3 \gamma B N_{\gamma}

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
        qult = (
            product(1.2, cohesion, Terzaghi.nc(friction_angle=friction_angle))
            + product(
                unit_weight_of_soil,
                foundation_depth,
                Terzaghi.nq(friction_angle=friction_angle),
            )
            + product(
                0.3,
                unit_weight_of_soil,
                foundation_width,
                Terzaghi.ngamma(friction_angle=friction_angle),
            )
        )

        return np.round(qult, DECIMAL_PLACES)


# class M:
#     """Meyerhoff Bearing Capacity."""

#     ALLOWABLE_SETTLEMENT: float = 25.4

#     @staticmethod
#     def Qa(
#         Ndes: float, foundation_depth: float, foundation_width: float, Se: float
#     ) -> float:
#         r"""Allowable bearing capacity ($q_{a(net)}$) for a given tolerable
#         settlement proposed by Meyerhoff.

#         Args:
#             Ndes: Average corrected number of blows from `SPT N-value`.
#             foundation_depth: Depth of foundation (m).
#             foundation_width: width of foundation (m).
#             Se: tolerable settlement (mm).

#         Returns:
#             Allowable bearing capacity.

#         Raises:
#             exceptions.AllowableSettlementError: Raised when $S_e$ is greater than `25.4mm`.
#         """
#         if Se > M.ALLOWABLE_SETTLEMENT:
#             raise exceptions.AllowableSettlementError(
#                 f"Se: {Se} cannot be greater than 25.4mm"
#             )

#         if foundation_width <= 1.22:
#             return (
#                 19.16
#                 * Ndes
#                 * depth_factor(foundation_depth, foundation_width)
#                 * (Se / 25.4)
#             )

#         return (
#             11.98
#             * Ndes
#             * np.power((3.28 * foundation_width + 1) / (3.28 * foundation_width), 2)
#             * depth_factor(foundation_depth, foundation_width)
#             * (Se / 25.4)
#         )

#     @staticmethod
#     def _Nq(phi: float) -> float:
#         return np.tan(np.deg2rad(45) + phi / 2) * np.exp(np.pi * np.tan(phi))

#     @staticmethod
#     @deg2rad("phi")
#     def Nq(*, phi: float) -> float:
#         r"""Vesic Bearing Capacity factor $N_q$.

#         $$\tan^2 \left(45^{\circ} + \frac{\phi}{2} \right)e^{\pi \tan \phi}$$

#         Args:
#             phi: Internal angle of friction (degrees).

#         Returns:
#             A `float` representing the bearing capacity factor ($N_q$).

#         """
#         return np.round(M._Nq(phi), 2)

#     @staticmethod
#     @deg2rad("phi")
#     def Nc(*, phi: float) -> float:
#         """Vesic Bearing Capacity factor $N_c$.

#         Args:
#             phi: Internal angle of friction (degrees).

#         Returns:
#             A `float` representing the bearing capacity factor ($N_c$).

#         """
#         return np.round((1 / np.tan(phi)) * (M._Nq(phi) - 1), 2)

#     @staticmethod
#     @deg2rad("phi")
#     def Ngamma(*, phi: float) -> float:
#         r"""Vesic Bearing Capacity factor $N_{\gamma}$.

#         Args:
#             phi: Internal angle of friction (degrees).

#         Returns:
#             A `float` representing the bearing capacity factor ($N_{\gamma}$).

#         """
#         return np.round(2 * (M._Nq(phi) + 1) * np.tan(phi), 2)

#     @staticmethod
#     def Sc(foundation_width: float, foundation_length: float, phi: float) -> float:
#         """Shape factor ($S_c$).

#         Args:
#             foundation_width: foundation_width of foundation.
#             foundation_length: foundation_length of foundation.
#             phi: Internal angle of friction (degrees).

#         Returns:
#             A `float` representing the shape factor ($S_c$).

#         """
#         return 1 + ((foundation_width * M.Nq(phi)) / (foundation_length * M.Nc(phi)))

#     @staticmethod
#     @deg2rad("phi")
#     def Sq(foundation_width: float, foundation_length: float, *, phi: float) -> float:
#         """Shape factor ($S_q$).

#         Args:
#             foundation_width: foundation_width of foundation.
#             foundation_length: foundation_length of foundation.
#             phi: Internal angle of friction (degrees).

#         Returns:
#             A `float` representing the shape factor ($S_q$).

#         """
#         return 1 + ((foundation_width / foundation_length) * np.tan(phi))

#     @staticmethod
#     def Sgamma(foundation_width: float, foundation_length: float) -> float:
#         r"""Shape factor ($S_{\gamma}$).

#         Args:
#             foundation_width: foundation_width of foundation.
#             foundation_length: foundation_length of foundation.

#         Returns:
#             A `float` representing the shape factor ($S_{\gamma}$).

#         """
#         return 1 - 0.4 * (foundation_width / foundation_length)

#     @staticmethod
#     def _ic(beta: float) -> float:
#         return (1 - beta / 90) ** 2

#     @staticmethod
#     @deg2rad("beta")
#     def ic(*, beta: float) -> float:
#         """Inclination factor ($i_c$).

#         Args:
#             beta: inclination of the load on the foundation with
#                   respect to the vertical (degrees).

#         Returns:
#             A `float` representing the inclination factor ($i_c$).

#         """
#         return M._ic(beta)

#     @staticmethod
#     @deg2rad("beta")
#     def iq(beta: float) -> float:
#         """Inclination factor ($i_q$).

#         Args:
#             beta: inclination of the load on the foundation with
#                   respect to the vertical (degrees).

#         Returns:
#             A `float` representing the inclination factor ($i_q$).

#         """
#         return M._ic(beta)

#     @staticmethod
#     def igamma(beta: float, phi: float) -> float:
#         r"""Inclination factor ($i_{\gamma}$).

#         Args:
#             beta: inclination of the load on the foundation with
#                   respect to the vertical (degrees).
#             phi: internal angle of friction. (degrees)

#         Returns:
#             A `float` representing the inclination factor ($i_{\gamma}$).

#         """
#         return (1 - beta / phi) ** 2

#     @staticmethod
#     def dc(foundation_width: float, foundation_depth: float) -> float:
#         r"""Depth factor ($d_c$).

#         Args:
#             foundation_width: width of foundation.
#             foundation_depth: depth of foundation.

#         Returns:
#             A `float` representing the depth factor ($d_c$).

#         """
#         if foundation_depth / foundation_width <= 1:
#             return 1 + 0.4 * (foundation_depth / foundation_width)

#         return 1 + 0.4 * np.arctan(foundation_depth / foundation_width) * (np.pi / 180)

#     @staticmethod
#     @deg2rad("phi")
#     def dq(foundation_width: float, foundation_depth: float, *, phi: float) -> float:
#         r"""Depth factor ($d_q$).

#         Args:
#             foundation_width: width of foundation.
#             foundation_depth: depth of foundation
#             phi: internal angle of friction (degrees).

#         Returns:
#             A `float` representing the depth factor ($d_q$).

#         """

#         if foundation_depth / foundation_width <= 1:
#             return (
#                 1
#                 + 2
#                 * np.tan(phi)
#                 * ((1 - np.sin(phi)) ** 2)
#                 * foundation_depth
#                 / foundation_width
#             )

#         return 1 + 2 * np.tan(phi) * ((1 - np.sin(phi)) ** 2) * np.arctan(
#             foundation_depth / foundation_width
#         ) * (np.pi / 180)

#     @staticmethod
#     def dgamma() -> float:
#         r"""Depth factor ($d_{\gamma}$)

#         Returns:
#             A `float` representing the depth factor ($d_{\gamma}$).

#         """
#         return 1.0
