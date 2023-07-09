"""Terzaghi Bearing Capacity Analysis."""

from dataclasses import dataclass, field
from typing import Union

from geolab import DECIMAL_PLACES, GeotechEng
from geolab.utils import cos, exp, PI, mul, tan, deg2rad


@dataclass
class TerzaghiBCF:
    """Terzaghi Bearing Capacity Factors."""

    nc: float = field(init=False)
    nq: float = field(init=False)
    ngamma: float = field(init=False)

    def __init__(
        self,
        friction_angle: float,
        eng: GeotechEng = GeotechEng.MEYERHOF,
    ):
        num = exp(
            ((3 * PI) / 2 - deg2rad(friction_angle)) * tan(friction_angle)
        )
        den = 2 * (cos(45 + (friction_angle / 2)) ** 2)

        self.nq = num / den
        self.nc = (1 / tan(friction_angle)) * (self.nq - 1)

        if eng is GeotechEng.MEYERHOF:
            self.ngamma = (self.nq - 1) * tan(1.4 * friction_angle)
        elif eng is GeotechEng.HANSEN:
            self.ngamma = 1.8 * (self.nq - 1) * tan(friction_angle)
        else:
            msg = f"Available types are {GeotechEng.MEYERHOF} or {GeotechEng.HANSEN}"
            raise TypeError(msg)


class TerzaghiBearingCapacity:
    """Terzaghi Bearing Capacity."""

    def __init__(
        self,
        cohesion: float,
        friction_angle: float,
        unit_weight_of_soil: float,
        foundation_depth: float,
        foundation_width: float,
        eng: GeotechEng = GeotechEng.MEYERHOF,
    ) -> None:
        """
        :param cohesion: cohesion of foundation soil :math:`(kN/m^2)`
        :type cohesion: float
        :param friction_angle: internal angle of friction (degrees)
        :type friction_angle: float
        :param unit_weight_of_soil: unit weight of soil :math:`(kN/m^3)`
        :type unit_weight_of_soil: float
        :param foundation_depth: depth of foundation :math:`d_f` (m)
        :type foundation_depth: float
        :param foundation_width: width of foundation (**B**) (m)
        :type foundation_width: float
        :param eng: specifies the type of ngamma formula to use. Available
                    values are geolab.MEYERHOF and geolab.HANSEN
        :type eng: GeotechEng
        """
        self.cohesion = cohesion
        self.gamma = unit_weight_of_soil
        self.fd = foundation_depth
        self.fw = foundation_width
        self.bearing_cap_factors = TerzaghiBCF(friction_angle, eng)

    @property
    def nc(self) -> float:
        r"""Terzaghi Bearing Capacity factor :math:`N_c`.

        .. math::

            N_c = \cot \phi \left(N_q - 1 \right)

        :return: The bearing capacity factor :math:`N_c`
        :rtype: float
        """
        return self.bearing_cap_factors.nc

    @nc.setter
    def nc(self, val: Union[int, float]):
        self.bearing_cap_factors.nc = val

    @property
    def nq(self) -> float:
        r"""Terzaghi Bearing Capacity factor :math:`N_q`.

        .. math::

            N_q=\dfrac{e^{(\frac{3\pi}{2}-\phi)\tan\phi}}{2\cos^2\left(45^{\circ}+\frac{\phi}{2}\right)}

        :return: The bearing capacity factor :math:`N_q`
        :rtype: float
        """
        return self.bearing_cap_factors.nq

    @nq.setter
    def nq(self, val: Union[int, float]):
        self.bearing_cap_factors.nq = val

    @property
    def ngamma(self) -> float:
        r"""Terzaghi Bearing Capacity factor :math:`N_\gamma`.

        .. note::

            Exact values of :math:`N_\gamma` are not directly obtainable; values have
            been proposed by ``Brinch Hansen (1968)`` which are widely used in Europe,
            and also by ``Meyerhof (1963)``, which have been adopted in North America.

        The formulas shown below are ``Brinch Hansen`` and ``Meyerhof`` respectively.

        .. math::

            N_\gamma = 1.8 \left(N_q - 1 \right) \tan \phi

            N_\gamma = \left(N_q -1 \right)\tan(1.4\phi)

        :return: The bearing capacity factor :math:`N_\gamma`
        :rtype: float
        """
        return self.bearing_cap_factors.ngamma

    @ngamma.setter
    def ngamma(self, val: Union[int, float]):
        self.bearing_cap_factors.ngamma = val

    def qult_4_strip_footing(self) -> float:
        r"""Ultimate bearing capacity according to ``Terzaghi`` for ``strip footing``.

        .. math::

            q_u = cN_c + \gamma D_f N_q + 0.5 \gamma B N_\gamma

        :return: ultimate bearing capacity of the soil :math:`(q_{ult})`
        :rtype: float
        """
        qult = (
            mul(self.cohesion, self.nc)
            + mul(self.gamma, self.fd, self.nq)
            + mul(0.5, self.gamma, self.fw, self.ngamma)
        )

        return round(qult, DECIMAL_PLACES)

    def qult_4_square_footing(self):
        r"""Ultimate bearing capacity according to ``Terzaghi`` for ``square footing``.

        .. math::

            q_u = 1.2cN_c + \gamma D_f N_q + 0.4 \gamma B N_\gamma

        :return: ultimate bearing capacity of the soil :math:`(q_{ult})`
        :rtype: float
        """
        qult = (
            mul(1.2, self.cohesion, self.nc)
            + mul(self.gamma, self.fd, self.nq)
            + mul(0.4, self.gamma, self.fw, self.ngamma)
        )

        return round(qult, DECIMAL_PLACES)

    def qult_4_circular_footing(self):
        r"""Ultimate bearing capacity according to ``Terzaghi`` for ``circular footing``.

        .. math::

            q_u = 1.2cN_c + \gamma D_f N_q + 0.3 \gamma B N_{\gamma}

        :return: ultimate bearing capacity of the soil :math:`(q_{ult})`
        :rtype: float
        """
        qult = (
            mul(1.2, self.cohesion, self.nc)
            + mul(self.gamma, self.fd, self.nq)
            + mul(0.3, self.gamma, self.fw, self.ngamma)
        )

        return round(qult, DECIMAL_PLACES)
