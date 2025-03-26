from abc import ABC

from geolysis.utils import cos, cot, deg2rad, exp, isclose, pi, round_, tan

from ._core import UltimateBearingCapacity

__all__ = ["TerzaghiUBC4StripFooting",
           "TerzaghiUBC4CircularFooting",
           "TerzaghiUBC4SquareFooting",
           "TerzaghiUBC4RectangularFooting"]


@round_(ndigits=2)
def n_c(friction_angle: float) -> float:
    if isclose(friction_angle, 0.0):
        return 5.7
    return cot(friction_angle) * (n_q(friction_angle) - 1.0)


@round_(ndigits=2)
def n_q(friction_angle: float) -> float:
    return (exp((3.0 * pi / 2.0 - deg2rad(friction_angle))
                * tan(friction_angle))
            / (2.0 * (cos(45.0 + friction_angle / 2.0)) ** 2.0))


@round_(ndigits=2)
def n_gamma(friction_angle: float) -> float:
    return (n_q(friction_angle) - 1.0) * tan(1.4 * friction_angle)


class TerzaghiUltimateBearingCapacity(UltimateBearingCapacity, ABC):

    @property
    def n_c(self) -> float:
        r"""Bearing capacity factor :math:`N_c`.

        :Equation:

        .. math:: N_c = \cot(\phi) \cdot (N_q - 1)
        """
        return n_c(self.friction_angle)

    @property
    def n_q(self) -> float:
        r"""Bearing capacity factor :math:`N_q`.

        :Equation:

        .. math::

            N_q = \dfrac{e^{(\frac{3\pi}{2} - \phi)\tan\phi}}
                      {2\cos^2(45 + \frac{\phi}{2})}
        """
        return n_q(self.friction_angle)

    @property
    def n_gamma(self) -> float:
        r"""Bearing capacity factor :math:`N_{\gamma}`.

        :Equation:

        .. math:: N_{\gamma} &=  (N_q - 1) \cdot \tan(1.4\phi)
        """
        return n_gamma(self.friction_angle)


class TerzaghiUBC4StripFooting(TerzaghiUltimateBearingCapacity):
    r"""Ultimate bearing capacity for strip footing according to
    ``Terzaghi 1943``.

    :Equation:

    .. math:: q_u = cN_c + qN_q + 0.5 \gamma BN_{\gamma}

    .. list-table::
       :widths: auto
       :header-rows: 1

       * - Symbol
         - Description
         - Unit
       * - :math:`q_u`
         - Ultimate bearing capacity
         - :math:`kPa`
       * - :math:`c`
         - Cohesion of soil
         - :math:`kPa`
       * - :math:`q`
         - Overburden pressure of soil
         - :math:`kPa`
       * - :math:`\gamma`
         - Unit weight of soil
         - :math:`kN/m^3`
       * - :math:`B`
         - Width of foundation footing
         - :math:`m`
       * - :math:`N_c`, :math:`N_q`, :math:`N_{\gamma}`
         - Bearing capacity factors
         - —
    """

    @round_(ndigits=2)
    def bearing_capacity(self) -> float:
        """Calculates ultimate bearing capacity for strip footing."""
        return (self._cohesion_term(1.0)
                + self._surcharge_term()
                + self._embedment_term(0.5))


class TerzaghiUBC4CircularFooting(TerzaghiUltimateBearingCapacity):
    r"""Ultimate bearing capacity for circular footing according to
    ``Terzaghi 1943``.

    :Equation:

    .. math:: q_u = 1.3cN_c + qN_q + 0.3 \gamma BN_{\gamma}

    .. list-table::
       :widths: auto
       :header-rows: 1

       * - Symbol
         - Description
         - Unit
       * - :math:`q_u`
         - Ultimate bearing capacity
         - :math:`kPa`
       * - :math:`c`
         - Cohesion of soil
         - :math:`kPa`
       * - :math:`q`
         - Overburden pressure of soil
         - :math:`kPa`
       * - :math:`\gamma`
         - Unit weight of soil
         - :math:`kN/m^3`
       * - :math:`B`
         - Width of foundation footing
         - :math:`m`
       * - :math:`N_c`, :math:`N_q`, :math:`N_{\gamma}`
         - Bearing capacity factors
         - —
    """

    @round_(ndigits=2)
    def bearing_capacity(self) -> float:
        """Calculates ultimate bearing capacity for circular footing."""
        return (self._cohesion_term(1.3)
                + self._surcharge_term()
                + self._embedment_term(0.3))


class TerzaghiUBC4RectangularFooting(TerzaghiUltimateBearingCapacity):
    r"""Ultimate bearing capacity for rectangular footing according to
    ``Terzaghi 1943``.

    :Equation:

    .. math::

            q_u = \left(1 + 0.3 \dfrac{B}{L} \right) c N_c + qN_q
                  + \left(1 - 0.2 \dfrac{B}{L} \right) 0.5 B \gamma N_{\gamma}

    .. list-table::
       :widths: auto
       :header-rows: 1

       * - Symbol
         - Description
         - Unit
       * - :math:`q_u`
         - Ultimate bearing capacity
         - :math:`kPa`
       * - :math:`c`
         - Cohesion of soil
         - :math:`kPa`
       * - :math:`q`
         - Overburden pressure of soil
         - :math:`kPa`
       * - :math:`\gamma`
         - Unit weight of soil
         - :math:`kN/m^3`
       * - :math:`B`
         - Width of foundation footing
         - :math:`m`
       * - :math:`L`
         - Length of foundation footing
         - :math:`m`
       * - :math:`N_c`, :math:`N_q`, :math:`N_{\gamma}`
         - Bearing capacity factors
         - —
    """

    @round_(ndigits=2)
    def bearing_capacity(self) -> float:
        """Calculates ultimate bearing capacity for rectangular footing."""
        width = self.foundation_size.width
        length = self.foundation_size.length
        coh_coef = 1.0 + 0.3 * (width / length)
        emb_coef = (1.0 - 0.2 * (width / length)) / 2.0

        return (self._cohesion_term(coh_coef)
                + self._surcharge_term()
                + self._embedment_term(emb_coef))


class TerzaghiUBC4SquareFooting(TerzaghiUBC4RectangularFooting):
    r"""Ultimate bearing capacity for square footing according to 
    ``Terzaghi 1943``.

    :Equation:

    .. math:: q_u = 1.3cN_c + qN_q + 0.4 \gamma BN_{\gamma}

    .. list-table::
       :widths: auto
       :header-rows: 1

       * - Symbol
         - Description
         - Unit
       * - :math:`q_u`
         - Ultimate bearing capacity
         - :math:`kPa`
       * - :math:`c`
         - Cohesion of soil
         - :math:`kPa`
       * - :math:`q`
         - Overburden pressure of soil
         - :math:`kPa`
       * - :math:`\gamma`
         - Unit weight of soil
         - :math:`kN/m^3`
       * - :math:`B`
         - Width of foundation footing
         - :math:`m`
       * - :math:`N_c`, :math:`N_q`, :math:`N_{\gamma}`
         - Bearing capacity factors
         - —
    """

    def bearing_capacity(self):
        """Calcalates ultimate bearing capacity for square footing.
        """
        return super().bearing_capacity()
