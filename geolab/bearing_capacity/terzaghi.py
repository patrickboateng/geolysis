import numpy as np

from geolab import DECIMAL_PLACES, deg2rad, passive_earth_pressure_coef
from geolab.bearing_capacity import BCF
from geolab.utils import product


class TerzaghiBCF(BCF):
    """Terzaghi Bearing Capacity Factors."""

    def __init__(self, friction_angle: float) -> None:
        """
        :param friction_angle: internal angle of friction :math:`(\phi)`
        :type friction_angle: float
        """
        self.friction_angle = friction_angle

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


class TBC:
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
        self.bcf = TerzaghiBCF(friction_angle)
        self.unit_weight_of_soil = unit_weight_of_soil
        self.foundation_depth = foundation_depth
        self.foundation_width = foundation_width

    @property
    def nq(self):
        return self.bcf.nq

    @property
    def nc(self):
        return self.bcf.nc

    @property
    def ngamma(self):
        return self.bcf.ngamma

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
