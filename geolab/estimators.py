"""Soil Engineering Parameter Estimators (:mod:`geolab.estimators`) .

This module provides functions for estimating soil engineering parameters.

Classes
-------

.. autosummary::
    :toctree:

    SoilUnitWeight
    CompressionIndex
    SoilFrictionAngle
    UndrainedShearStrength


Functions
---------

.. autosummary::
    :toctree:

    bowles_soil_elastic_modulus
    rankine_foundation_depth
"""

from dataclasses import dataclass

from geolab import GeotechEng
from geolab.exceptions import EngineerTypeError
from geolab.utils import arctan, round_, sin


@dataclass
class SoilUnitWeight:
    """Calculates the ``moist``, ``saturated`` and ``submerged`` unit weight of
    soil sample.

    :Example:
        >>> from geolab.estimators import SoilUnitWeight
        >>> suw = SoilUnitWeight(spt_n60=13)
        >>> suw.moist
        17.3
        >>> suw.saturated
        18.75
        >>> suw.submerged
        8.93

    :param spt_n60: spt N-value corrected for 60% hammer efficiency.
    :type spt_n60: float
    """

    spt_n60: float

    @property
    @round_
    def moist(self) -> float:
        r"""Return the ``moist`` unit weight for cohesionless soil.

        .. math::

            \gamma_{moist} = 16.0 + 0.1 \cdot N_{60} \rightarrow (kN/m^3)
        """
        return 16.0 + 0.1 * self.spt_n60

    @property
    @round_
    def saturated(self) -> float:
        r"""Return the ``saturated`` unit weight for cohesive soil.

        .. math::

            \gamma_{sat} = 16.8 + 0.15 \cdot N_{60} \rightarrow (kN/m^3)
        """
        return 16.8 + 0.15 * self.spt_n60

    @property
    @round_
    def submerged(self) -> float:
        r"""Return the ``submerged`` unit weight of cohesionless soil.

        .. math::

            \gamma_{submerged} = 8.8 + 0.01 \cdot N_{60} \rightarrow (kN/m^3)
        """
        return 8.8 + 0.01 * self.spt_n60


class CompressionIndex:
    r"""The compression index of soil estimated from ``liquid limit`` or ``void
    ratio``.

    The available correlations used are :py:meth:`~compression_index.skempton_1994`,
    :py:meth:`terzaghi_et_al_1967`, and :meth:`hough_1957`.

    :Example:

        >>> from geolab.estimators import CompressionIndex
        >>> c_c = CompressionIndex(liquid_limit=35)
        >>> c_c.skempton_1994()
        0.175
        >>> c_c.terzaghi_et_al_1967()
        0.225
        >>> c_c() # By default it uses SKEMPTON's correlation
        0.175
        >>> c_c = CompressionIndex(liquid_limit=35, eng=GeotechEng.TERZAGHI)
        >>> c_c() # This uses TERZAGHI's correlation
        0.225
        >>> c_c = CompressionIndex(void_ratio=0.78, eng=GeotechEng.HOUGH)
        >>> c_c()
        0.148
        >>> c_c.hough_1957()
        0.148

    :param liquid_limit: water content beyond which soils flows under their own weight (%)
    :type liquid_limit: float
    :param void_ratio: ratio of the volume of voids to the volume of solids (unitless)
    :type void_ratio: float
    :param eng: specifies the type of compression index formula to use. Available
                values are ``GeotechEng.SKEMPTON``, ``GeotechEng.TERZAGHI`` and
                ``GeotechEng.HOUGH``. Defaults to ``GeotechEng.SKEMPTON``.
    :type eng: GeotechEng

    :raises exceptions.EngineerTypeError: if eng specified is not valid
    """

    def __init__(
        self,
        *,
        liquid_limit: float = 0.0,
        void_ratio: float = 0.0,
        eng: GeotechEng = GeotechEng.SKEMPTON,
    ) -> None:
        self.liquid_limit = liquid_limit
        self.void_ratio = void_ratio
        self.eng = eng

        if self.eng not in {
            GeotechEng.SKEMPTON,
            GeotechEng.TERZAGHI,
            GeotechEng.HOUGH,
        }:
            msg = f"{self.eng} is not a valid type for {type(self)} engineer"
            raise EngineerTypeError(msg)

    def __call__(self) -> float:
        # Returns the compression index of the soil sample (unitless)

        comp_idx: float  # compression index

        if self.eng is GeotechEng.SKEMPTON:
            comp_idx = self.skempton_1994()

        elif self.eng is GeotechEng.TERZAGHI:
            comp_idx = self.terzaghi_et_al_1967()

        else:
            comp_idx = self.hough_1957()

        return comp_idx

    @round_
    def terzaghi_et_al_1967(self) -> float:
        r"""Return the compression index of the soil using ``Terzaghi's``
        correlation.

        .. math::

            C_c = 0.009 \left(LL - 10 \right) \rightarrow (unitless)

        - :math:`LL` |rarr| liquid limit of soil
        """
        return 0.009 * (self.liquid_limit - 10)

    @round_
    def skempton_1994(self) -> float:
        r"""Return the compression index of the soil using ``Skempton's``
        correlation.

        .. math::

            C_c = 0.007 \left(LL - 10 \right) \rightarrow (unitless)

        - :math:`LL` |rarr| liquid limit of soil
        """
        return 0.007 * (self.liquid_limit - 10)

    @round_
    def hough_1957(self) -> float:
        r"""Return the compression index of the soil using ``Hough's``
        correlation.

        .. math::

            C_c = 0.29 \left(e_o - 0.27 \right) \rightarrow (unitless)

        - :math:`e_o` |rarr| void ratio of soil
        """
        return 0.29 * (self.void_ratio - 0.27)


