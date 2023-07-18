from geolab.utils import round_, sin


@round_
def passive_earth_pressure_coef(friction_angle: float) -> float:
    r"""Coefficient of passive earth pressure :math:`K_p`.

    .. math::

        \dfrac{1 + \sin \phi}{1 - \sin \phi}

    :param friction_angle: internal angle of friction (degrees)
    :type friction_angle: float
    :return: passive earth pressure coefficient
    :rtype: float
    """
    return (1 + sin(friction_angle)) / (1 - sin(friction_angle))
