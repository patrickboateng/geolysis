from geolysis.bearing_capacity import FootingShape, FoundationSize
from geolysis.exceptions import FootingShapeError
from geolysis.utils import PI, cot, exp, prod, round_, sin, tan


class VesicFactors:
    def __init__(
        self,
        soil_friction_angle: float,
        beta: float,
        foundation_size: FoundationSize,
        footing_shape: FootingShape,
    ) -> None:
        self.soil_friction_angle = soil_friction_angle
        self.beta = beta
        self.foundation_size = foundation_size
        self.footing_shape = footing_shape

    @property
    def nc(self) -> float:
        r"""Return ``Vesic`` bearing capacity factor :math:`N_c`.

        .. math::

            N_c = \cot \phi \cdot (N_q - 1)
        """
        return cot(self.soil_friction_angle) * (self.nq - 1)

    @property
    def nq(self) -> float:
        r"""Return ``Vesic`` bearing capacity factor :math:`N_q`.

        .. math::

            N_q = \tan^2 \left(45 + \frac{\phi}{2} \right)
                  \cdot (e^{\pi \tan \phi})

        """
        expr_1 = tan(45 + self.soil_friction_angle / 2) ** 2
        expr_2 = exp(PI * tan(self.soil_friction_angle))

        return expr_1 * expr_2

    @property
    def ngamma(self) -> float:
        r"""Return ``Vesic`` bearing capacity factor :math:`N_\gamma`.

        .. math::

            N_\gamma &= 2 \cdot (N_q + 1) \cdot \tan \phi`

        """
        return 2 * (self.nq + 1) * tan(self.soil_friction_angle)

    @property
    def _d2w(self) -> float:
        return self.foundation_size.d2w

    @property
    def dc(self) -> float:
        r"""Return ``Vesic`` depth factor :math:`d_c`.

        .. math::

            d_c = 1 + 0.4 \cdot \left(\frac{D_f}{B} \right)
        """
        return 1 + 0.4 * self._d2w

    @property
    def dq(self) -> float:
        r"""Return ``Vesic`` depth factor :math:`d_q`.

        .. math::

            d_q = 1 + 2 \cdot \tan \phi
                  \cdot (1 - \sin \phi)^2
                  \cdot \dfrac{D_f}{B}
        """
        a = 2 * tan(self.soil_friction_angle)
        b = (1 - sin(self.soil_friction_angle)) ** 2

        return 1 + a * b * self._d2w

    @property
    def dgamma(self) -> float:
        r"""Return ``Vesic`` depth factor :math:`d_\gamma`.

        .. math::

            d_\gamma = 1.0`

        """
        return 1.0

    @property
    def _w2l(self) -> float:
        return self.foundation_size.w2l

    @property
    def sc(self) -> float:
        r"""Return ``Vesic`` shape factor :math:`s_c`.

        - for strip footing |rarr| :math:`s_c = 1`
        - for rectangular footing |rarr| math:`s_c = 1 + \dfrac{B}{L} \cdot \dfrac{N_q}{N_c}`
        - for square or circular footing |rarr| :math:`s_c = 1 + \dfrac{N_q}{N_c}`
        """

        if self.footing_shape is FootingShape.STRIP:
            return 1.0

        if (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            return 1 + (self.nq / self.nc)

        if self.footing_shape is FootingShape.RECTANGULAR:
            return 1 + self._w2l * (self.nq / self.nc)

        msg = f"Footing shape should be one of the following: {FootingShape.STRIP}, \
                {FootingShape.SQUARE}, {FootingShape.RECTANGULAR}, and {FootingShape.CIRCULAR}"
        raise FootingShapeError(msg)

    @property
    def sq(self) -> float:
        r"""Return ``Vesic`` shape factor :math:`s_q`.

        - for strip footing |rarr| :math:`s_q = 1`
        - for rectangular footing |rarr| math:`s_q = 1 + \dfrac{B}{L} \cdot \tan \phi`
        - for square or circular footing |rarr| :math:`s_q = 1 + \tan \phi`
        """
        if self.footing_shape is FootingShape.STRIP:
            return 1.0

        if (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            return 1 + tan(self.soil_friction_angle)

        if self.footing_shape is FootingShape.RECTANGULAR:
            return 1 + self._w2l * tan(self.soil_friction_angle)

        msg = f"Footing shape should be one of the following: {FootingShape.STRIP}, \
                {FootingShape.SQUARE}, {FootingShape.RECTANGULAR}, and {FootingShape.CIRCULAR}"
        raise FootingShapeError(msg)

    @property
    def sgamma(self) -> float:
        r"""Return ``Vesic`` shape factor :math:`s_\gamma`.

        - for strip footing |rarr| :math:`s_\gamma = 1`
        - for rectangular footing |rarr| math:`s_\gamma = 1 - 0.4 \cdot \dfrac{B}{L}`
        - for square or circular footing |rarr| :math:`s_\gamma = 0.6`
        """

        if self.footing_shape is FootingShape.STRIP:
            return 1.0

        if (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            return 0.6

        if self.footing_shape is FootingShape.RECTANGULAR:
            return 1 - 0.4 * (self._w2l)

        msg = f"Footing shape should be one of the following: {FootingShape.STRIP}, \
                {FootingShape.SQUARE}, {FootingShape.RECTANGULAR}, and {FootingShape.CIRCULAR}"
        raise FootingShapeError(msg)

    @property
    def ic(self) -> float:
        r"""Return ``Vesic`` inclination factor :math:`i_c`.

        .. math::

            i_c = \left(1 - \frac{\beta}{90} \right)^2

        """
        return (1 - self.beta / 90) ** 2

    @property
    def iq(self) -> float:
        r"""Return ``Vesic`` inclination factor :math:`i_q`.

        .. math::

            i_q = \left(1 - \frac{\beta}{90} \right)^2

        """
        return self.ic

    @property
    def igamma(self) -> float:
        r"""Return ``Vesic`` inclination factor :math:`i_\gamma`.

        .. math::

            i_\gamma = \left(1 - \dfrac{\beta}{\phi} \right)^2

        """
        return (1 - self.beta / self.soil_friction_angle) ** 2


class VesicBearingCapacity:
    r"""Ultimate bearing capacity according to ``Vesic``.

    :param cohesion: Cohesion of foundation soil :math:`(kN/m^2)`
    :type cohesion: float
    :param unit_weight_of_soil: Unit weight of soil :math:`(kN/m^3)`
    :type unit_weight_of_soil: float
    :param foundation_size: Size of foundation
    :param friction_angle: Internal angle of friction (degrees)
    :type friction_angle: float
    ::param beta: Inclination of the load on the foundation with
                  respect to the vertical (degrees)
    :type beta: float
    :param total_vertical_load: total vertical load on foundation
    :type total_vertical_load: float
    :param footing_shape: Shape of the footing
    :type footing_shape: float
    """

    def __init__(
        self,
        cohesion: float,
        soil_unit_weight: float,
        foundation_size: FoundationSize,
        soil_friction_angle: float,
        beta: float,
        footing_shape: FootingShape = FootingShape.SQUARE,
    ) -> None:
        self.cohesion = cohesion
        self.soil_unit_weight = soil_unit_weight
        self.foundation_size = foundation_size
        self.soil_friction_angle = soil_friction_angle
        self.beta = beta
        self.footing_shape = footing_shape

        self._vesic_factors = VesicFactors(
            soil_friction_angle=self.soil_friction_angle,
            beta=self.beta,
            foundation_size=self.foundation_size,
            footing_shape=self.footing_shape,
        )

    @property
    def _first_expr(self) -> float:
        return self.cohesion * self.nc * self.sc * self.dc * self.ic

    @property
    def _mid_expr(self) -> float:
        return prod(
            self.soil_unit_weight,
            self.foundation_size.depth,
            self.nq,
            self.sq,
            self.dq,
            self.iq,
        )

    @property
    def _last_expr(self) -> float:
        return prod(
            self.soil_unit_weight,
            self.foundation_size.width,
            self.ngamma,
            self.sgamma,
            self.dgamma,
            self.igamma,
        )

    @round_(precision=2)
    def ultimate_bearing_capacity(self) -> float:
        r"""Return the ultimate bearing capacity according to ``Vesic``.

        .. math::

            q_u = c N_c s_c d_c i_c + q N_q s_q d_q i_q
                  + 0.5 \gamma B N_\gamma s_\gamma d_\gamma i_\gamma

        """
        return self._first_expr + self._mid_expr + 0.5 * self._last_expr

    @property
    def nc(self) -> float:
        return self._vesic_factors.nc

    @property
    def nq(self) -> float:
        return self._vesic_factors.nq

    @property
    def ngamma(self) -> float:
        return self._vesic_factors.ngamma

    @property
    def dc(self) -> float:
        return self._vesic_factors.dc

    @property
    def dq(self) -> float:
        return self._vesic_factors.dq

    @property
    def dgamma(self) -> float:
        return self._vesic_factors.dgamma

    @property
    def sc(self) -> float:
        return self._vesic_factors.sc

    @property
    def sq(self) -> float:
        return self._vesic_factors.sq

    @property
    def sgamma(self) -> float:
        return self._vesic_factors.sgamma

    @property
    def ic(self) -> float:
        return self._vesic_factors.ic

    @property
    def iq(self) -> float:
        return self._vesic_factors.iq

    @property
    def igamma(self) -> float:
        return self._vesic_factors.igamma