class SoilFrictionAngle:
    r"""Estimation of the internal angle of friction using spt_n60.

    For cohesionless soils the coefficient of internal friction (:math:`\phi`)
    was determined from the minimum value from :py:meth:`wolff_1989` and 
    :py:meth:`kullhawy_mayne_1990`.

    :Example:

        >>> from geolab.estimators import SoilFrictionAngle
        >>> sfa = SoilFrictionAngle(spt_n60=50)
        >>> sfa.wolff_1989()
        40.75
        >>> sfa() # By default it uses WOLFF's correlation
        40.75
        >>> sfa.spt_n60 = 40
        >>> sfa()
        38.236
        >>> sfa = SoilFrictionAngle(spt_n60=40, eop=103.8, atm_pressure=101.325,\
        ... eng=GeotechEng.KULLHAWY)
        >>> sfa()
        46.874
        >>> sfa.kullhawy_mayne_1990()
        46.874
        >>> sfa.spt_n60 = 50
        >>> sfa()
        49.035

    :param spt_n60: spt N-value corrected for 60% hammer efficiency
    :type spt_n60: float
    :param eop: effective overburden pressure :math:`kN/m^2`, defaults to 0
    :type eop: float, optional
    :param atm_pressure: atmospheric pressure :math:`kN/m^2`, defaults to 0
    :type atm_pressure: float, optional
    :param eng: specifies the type of soil friction angle formula to use. Available
                values are ``GeotechEng.WOLFF`` and ``GeotechEng.KULLHAWY``. Defaults to 
                ``GeotechEng.WOLFF``.
    :type eng: GeotechEng

    :raises exceptions.EngineerTypeError: if eng specified is not valid
    """

    def __init__(
        self,
        *,
        spt_n60: float,
        eop: float = 0,
        atm_pressure: float = 0,
        eng: GeotechEng = GeotechEng.WOLFF,
    ):
        self.spt_n60 = spt_n60
        self.eop = eop
        self.atm_pressure = atm_pressure
        self.eng = eng

        if self.eng not in {GeotechEng.WOLFF, GeotechEng.KULLHAWY}:
            msg = f"{self.eng} is not a valid type for {type(self)} Engineer"
            raise EngineerTypeError(msg)

    def __call__(self) -> float:
        # Returns the internal angle of friction (degrees)

        _friction_angle: float

        if self.eng is GeotechEng.WOLFF:
            _friction_angle = self.wolff_1989()

        else:
            _friction_angle = self.kullhawy_mayne_1990()

        return _friction_angle

    @round_
    def wolff_1989(self) -> float:
        r"""Return the internal angle of friction using ``Wolff's`` correlation
        for granular soils (degrees).

        .. math::

            \phi = 27.1 + 0.3 \cdot N_{60} - 0.00054 \cdot (N_{60})^2 \rightarrow (degrees)
        """
        return 27.1 + (0.3 * self.spt_n60) - (0.00054 * (self.spt_n60**2))

    @round_
    def kullhawy_mayne_1990(self) -> float:
        r"""Return the internal angle of friction using ``Kullhawy & Mayne``
        correlation for cohesionless soils (degrees).

        .. math::

            \phi = \tan^{-1}\left[\dfrac{N_{60}}
                    {12.2 + 20.3 \cdot \left(\dfrac{\sigma_o}{P_a}\right)}
                    \right]^{0.34} \rightarrow (degrees)

        - :math:`\sigma_o \rightarrow` effective overburden pressure (:math:`kN/m^3`)
        - :math:`P_a \rightarrow` atmospheric pressure in the same unit as :math:`\sigma_o`
        """
        expr = self.spt_n60 / (12.2 + 20.3 * (self.eop / self.atm_pressure))
        return arctan(expr**0.34)


