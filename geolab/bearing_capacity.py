"""This module provides functions for bearing capacity analysis."""


import numpy as np

from geolab import Kp, deg2rad, exceptions


def Ncor(Nr: int, gamma: float, spt_correction: str = "skempton") -> float:
    """SPT N-value correction.

    Args:
        Nr: Recorded SPT N-value.
        gamma: Effective overburden pressure ($kN/m^2$).
        spt_correction: The type of spt correction. `skempton` or `bazaraa`. Defaults to `skempton`.

    Returns:
        Corrected SPT N-value.
    """
    spt_correction = spt_correction.casefold()
    if spt_correction not in {"skempton", "bazaraa"}:
        raise exceptions.SPTCorrectionTypeError(
            f"SPT Correction should be skempton or bazaraa not {spt_correction}"
        )

    if spt_correction == "skempton":
        return (2 / (1 + 0.01044 * gamma)) * Nr

    if spt_correction == "bazaraa":
        if gamma < 71.8:
            return 4 * Nr / (1 + 0.0418 * gamma)
        if gamma > 71.8:
            return 4 * Nr / (3.25 + 0.0104 * gamma)

        return Nr


def Es(N60: float) -> float:
    r"""Elastic modulus of soil ($kN/m^2$).

    $$E_s = 320\left(N_{60} + 15 \right)$$

    Args:
        N60: The SPT N-value corrected for 60% hammer efficiency.

    Returns:
        Elastic modulus
    """

    return 320 * (N60 + 15)


class T:
    """Terzaghi Bearing Capacity."""

    @staticmethod
    def _Nq(phi: float) -> float:
        num = np.exp(
            ((3 * np.pi) / 2 - phi) * np.tan(phi)
        )  # The numerator of the formula
        den = 2 * (
            np.cos(np.deg2rad(45) + (phi / 2)) ** 2
        )  # The denominator of the formula

        return num / den

    @staticmethod
    @deg2rad
    def Nq(phi: float) -> float:
        r"""Terzaghi Bearing Capacity factor $N_q$.

        $$\frac{e^{(\frac{3\pi}{2} - \phi)\tan \phi}}{2 \cos^2 \left(45^{\circ} + \frac{\phi}{2} \right)}$$

        Args:
            phi: Internal angle of friction (degrees).

        Returns:
            A `float` representing the bearing capacity factor ($N_q$).

        """
        return np.round(T._Nq(phi), 2)

    @staticmethod
    @deg2rad
    def Nc(phi: float) -> float:
        r"""Terzaghi Bearing Capacity factor $N_c$.

        $$\cot \phi \left(N_q - 1 \right)$$

        Args:
            phi: Internal angle of friction (degrees).

        Returns:
            A `float` representing the bearing capacity factor $N_c$.

        """
        if np.isclose(phi, 0.0):
            return 5.70

        return np.round((1 / np.tan(phi)) * (T._Nq(phi) - 1), 2)

    @staticmethod
    @deg2rad
    def Ngamma(phi: float) -> float:
        r"""Terzaghi Bearing Capacity factor $N_\gamma$.

        $$\frac{1}{2}\left(\frac{K_p}{\cos^2 \phi} - 1 \right)\tan \phi$$

        - $K_p$ : coefficient of passive earth pressure.

        Args:
            phi: Internal angle of friction (degrees).

        Returns:
            A `float` representing the bearing capacity factor $N_\gamma$.

        """
        return 0.5 * ((Kp(np.rad2deg(phi)) / (np.cos(phi) ** 2)) - 1) * np.tan(phi)

    @staticmethod
    def qult_4_strip_footing(
        cohesion: float,
        phi: float,
        gamma: float,
        foundation_depth: float,
        foundation_width: float,
    ) -> float:
        r"""Ultimate bearing capacity according to `Terzaghi` for `strip footing`.

        Args:
            cohesion: cohesion of foundation soil ($kN/m^2$).
            phi: Internal angle of friction ($\phi$)
            gamma: Unit weight of soil ($kN/m^3$).
            foundation_depth: Foundation depth $D_f$ (m).
            foundation_width: Foundation width (**B**) (m)

        Returns:
            Ultimate bearing capacity ($q_{ult}$)

        """
        qult = (
            cohesion * T.Nc(phi)
            + gamma * foundation_depth * T.Nq(phi)
            + 0.5 * gamma * foundation_width * T.Ngamma(phi)
        )

        return np.round(qult, 2)

    @staticmethod
    def qult(
        cohesion: float,
        phi: float,
        gamma: float,
        foundation_depth: float,
        foundation_width: float,
        foundation_type: str = "square",
    ) -> float:
        r"""Ultimate bearing capacity according to `Terzaghi` for `square` and
        `circular` footing.

        Args:
            cohesion: cohesion of foundation soil ($kN/m^2$).
            phi: Internal angle of friction ($\phi$)
            gamma: Unit weight of soil ($kN/m^3$).
            foundation_depth: Foundation depth $D_f$ (m).
            foundation_width: Foundation width (**B**) (m)
            foundation_type: Determines the type of foundation. Defaults to `square`.
        Returns:
            Ultimate bearing capacity ($q_{ult}$)

        """
        if foundation_type not in {"square", "circular"}:
            raise exceptions.FoundationTypeError(
                f"Foundation type must be square or circular not {foundation_type}"
            )

        i = 0.4 if foundation_type in {"s", "square"} else 0.3

        qult = (
            1.2 * cohesion * T.Nc(phi)
            + gamma * foundation_depth * T.Nq(phi)
            + i * gamma * foundation_width * T.Ngamma(phi)
        )

        return np.round(qult, 2)


