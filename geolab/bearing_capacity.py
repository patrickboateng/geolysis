"""This module provides functions for bearing capacity analysis."""

import numpy as np

from geolab import ERROR_TOLERANCE, deg2rad, exceptions, passive_earth_pressure_coef


def dilatancy_spt_correction(recorded_spt_nvalue: int) -> float:
    r"""SPT N-value Dilatancy Correction.

    **Dilatancy Correction** is a correction for silty fine sands and fine sands
    below the water table that develop pore pressure which is not easily
    dissipated. The pore pressure increases the resistance of the soil hence the
    penetration number (N).

    Correction of silty fine sands recommended by `Terzaghi and Peck (1967)` if
    $N_R$ exceeds 15.

    $N_c = 15 + \frac{1}{2}\left(N_R - 15\right)$ if $N_R \gt 15$

    $N_c = N_R$ if $N_R \le 15$

    Args:
        recorded_spt_nvalue: Recorded SPT N-value.

    Returns:
        Corrected SPT N-value.

    References:
        Arora, K 2003, _Soil Mechanics and Foundation Engineering_, 6 Edition,
        Standard Publishers Distributors, Delhi.
    """
    if recorded_spt_nvalue <= 15:
        corrected_spt_nvalue = recorded_spt_nvalue
        return corrected_spt_nvalue

    corrected_spt_nvalue = 15 + 0.5 * (recorded_spt_nvalue - 15)

    return np.round(corrected_spt_nvalue, 2)


def overburden_pressure_spt_correction(
    recorded_spt_nvalue: int, effective_overburden_pressure: float
):
    r"""SPT N-value Overburden Pressure Correction.

    In granular soils, the overburden pressure affects the penetration resistance.
    If two soils having same relative density but different confining pressures are tested,
    the one with a higher confining pressure gives a higher penetration number. As the
    confining pressure in cohesionless soils increases with the depth, the penetration number
    for soils at shallow depths is underestimated and that at greater depths is overestimated.
    For uniformity, the N-values obtained from field tests under different effective overburden pressures
    are corrected to a standard effective overburden pressure.
    `Gibbs and Holtz (1957)` recommend the use of the following equation for dry or moist clean sand.
    (Arora 2003, p. 428)

    $N = \dfrac{350}{\sigma_o + 70} \times N_R$ if $\sigma_o \le 280kN/m^2$

    !!! Note
        $\frac{N_c}{N_R}$ should lie between 0.45 and 2.0, if $\frac{N_c}{N_R}$ is greater than 2.0,
        $N_c$ should be divided by 2.0 to obtain the design value used in finding the bearing
        capacity of the soil. (Arora 2003, p. 428)

    Args:
        recorded_spt_nvalue: Recorded SPT N-value.
        effective_overburden_pressure: Effective overburden pressure. ($kN/m^2$)

    Returns:
        Corrected SPT N-value.

    References:
        Arora, K 2003, _Soil Mechanics and Foundation Engineering_, 6 edn,
        Standard Publishers Distributors, Delhi.
    """

    if effective_overburden_pressure > 280:
        raise ValueError(
            f"{effective_overburden_pressure} should be less than or equal to 280"
        )

    corrected_spt = recorded_spt_nvalue * (350 / (effective_overburden_pressure + 70))
    spt_ratio = corrected_spt / recorded_spt_nvalue

    if 0.45 < spt_ratio < 2.0:
        return corrected_spt

    if spt_ratio > 2.0:
        return corrected_spt / 2

    return corrected_spt


def skempton_spt_correction(
    recorded_spt_nvalue: int, effective_overburden_pressure: float
) -> float:
    r"""SPT N-value correction.

    $$N = \dfrac{2}{1 + 0.01044\sigma_o} \times N_R$$

    Args:
        recorded_spt_nvalue: Recorded SPT N-value.
        effective_overburden_pressure: Effective overburden pressure. ($kN/m^2$)

    Returns:
        Corrected SPT N-value.
    """
    first_expr = 2 / (1 + 0.01044 * effective_overburden_pressure)
    corrected_spt = first_expr * recorded_spt_nvalue

    return np.round(corrected_spt, 2)


def bazaraa_spt_correction(
    recorded_spt_nvalue: int, effective_overburden_pressure: float
) -> float:
    r"""SPT N-value correction.

    This is a correction given by `Bazaraa (1967)` and also by
    `Peck and Bazaraa (1969)` and it is one of the commonly used corrections.
    According to them:

    $N = \dfrac{4N_R}{1 + 0.0418\sigma_o}$ if $\sigma_o \lt 71.8kN/m^2$

    $N = \dfrac{4N_R}{3.25 + 0.0104\sigma_o}$ if $\sigma_o \gt 71.8kN/m^2$

    $N = N_R$ if $\sigma_o = 71.8kN/m^2$

    Args:
        recorded_spt_nvalue: Recorded SPT N-value.
        effective_overburden_pressure: Effective overburden pressure ($kN/m^2$).

    Returns:
        Corrected SPT N-value.
    """
    overburden_pressure = 71.8

    if np.isclose(
        effective_overburden_pressure, overburden_pressure, rtol=ERROR_TOLERANCE
    ):
        return recorded_spt_nvalue

    if effective_overburden_pressure < overburden_pressure:
        spt_correction = (
            4 * recorded_spt_nvalue / (1 + 0.0418 * effective_overburden_pressure)
        )
        return np.round(spt_correction, 2)

    spt_correction = (
        4 * recorded_spt_nvalue / (3.25 + 0.0104 * effective_overburden_pressure)
    )

    return np.round(spt_correction, 2)


