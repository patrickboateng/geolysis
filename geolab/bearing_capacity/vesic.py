"""Vesic Bearing Capacity Analysis."""

from dataclasses import dataclass, field
from typing import Optional, Union


from geolab import DECIMAL_PLACES
from geolab.bearing_capacity import (
    FootingShape,
    _check_footing_dimension,
    _check_footing_shape,
)
from geolab.utils import exp, PI, tan, mul, sin


@dataclass
class VesicBCF:
    """Vesic Bearing Capacity Factors."""

    nc: float = field(init=False)
    nq: float = field(init=False)
    ngamma: float = field(init=False)

    def __init__(self, friction_angle: float) -> None:
        self.nq = tan(45 + friction_angle / 2) ** 2 * exp(
            PI * tan(friction_angle)
        )
        self.nc = (1 / tan(friction_angle)) * (self.nq - 1)
        self.ngamma = 2 * (self.nq + 1) * tan(friction_angle)


@dataclass
class VesicShapeFactors:
    """Vesic Shape Factors."""

    sc: float = field(init=False)
    sq: float = field(init=False)
    sgamma: float = field(init=False)

    def __init__(
        self,
        footing_shape: FootingShape,
        nq: float,
        nc: float,
        friction_angle: float,
        foundation_width: Optional[float] = None,
        foundation_length: Optional[float] = None,
    ) -> None:
        _check_footing_shape(footing_shape)

        if footing_shape is FootingShape.STRIP_FOOTING:
            self.sc = 1.0
            self.sq = 1.0
            self.sgamma = 1.0

        elif footing_shape is FootingShape.RECTANGULAR_FOOTING:
            _check_footing_dimension(foundation_width, foundation_length)
            w2l = foundation_width / foundation_length

            self.sc = 1 + (w2l) * (nq / nc)
            self.sq = 1 + (w2l) * tan(friction_angle)
            self.sgamma = 1 - 0.4 * (w2l)

        else:
            self.sc = 1 + (nq / nc)
            self.sq = 1 + tan(friction_angle)
            self.sgamma = 0.6


@dataclass
class VesicDepthFactors:
    """Vesic Depth Factors."""

    dc: float = field(init=False)
    dq: float = field(init=False)
    dgamma: float = field(init=False)

    def __init__(
        self,
        foundation_depth: float,
        foundation_width: float,
        friction_angle: float,
    ) -> None:
        d2w = foundation_depth / foundation_width
        self.dc = 1 + 0.4 * d2w
        self.dq = (
            1 + 2 * tan(friction_angle) * (1 - sin(friction_angle)) ** 2 * d2w
        )
        self.dgamma = 1.0


@dataclass
class VesicInclinationFactors:
    """Vesic Inclination Factors."""

    ic: float = field(init=False)
    iq: float = field(init=False)
    igamma: float = field(init=False)

    def __init__(self, beta: float, friction_angle: float) -> None:
        self.ic = (1 - beta / 90) ** 2
        self.iq = self.ic
        self.igamma = (1 - beta / friction_angle) ** 2