class M:
    """Meyerhoff Bearing Capacity."""

    ALLOWABLE_SETTLEMENT: float = 25.4

    @staticmethod
    def Fd(foundation_depth: float, foundation_width: float) -> float:
        """Depth Factor."""
        depth_factor = 1 + 0.33 * (foundation_depth / foundation_width)

        return depth_factor if depth_factor <= 1.33 else 1.33

    @staticmethod
    def Qa(
        Ndes: float, foundation_depth: float, foundation_width: float, Se: float
    ) -> float:
        r"""Allowable bearing capacity ($q_{a(net)}$) for a given tolerable
        settlement proposed by Meyerhoff.

        Args:
            Ndes: Average corrected number of blows from `SPT N-value`.
            foundation_depth: Depth of foundation (m).
            foundation_width: width of foundation (m).
            Se: tolerable settlement (mm).

        Returns:
            Allowable bearing capacity.

        Raises:
            exceptions.AllowableSettlementError: Raised when $S_e$ is greater than `25.4mm`.

        """

        if Se > M.ALLOWABLE_SETTLEMENT:
            raise exceptions.AllowableSettlementError(
                f"Se: {Se} cannot be greater than 25.4mm"
            )

        if foundation_width <= 1.22:
            return 19.16 * Ndes * M.Fd(foundation_depth, foundation_width) * (Se / 25.4)

        return (
            11.98
            * Ndes
            * np.power((3.28 * foundation_width + 1) / (3.28 * foundation_width), 2)
            * M.Fd(foundation_depth, foundation_width)
            * (Se / 25.4)
        )

    @staticmethod
    def _Nq(phi: float) -> float:
        return np.tan(np.deg2rad(45) + phi / 2) * np.exp(np.pi * np.tan(phi))

    @staticmethod
    @deg2rad
    def Nq(phi: float) -> float:
        r"""Vesic Bearing Capacity factor $N_q$.

        $$\tan^2 \left(45^{\circ} + \frac{\phi}{2} \right)e^{\pi \tan \phi}$$

        Args:
            phi: Internal angle of friction (degrees).

        Returns:
            A `float` representing the bearing capacity factor ($N_q$).

        """
        return np.round(M._Nq(phi), 2)

    @staticmethod
    @deg2rad
    def Nc(phi: float) -> float:
        """Vesic Bearing Capacity factor $N_c$.

        Args:
            phi: Internal angle of friction (degrees).

        Returns:
            A `float` representing the bearing capacity factor ($N_c$).

        """
        return np.round((1 / np.tan(phi)) * (M._Nq(phi) - 1), 2)

    @staticmethod
    @deg2rad
    def Ngamma(phi: float) -> float:
        r"""Vesic Bearing Capacity factor $N_{\gamma}$.

        Args:
            phi: Internal angle of friction (degrees).

        Returns:
            A `float` representing the bearing capacity factor ($N_{\gamma}$).

        """
        return np.round(2 * (M._Nq(phi) + 1) * np.tan(phi), 2)

    @staticmethod
    def Sc(foundation_width: float, foundation_length: float, phi: float) -> float:
        """Shape factor ($S_c$).

        Args:
            foundation_width: foundation_width of foundation.
            foundation_length: foundation_length of foundation.
            phi: Internal angle of friction (degrees).

        Returns:
            A `float` representing the shape factor ($S_c$).

        """
        return 1 + ((foundation_width * M.Nq(phi)) / (foundation_length * M.Nc(phi)))

    @staticmethod
    def Sq(foundation_width: float, foundation_length: float, phi: float) -> float:
        """Shape factor ($S_q$).

        Args:
            foundation_width: foundation_width of foundation.
            foundation_length: foundation_length of foundation.
            phi: Internal angle of friction (degrees).

        Returns:
            A `float` representing the shape factor ($S_q$).

        """
        return 1 + ((foundation_width / foundation_length) * np.tan(np.deg2rad(phi)))

    @staticmethod
    def Sgamma(foundation_width: float, foundation_length: float) -> float:
        r"""Shape factor ($S_{\gamma}$).

        Args:
            foundation_width: foundation_width of foundation.
            foundation_length: foundation_length of foundation.

        Returns:
            A `float` representing the shape factor ($S_{\gamma}$).

        """
        return 1 - 0.4 * (foundation_width / foundation_length)

    @staticmethod
    def _ic(beta: float) -> float:
        return (1 - beta / 90) ** 2

    @staticmethod
    @deg2rad
    def ic(beta: float) -> float:
        """Inclination factor ($i_c$).

        Args:
            beta: inclination of the load on the foundation with respect to the vertical (degrees).

        Returns:
            A `float` representing the inclination factor ($i_c$).

        """
        return M._ic(beta)

    @staticmethod
    def iq(beta: float) -> float:
        """Inclination factor ($i_q$).

        Args:
            beta: inclination of the load on the foundation with respect to the vertical (degrees).

        Returns:
            A `float` representing the inclination factor ($i_q$).

        """
        return M._ic(beta)

    @staticmethod
    def igamma(beta: float, phi: float) -> float:
        r"""Inclination factor ($i_{\gamma}$).

        Args:
            beta: inclination of the load on the foundation with respect to the vertical (degrees).
            phi: internal angle of friction.

        Returns:
            A `float` representing the inclination factor ($i_{\gamma}$).

        """
        return (1 - beta / phi) ** 2

    @staticmethod
    def dc(foundation_width: float, foundation_depth: float) -> float:
        r"""Depth factor ($d_c$).

        Args:
            foundation_width: width of foundation.
            foundation_depth: depth of foundation.

        Returns:
            A `float` representing the depth factor ($d_c$).

        """
        if foundation_depth / foundation_width <= 1:
            return 1 + 0.4 * (foundation_depth / foundation_width)

        return 1 + 0.4 * np.arctan(foundation_depth / foundation_width) * (np.pi / 180)

    @staticmethod
    def dq(foundation_width: float, foundation_depth: float, phi: float) -> float:
        r"""Depth factor ($d_q$).

        Args:
            foundation_width: width of foundation.
            foundation_depth: depth of foundation
            phi: internal angle of friction (degrees).

        Returns:
            A `float` representing the depth factor ($d_q$).

        """
        phi = np.deg2rad(phi)

        if foundation_depth / foundation_width <= 1:
            return (
                1
                + 2
                * np.tan(phi)
                * ((1 - np.sin(phi)) ** 2)
                * foundation_depth
                / foundation_width
            )

        return 1 + 2 * np.tan(phi) * ((1 - np.sin(phi)) ** 2) * np.arctan(
            foundation_depth / foundation_width
        ) * (np.pi / 180)

    @staticmethod
    def dgamma() -> float:
        r"""Depth factor ($d_{\gamma}$)

        Returns:
            A `float` representing the depth factor ($d_{\gamma}$).

        """
        return 1.0
