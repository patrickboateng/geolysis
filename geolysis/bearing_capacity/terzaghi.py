from geolysis import GeotechEng
from geolysis.bearing_capacity import FoundationSize, _base
from geolysis.utils import round_


class TerzaghiBearingCapacity(_base.Terzaghi):
    r"""Ultimate bearing capacity according to ``Terzaghi`` for
    ``strip``, ``square``, ``rectangular`` and ``circular footing``.

    :Example:


    :param cohesion: cohesion of foundation soil :math:`(kN/m^2)`
    :type cohesion: float
    :param friction_angle: internal angle of friction (degrees)
    :type soil_friction_angle: float
    :param soil_unit_weight: unit weight of soil :math:`(kN/m^3)`
    :type soil_unit_weight: float
    :param foundation_depth: depth of foundation :math:`d_f` (m)
    :type foundation_depth: float
    :param foundation_width: width of foundation (**B**) (m)
    :type foundation_width: float
    :param eng: specifies the type of ngamma formula to use. Available
                values are geolysis.MEYERHOF and geolysis.HANSEN
    :type eng: GeotechEng
    """

    def __init__(
        self,
        *,
        cohesion: float,
        soil_friction_angle: float,
        soil_unit_weight: float,
        foundation_size: FoundationSize,
        eng: GeotechEng = GeotechEng.MEYERHOF,
        local_shear: bool = False,
    ) -> None:
        super().__init__(
            cohesion=cohesion,
            soil_friction_angle=soil_friction_angle,
            soil_unit_weight=soil_unit_weight,
            foundation_size=foundation_size,
            eng=eng,
            local_shear=local_shear,
        )

    @property
    def _first_expr(self) -> float:
        return self.cohesion * self.nc

    @property
    def _mid_expr(self) -> float:
        return self.soil_unit_weight * self.foundation_size.depth * self.nq

    @property
    def _last_expr(self) -> float:
        return self.soil_unit_weight * self.foundation_size.width * self.ngamma

    @round_(precision=2)
    def ultimate_4_strip_footing(self) -> float:
        r"""Return ultimate bearing capacity of strip footings.

        .. math::

            q_u = c N_c + \gamma D_f N_q + 0.5 \gamma B N_\gamma
        """
        return self._first_expr + self._mid_expr + 0.5 * self._last_expr

    @round_(precision=2)
    def ultimate_4_square_footing(self) -> float:
        r"""Return ultimate bearing capacity for square footings.

        .. math::

            q_u = 1.3 c N_c + \gamma D_f N_q + 0.4 \gamma B N_\gamma
        """
        return self.ultimate_4_rectangular_footing()

    @round_(precision=2)
    def ultimate_4_circular_footing(self) -> float:
        r"""Return ultimate bearing capacity for circular footing.

        .. math::

            q_u = 1.3 c N_c + \gamma D_f N_q + 0.3 \gamma B N_\gamma
        """
        return 1.3 * self._first_expr + self._mid_expr + 0.3 * self._last_expr

    @round_(precision=2)
    def ultimate_4_rectangular_footing(self) -> float:
        r"""Return the ultimate bearing capacity for rectangular footing.

        .. math::

            q_u = \left( 1 + 0.3 \dfrac{B}{L} \right) N_c + \gamma D_f N_q
                  + \dfrac{1}{2} \left(1 - 0.2 \dfrac{B}{L} \right)
                  \gamma B N_\gamma
        """
        a = 1 + 0.3 * self.foundation_size.w2l
        b = 0.5 * (1 - 0.2 * self.foundation_size.w2l)

        return a * self._first_expr + self._mid_expr + b * self._last_expr