class VesicBearingCapacity:
    """Vesic Bearing Capacity."""

    def __init__(
        self,
        cohesion: float,
        unit_weight_of_soil: float,
        foundation_depth: float,
        foundation_width: float,
        foundation_length: float,
        friction_angle: float,
        beta: float,
        footing_shape: FootingShape = FootingShape.SQUARE_FOOTING,
    ) -> None:
        """
        :param cohesion: cohesion of foundation soil :math:`(kN/m^2)`
        :type cohesion: float
        :param unit_weight_of_soil: unit weight of soil :math:`(kN/m^3)`
        :type unit_weight_of_soil: float
        :param foundation_depth: depth of foundation (m)
        :type foundation_depth: float
        :param foundation_width: width of foundation (m)
        :type foundation_width: float
        :param foundation_length: length of foundation (m)
        :type foundation_length: float
        :param friction_angle: internal angle of friction (degrees)
        :type friction_angle: float
        ::param beta: inclination of the load on the foundation with
                      respect to the vertical (degrees)
        :type beta: float
        :param total_vertical_load: total vertical load on foundation
        :type total_vertical_load: float
        :param footing_shape: shape of the footing
        :type footing_shape: float
        """
        self.cohesion = cohesion
        self.gamma = unit_weight_of_soil
        self.fd = foundation_depth
        self.fw = foundation_width
        self.fl = foundation_length

        self.bearing_cap_factors = VesicBCF(friction_angle)
        self.shape_factors = VesicShapeFactors(
            footing_shape,
            self.nq,
            self.nc,
            self.fw,
            self.fl,
            friction_angle,
        )
        self.depth_factors = VesicDepthFactors(
            self.fd, self.fw, friction_angle
        )
        self.incl_factors = VesicInclinationFactors(beta, friction_angle)

    def ultimate_bearing_capacity(self) -> float:
        r"""Ultimate bearing capacity according to ``Vesic``.

        .. math::

            q_u = c N_c S_c d_c i_c + q N_q S_q d_q i_q + 0.5 \gamma B N_\gamma S_\gamma d_\gamma i_\gamma

        :return: ultimate bearing capacity
        :rtype: float
        """
        expr_1 = mul(self.cohesion, self.nc, self.sc, self.dc, self.ic)
        expr_2 = mul(self.gamma, self.fd, self.nq, self.sq, self.dq, self.iq)
        expr_3 = mul(
            self.gamma,
            self.fw,
            self.ngamma,
            self.sgamma,
            self.dgamma,
            self.igamma,
        )
        qult = expr_1 + expr_2 + 0.5 * expr_3

        return round(qult, DECIMAL_PLACES)

    @property
    def nc(self) -> float:
        r"""Vesic Bearing Capacity factor :math:`N_c`.

        .. math::

            N_c = (N_q - 1) \cot \phi

        :return: A `float` representing the bearing capacity factor :math:`N_c`
        :rtype: float
        """
        return round(self.bearing_cap_factors.nc, DECIMAL_PLACES)

    @nc.setter
    def nc(self, val: Union[int, float]):
        self.bearing_cap_factors.nc = val

    @property
    def nq(self) -> float:
        r"""Vesic Bearing Capacity factor :math:`N_q`.

        .. math::

            N_q = \tan^2 (45 + \frac{\phi}{2})(e^{\pi \tan \phi})

        :return: A `float` representing the bearing capacity factor :math:`N_q`
        :rtype: float
        """
        return round(self.bearing_cap_factors.nq, DECIMAL_PLACES)

    @nq.setter
    def nq(self, val: Union[int, float]):
        self.bearing_cap_factors.nq = val

    @property
    def ngamma(self) -> float:
        r"""Vesic Bearing Capacity factor :math:`N_\gamma`.

        .. math::

            N_\gamma = 2(N_q + 1) \tan \phi

        :return: A `float` representing the bearing capacity factor :math:`N_\gamma`
        :rtype: float
        """
        return round(self.bearing_cap_factors.ngamma, DECIMAL_PLACES)

    @ngamma.setter
    def ngamma(self, val: Union[int, float]):
        self.bearing_cap_factors.ngamma = val

    @property
    def dc(self) -> float:
        r"""Depth factor :math:`d_c`.

        .. math::

            d_q = 1 + 0.4 (\frac{D_f}{B})

        :return: A `float` representing the depth factor :math:`d_c`
        :rtype: float
        """
        return round(self.depth_factors.dc, DECIMAL_PLACES)

    @dc.setter
    def dc(self, val: Union[int, float]):
        self.depth_factors.dc = val

    @property
    def dq(self) -> float:
        r"""Depth factor :math:`d_q`.

        .. math::

            d_q = 1 + 2 \tan \phi (1 - \sin \phi)^2 \frac{D_f}{B}

        :return: A `float` representing the depth factor :math:`d_q`
        :rtype: float
        """
        return round(self.depth_factors.dq, DECIMAL_PLACES)

    @dq.setter
    def dq(self, val: Union[int, float]):
        self.depth_factors.dq = val

    @property
    def dgamma(self) -> float:
        r"""Depth factor :math:`d_\gamma`.

        .. math::

            d_\gamma = 1.0

        :return: 1.0
        :rtype: float
        """
        return round(self.depth_factors.dgamma, DECIMAL_PLACES)

    @dgamma.setter
    def dgamma(self, val: Union[int, float]):
        self.depth_factors.dgamma = val

    @property
    def sc(self) -> float:
        r"""Shape factor :math:`S_c`.

        .. math::

            if \, footing \, shape \, is \, continuous(strip):
                S_c = 1

            if \, footing \, shape \, is \, rectangular:
                S_c = 1 + \frac{B}{L} \frac{N_q}{N_c}

            if \, footing \, shape \, is \, square \, or \, circular:
                S_c = 1 + (\frac{N_q}{N_c})

        :return: A `float` representing the shape factor :math:`S_c`
        :rtype: float
        """
        return round(self.shape_factors.sc, DECIMAL_PLACES)

    @sc.setter
    def sc(self, val: Union[int, float]):
        self.shape_factors.sc = val

    @property
    def sq(self) -> float:
        r"""Shape factor :math:`S_q`.

        .. math::

            if \, footing \, shape \, is \, continuous(strip):
                S_q = 1

            if \, footing \, shape \, is \, rectangular:
                S_q = 1 + \frac{B}{L} \tan \phi

            if \, footing \, shape \, is \, square \, or \, circular:
                S_c = 1 + \tan \phi

        :return: A `float` representing the shape factor :math:`S_q`
        :rtype: float
        """
        return round(self.shape_factors.sq, DECIMAL_PLACES)

    @sq.setter
    def sq(self, val: Union[int, float]):
        self.shape_factors.sq = val

    @property
    def sgamma(self) -> float:
        r"""Shape factor :math:`S_\gamma`.

        .. math::

            if \, footing \, shape \, is \, continuous(strip):
                S_\gamma = 1

            if \, footing \, shape \, is \, rectangular:
                S_\gamma = 1 - 0.4 \frac{B}{L}

            if \, footing \, shape \, is \, square \, or \, circular:
                S_\gamma = 0.6

        :return: A `float` representing the shape factor :math:`S_\gamma`
        :rtype: float
        """
        return round(self.shape_factors.sgamma, DECIMAL_PLACES)

    @sgamma.setter
    def sgamma(self, val: Union[int, float]):
        self.shape_factors.sgamma = val

    @property
    def ic(self) -> float:
        r"""Inclination factor :math:`i_c`.

        .. math::

            i_c = (1 - \frac{\beta}{90})^2

        :return: A `float` representing the inclination factor :math:`i_c`
        :rtype: float
        """
        return round(self.incl_factors.ic, DECIMAL_PLACES)

    @ic.setter
    def ic(self, val: Union[int, float]):
        self.incl_factors.ic = val

    @property
    def iq(self) -> float:
        r"""Inclination factor :math:`i_q`.

        .. math::

            i_q = (1 - \frac{\beta}{90})^2

        :return: A `float` representing the inclination factor :math:`i_q`
        :rtype: float
        """
        return round(self.incl_factors.iq, DECIMAL_PLACES)

    @iq.setter
    def iq(self, val: Union[int, float]):
        self.incl_factors.iq = val

    @property
    def igamma(self) -> float:
        r"""Inclination factor :math:`i_\gamma`.

        .. math::

            i_\gamma = (1 - \frac{\beta}{\phi})^2

        :return: A `float` representing the inclination factor :math:`i_\gamma`
        :rtype: float
        """
        return round(self.incl_factors.igamma, DECIMAL_PLACES)

    @igamma.setter
    def igamma(self, val: Union[int, float]):
        self.incl_factors.igamma = val
