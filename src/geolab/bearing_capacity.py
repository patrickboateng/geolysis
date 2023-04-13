import functools
import math


def _phi_to_radians(func):
    @functools.wraps(func)
    def wrapper(phi):
        phi = math.radians(phi)
        return func(phi)

    return wrapper


@_phi_to_radians
def Kp(phi: float) -> float:
    """Coeffiecient of passive earth pressure ($K_p$).

    Args:
        phi: Internal angle of friction (degrees).

    Returns:
        Passive earth pressure coefficient.
    """
    return (1 + math.sin(phi)) / (1 - math.sin(phi))


@_phi_to_radians
def Nq(phi: float) -> float:
    """Terzaghi Bearing Capacity factor $N_q$.

    Args:
        phi: Internal angle of friction (degrees).

    Returns:
        A `float` describing the bearing capacity factor ($N_q$).
    """
    numerator = math.exp(((3 * math.pi) / 2 - phi) * math.tan(phi))
    denominator = 2 * math.pow(math.cos(math.radians(45) + (phi / 2)), 2)

    return round(numerator / denominator, 5)


@_phi_to_radians
def Ngamma(phi: float) -> float:
    r"""Terzaghi Bearing Capacity factor $N_\gamma$.

    Args:
        phi: Internal angle of friction (degrees).

    Returns:
        A `float` describing the bearing capacity factor $N_\gamma$.
    """
    return round(
        0.5 * (Kp(math.degrees(phi)) / math.cos(phi) ** 2 - 1) * math.tan(phi), 5
    )


@_phi_to_radians
def Nc(phi: float) -> float:
    """Terzaghi Bearing Capacity factor $N_c$.

    Args:
        phi: Internal angle of friction (degrees).

    Returns:
        A `float` describing the bearing capacity factor $N_c$.
    """
    if math.isclose(phi, 0.0):
        return 5.70

    return round((1 / math.tan(phi)) * (Nq(math.degrees(phi)) - 1), 5)


def q_ult_terzaghi(
    cohesion: float,
    gamma: float,
    depth_of_foundation: float,
    width_of_foundation: float,
) -> float:
    """Ultimate bearing capacity according to `Terzaghi`.

    Args:
        cohesion: cohesion of foundation soil ($kN/m^2$).
        gamma: Unit weight of soil ($kN/m^3$).
        depth_of_foundation: Foundation depth (m).
        width_of_foundation: Foundation width (m)

    Returns:
        Ultimate bearing capacity ($q_{ult}$)
    """
