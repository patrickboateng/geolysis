from geolab import DECIMAL_PLACES
from geolab.utils import sin


def passive_earth_pressure_coef(friction_angle: float) -> float:
    r"""Coefficient of passive earth pressure :math:`K_p`.

    .. math::

        \dfrac{1 + \sin \phi}{1 - \sin \phi}

    :param friction_angle: Internal angle of friction (degrees)
    :type friction_angle: float
    :return: Passive earth pressure coefficient
    :rtype: float
    """
    phi = friction_angle
    kp = (1 + sin(phi)) / (1 - sin(phi))
    return round(kp, DECIMAL_PLACES)