def depth_factor(foundation_depth: float, foundation_width: float) -> float:
    r"""Depth Factor.

    $$k = 1 + 0.33 \frac{D_f}{B}$$

    Args:
        foundation_depth: Depth of foundation. (m)
        foundation_width: Width of foundation. (m)

    Returns:
        Depth factor.
    """
    _depth_factor = 1 + 0.33 * (foundation_depth / foundation_width)

    return _depth_factor if _depth_factor <= 1.33 else 1.33


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
        r"""Terzaghi Bearing Capacity factor $N_q$.

        $$\frac{e^{(\frac{3\pi}{2} - \phi)\tan \phi}}{2 \cos^2 \left(45^{\circ} + \frac{\phi}{2} \right)}$$

        Args:
            friction_angle: Internal angle of friction (degrees).

        Returns:
            A `float` representing the bearing capacity factor ($N_q$).

        """
        return np.round(Terzaghi._nq(friction_angle), 2)

    @staticmethod
    @deg2rad("friction_angle")
    def nc(*, friction_angle: float) -> float:
        r"""Terzaghi Bearing Capacity factor $N_c$.

        $$\cot \phi \left(N_q - 1 \right)$$

        Args:
            friction_angle: Internal angle of friction (degrees).

        Returns:
            A `float` representing the bearing capacity factor $N_c$.

        """
        if np.isclose(friction_angle, 0.0):
            return 5.70

        _nc = (1 / np.tan(friction_angle)) * (Terzaghi._nq(friction_angle) - 1)

        return np.round(_nc, 2)

    @staticmethod
    @deg2rad("friction_angle")
    def ngamma(*, friction_angle: float) -> float:
        r"""Terzaghi Bearing Capacity factor $N_\gamma$.

        $$\frac{1}{2}\left(\frac{K_p}{\cos^2 \phi} - 1 \right)\tan \phi$$

        Args:
            friction_angle: Internal angle of friction (degrees).

        Returns:
            A `float` representing the bearing capacity factor $N_\gamma$.

        """
        phi = np.rad2deg(friction_angle)
        num = passive_earth_pressure_coef(friction_angle=phi)
        den = np.cos(friction_angle) ** 2
        mid_expr = (num / den) - 1

        _ngamma = 0.5 * (mid_expr) * np.tan(friction_angle)

        return np.round(_ngamma, 2)

    @staticmethod
    def qult_4_strip_footing(
        cohesion: float,
        friction_angle: float,
        unit_weight_of_soil: float,
        foundation_depth: float,
        foundation_width: float,
    ) -> float:
        r"""Ultimate bearing capacity according to `Terzaghi` for `strip footing`.

        $$q_u = cN_c + \gamma D_f N_q + 0.5 \gamma B N_{\gamma}$$

        Args:
            cohesion: cohesion of foundation soil ($kN/m^2$).
            friction_angle: Internal angle of friction ($\phi$)
            unit_weight_of_soil: Unit weight of soil ($kN/m^3$).
            foundation_depth: Foundation depth $D_f$ (m).
            foundation_width: Foundation width (**B**) (m)

        Returns:
            Ultimate bearing capacity ($q_{ult}$)

        """
        overburden_pressure = unit_weight_of_soil * foundation_depth
        first_expr = cohesion * Terzaghi.nc(friction_angle=friction_angle)
        mid_expr = overburden_pressure * Terzaghi.nq(friction_angle=friction_angle)
        last_expr = (
            0.5
            * unit_weight_of_soil
            * foundation_width
            * Terzaghi.ngamma(friction_angle=friction_angle)
        )

        qult = first_expr + mid_expr + last_expr

        return np.round(qult, 2)

    @staticmethod
    def qult_4_foundation(
        cohesion: float,
        friction_angle: float,
        unit_weight_of_soil: float,
        foundation_depth: float,
        foundation_width: float,
        shape: str = "square",
    ) -> float:
        r"""Ultimate bearing capacity according to `Terzaghi` for `square` and
            `circular` footing.

        `square` $\rightarrow q_u = 1.2cN_c + \gamma D_f N_q + 0.4 \gamma B N_{\gamma}$

        `circular` $\rightarrow q_u = 1.2cN_c + \gamma D_f N_q + 0.3 \gamma B N_{\gamma}$

        Args:
            cohesion: cohesion of foundation soil. ($kN/m^2$)
            friction_angle: Internal angle of friction. ($\phi$)
            unit_weight_of_soil: Unit weight of soil. ($kN/m^3$)
            foundation_depth: Foundation depth $D_f$. (m)
            foundation_width: Foundation width (**B**). (m)
            shape: Determines the shape of the foundation. `square` or `circular`.
                   Defaults to `square`.
        Returns:
            Ultimate bearing capacity ($q_{ult}$)

        Raises:
            exceptions.FoundationTypeError: Exception raised when an invalid foundation shape
                                            is specified.
        """
        if shape == "square":
            i = 0.4
        elif shape == "circular":
            i = 0.3
        else:
            raise exceptions.FoundationTypeError(
                f"Foundation type must be square or circular not {shape}"
            )

        overburden_pressure = unit_weight_of_soil * foundation_depth
        first_expr = 1.2 * cohesion * Terzaghi.nc(friction_angle=friction_angle)
        mid_expr = overburden_pressure * Terzaghi.nq(friction_angle=friction_angle)
        last_expr = (
            i
            * unit_weight_of_soil
            * foundation_width
            * Terzaghi.ngamma(friction_angle=friction_angle)
        )

        qult = first_expr + mid_expr + last_expr

        return np.round(qult, 2)


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