class UndrainedShearStrength:
    r"""Undrained shear strength of soil.

    The available correlations used are :py:meth:`stroud_1974` and 
    :py:meth:`skempton_1957`.

    :Example:

        >>> from geolab.estimators import UndrainedShearStrength
        >>> uss = UndrainedShearStrength(spt_n60=40)
        >>> uss()
        140.0
        >>> uss.stroud_1974()
        140.0
        >>> uss = UndrainedShearStrength(spt_n60=40, eop=108.3,\
        ... plasticity_index=12, eng=GeotechEng.SKEMPTON)
        >>> uss()
        16.722
        >>> uss.skempton_1957()
        16.722

    :param spt_n60: SPT N-value corrected for 60% hammer efficiency, defaults to 0
    :type spt_n60: Optional[float], optional
    :param eop: effective overburden pressure :math:`kN/m^2`, defaults to 0
    :type eop: Optional[float], optional
    :param plasticity_index: range of water content over which soil remains in plastic
                             condition, defaults to 0
    :type plasticity_index: Optional[float], optional
    :param k: stroud parameter, defaults to 3.5
    :type k: float, optional
    :param eng: specifies the type of undrained shear strength formula to use. Available
                values are ``GeotechEng.STROUD`` and ``GeotechEng.SKEMPTON``, defaults to
                ``GeotechEng.STROUD``
    :type eng: GeotechEng, optional

    :raises exceptions.EngineerTypeError: if eng specified is not valid
    """

    def __init__(
        self,
        *,
        spt_n60: float = 0,
        eop: float = 0,
        plasticity_index: float = 0,
        k: float = 3.5,
        eng: GeotechEng = GeotechEng.STROUD,
    ) -> None:
        self.spt_n60 = spt_n60
        self.eop = eop
        self.plasticity_index = plasticity_index
        self.k = k
        self.eng = eng

        if self.eng not in {GeotechEng.STROUD, GeotechEng.SKEMPTON}:
            msg = f"{self.eng} is not a valid type for {type(self)} engineer"
            raise EngineerTypeError(msg)

    def __call__(self) -> float:
        und_shr: float  # undrained shear strength

        if self.eng is GeotechEng.STROUD:
            und_shr = self.stroud_1974()

        else:
            und_shr = self.skempton_1957()

        return und_shr

    @round_
    def stroud_1974(self):
        r"""Return the undrained shear strength using ``Stroud's`` correlation.

        .. math::

            C_u = K \times N_{60}

            3.5 \le K \le 6.5

        :raises ValueError: If ``k`` is not in the specified range.
        """
        if 3.5 <= self.k <= 6.5:
            return self.k * self.spt_n60

        msg = f"k should be 3.5 <= k <= 6.5 not {self.k}"
        raise ValueError(msg)

    @round_
    def skempton_1957(self):
        r"""Return the undrained shear strength using ``Skempton's`` correlation.

        .. math::

            \dfrac{C_u}{\sigma_o} = 0.11 + 0.0037 \cdot PI

        - :math:`\sigma_o \rightarrow` effective overburden pressure (:math:`kN/m^2`)

        The ratio :math:`\frac{C_u}{\sigma_o}` is a constant for a given clay.
        ``Skempton`` suggested that a similar constant ratio exists between the
        undrained shear strength of normally consolidated natural deposits and
        the effective overburden pressure. It has been established that the ratio
        :math:`\frac{C_u}{\sigma_o}` is constant provided the plasticity index (PI)
        of the soil remains constant.

        The value of the ratio :math:`\frac{C_u}{\sigma_o}` determined in a
        consolidated-undrained test on undisturbed samples is generally greater than
        actual value because of anisotropic consolidation in the field. The actual
        value is best determined by `in-situ shear vane test`.
        """
        return self.eop * (0.11 + 0.0037 * self.plasticity_index)


@round_(precision=2)
def bowles_soil_elastic_modulus(spt_n60: float) -> float:
    r"""Elastic modulus of soil estimated from ``Joseph Bowles`` correlation.

    .. math::

        E_s = 320\left(N_{60} + 15 \right) \rightarrow (kN/m^2)

    :Example:

        >>> from geolab.estimators import bowles_soil_elastic_modulus
        >>> bowles_soil_elastic_modulus(20)
        11200
        >>> bowles_soil_elastic_modulus(30)
        14400
        >>> bowles_soil_elastic_modulus(10)
        8000

    :param spt_n60: spt N-value corrected for 60% hammer efficiency
    :type spt_n60: float

    :return: Elastic modulus of the soil :math:`kN/m^2`
    :rtype: float
    """
    return 320 * (spt_n60 + 15)


@round_(precision=1)
def rankine_foundation_depth(
    allowable_bearing_capacity: float,
    soil_unit_weight: float,
    soil_friction_angle: float,
) -> float:
    r"""Depth of foundation estimated using ``Rankine's`` formula.

    .. math::

        D_f=\dfrac{Q_{all}}{\gamma}\left(\dfrac{1 - \sin \phi}{1 + \sin \phi}\right)^2
        \rightarrow (m)

    :Example:

        >>> from geolab.estimators import rankine_foundation_depth
        >>> rankine_foundation_depth(350, 18, 35)
        1.4

    :param allowable_bearing_capacity: allowable bearing capacity :math:`kN/m^2`
    :type allowable_bearing_capaciy: float
    :param soil_unit_weight: unit weight of soil :math:`kN/m^3`
    :type soil_unit_weight: float
    :param soil_friction_angle: internal angle of friction (degrees)
    :type soil_friction_angle: float

    :return: depth of foundation
    :rtype: float
    """
    x_1 = allowable_bearing_capacity / soil_unit_weight
    x_2 = (1 - sin(soil_friction_angle)) / (1 + sin(soil_friction_angle))

    return x_1 * (x_2**2)
