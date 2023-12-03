from abc import ABC, abstractmethod

from geolysis import GeotechEng
from geolysis.bearing_capacity import FoundationSize
from geolysis.utils import PI, arctan, cos, cot, deg2rad, exp, round_, tan


def _local_shear(
    cohesion: float,
    soil_friction_angle: float,
) -> tuple[float, float]:
    cohesion = (2 / 3) * cohesion
    soil_friction_angle = arctan((2 / 3) * tan(soil_friction_angle))

    return (cohesion, soil_friction_angle)


class Terzaghi(ABC):
    def __init__(
        self,
        *,
        cohesion: float,
        soil_friction_angle: float,
        soil_unit_weight: float,
        foundation_size: FoundationSize,
        eng: GeotechEng,
        local_shear: bool,
    ) -> None:
        if local_shear:
            self.cohesion, self.soil_friction_angle = _local_shear(
                cohesion,
                soil_friction_angle,
            )

        else:
            self.cohesion = cohesion
            self.soil_friction_angle = soil_friction_angle

        self.soil_unit_weight = soil_unit_weight
        self.foundation_size = foundation_size
        self.eng = eng
        self.local_shear = local_shear

    @abstractmethod
    @round_(precision=2)
    def ultimate_4_strip_footing(self) -> float:
        ...

    @abstractmethod
    @round_(precision=2)
    def ultimate_4_square_footing(self) -> float:
        ...

    @abstractmethod
    @round_(precision=2)
    def ultimate_4_circular_footing(self) -> float:
        ...

    @abstractmethod
    @round_(precision=2)
    def ultimate_4_rectangular_footing(self) -> float:
        ...

    @property
    @round_(precision=2)
    def nc(self) -> float:
        r"""Return ``Terzaghi`` bearing capacity factor :math:`N_c`.

        .. math::

            N_c = \cot \phi \left(N_q - 1 \right)

        """
        return cot(self.soil_friction_angle) * (self.nq - 1)

    @property
    @round_(precision=2)
    def nq(self) -> float:
        r"""Return ``Terzaghi`` bearing capacity factor :math:`N_q`.

        .. math::

            N_q = \dfrac{e^{(\frac{3\pi}{2}-\phi)\tan\phi}}
                  {2\cos^2\left(45^{\circ}+\frac{\phi}{2}\right)}
        """

        a = (3 * PI) / 2 - deg2rad(self.soil_friction_angle)
        b = a * tan(self.soil_friction_angle)

        return exp(b) / (2 * (cos(45 + (self.soil_friction_angle / 2)) ** 2))

    @property
    @round_(precision=2)
    def ngamma(self) -> float:
        r"""Return ``Terzaghi`` bearing capacity factor :math:`N_\gamma`.

        The formulas shown below are ``Meyerhof`` and ``Brinch Hansen`` rspectively.

        .. math::

            N_\gamma &= (N_q -1) \tan(1.4 \phi)

            N_\gamma &= 1.8 (N_q - 1) \tan \phi


        .. note::

            Exact values of :math:`N_\gamma` are not directly obtainable; values have
            been proposed by ``Brinch Hansen (1968)`` which are widely used in Europe,
            and also by ``Meyerhof (1963)``, which have been adopted in North America.
        """

        if self.eng is GeotechEng.MEYERHOF:
            return (self.nq - 1) * tan(1.4 * self.soil_friction_angle)

        if self.eng is GeotechEng.HANSEN:
            return 1.8 * (self.nq - 1) * tan(self.soil_friction_angle)

        msg = (
            f"Available types are {GeotechEng.MEYERHOF} or {GeotechEng.HANSEN}"
        )
        raise TypeError(msg)
