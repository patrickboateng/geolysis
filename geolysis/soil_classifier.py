import enum
from typing import Iterable, Optional, NamedTuple

from geolysis.utils import isclose, round_

__all__ = ["ClfType", "AtterbergLimits", "PSD", "AASHTO", "USCS",
           "SizeDistribution", "create_soil_classifier"]


class SizeDistError(ZeroDivisionError):
    pass


# Soil classification type
class ClfType(enum.StrEnum):
    AASHTO = enum.auto()
    USCS = enum.auto()


class ClfSymbol(enum.Enum):
    def __eq__(self, value: object) -> bool:
        if isinstance(value, str):
            return self.symbol == value
        return super().__eq__(value)

    @property
    def symbol(self) -> str:
        return self.value[0]

    @property
    def description(self) -> str:
        return self.value[1]


@enum.global_enum
class USCSSymbol(ClfSymbol):
    G = GRAVEL = ("G", "Gravel")
    S = SAND = ("S", "Sand")
    M = SILT = ("M", "Silt")
    C = CLAY = ("C", "Clay")
    O = ORGANIC = ("O", "Organic")
    W = WELL_GRADED = ("W", "Well graded")
    P = POORLY_GRADED = ("P", "Poorly graded")
    L = LOW_PLASTICITY = ("L", "Low plasticity")
    H = HIGH_PLASTICITY = ("H", "High plasticity")
    GW = ("GW", "Well graded gravels")
    GP = ("GP", "Poorly graded gravels")
    GM = ("GM", "Silty gravels")
    GC = ("GC", "Clayey gravels")
    GM_GC = ("GM-GC", "Gravelly clayey silt")
    GW_GM = ("GW-GM", "Well graded gravel with silt")
    GP_GM = ("GP-GM", "Poorly graded gravel with silt")
    GW_GC = ("GW-GC", "Well graded gravel with clay")
    GP_GC = ("GP-GC", "Poorly graded gravel with clay")
    SW = ("SW", "Well graded sands")
    SP = ("SP", "Poorly graded sands")
    SM = ("SM", "Silty sands")
    SC = ("SC", "Clayey sands")
    SM_SC = ("SM-SC", "Sandy clayey silt")
    SW_SM = ("SW-SM", "Well graded sand with silt")
    SP_SM = ("SP-SM", "Poorly graded sand with silt")
    SW_SC = ("SW-SC", "Well graded sand with clay")
    SP_SC = ("SP-SC", "Poorly graded sand with clay")
    ML = ("ML", "Inorganic silts with low plasticity")
    CL = ("CL", "Inorganic clays with low plasticity")
    ML_CL = ("ML-CL", "Clayey silt with low plasticity")
    OL = ("OL", "Organic clays with low plasticity")
    MH = ("MH", "Inorganic silts with high plasticity")
    CH = ("CH", "Inorganic clays with high plasticity")
    OH = ("OH", "Organic silts with high plasticity")
    Pt = ("Pt", "Highly organic soils")


@enum.global_enum
class AASHTOSymbol(ClfSymbol):
    A_1_a = ("A-1-a", "Stone fragments, gravel, and sand")
    A_1_b = ("A-1-b", "Stone fragments, gravel, and sand")
    A_3 = ("A-3", "Fine sand")
    A_2_4 = ("A-2-4", "Silty or clayey gravel and sand")
    A_2_5 = ("A-2-5", "Silty or clayey gravel and sand")
    A_2_6 = ("A-2-6", "Silty or clayey gravel and sand")
    A_2_7 = ("A-2-7", "Silty or clayey gravel and sand")
    A_4 = ("A-4", "Silty soils")
    A_5 = ("A-5", "Silty soils")
    A_6 = ("A-6", "Clayey soils")
    A_7_5 = ("A-7-5", "Clayey soils")
    A_7_6 = ("A-7-6", "Clayey soils")


class AtterbergLimits:
    """Water contents at which soil changes from one state to the other.

    In 1911, a Swedish agriculture engineer ``Atterberg`` mentioned that a
    fined-grained soil can exist in four states, namely, liquid, plastic,
    semi-solid or solid state.

    The main use of Atterberg Limits is in the classification of soils.

    :param int | float liquid_limit: Water content beyond which soils flows
        under their own weight. It can also be defined as the minimum moisture
        content at which a soil flows upon application of a very small shear
        force.
    :param int | float plastic_limit: Water content at which plastic deformation
        can be initiated. It is also the minimum water content at which soil can
        be rolled into a thread 3mm thick. (molded without breaking)

    Examples
    --------
    >>> from geolysis.soil_classifier import AtterbergLimits as AL

    >>> atterberg_limits = AL(liquid_limit=55.44, plastic_limit=33.31)
    >>> atterberg_limits.plasticity_index
    22.13
    >>> atterberg_limits.A_line
    25.87

    >>> atterberg_limits.above_A_LINE()
    False
    >>> atterberg_limits.limit_plot_in_hatched_zone()
    False

    Negative values of liquidity index indicates that the soil is in a hard
    state.

    >>> atterberg_limits.liquidity_index(nmc=15.26)
    -81.56

    A consistency index greater than 100% shows the soil is relatively strong.

    >>> atterberg_limits.consistency_index(nmc=15.26)
    181.56
    """

    def __init__(self, liquid_limit: float, plastic_limit: float):
        self.liquid_limit = liquid_limit
        self.plastic_limit = plastic_limit

    @property
    @round_
    def plasticity_index(self) -> float:
        """Plasticity index (PI) is the range of water content over which the
        soil remains in the plastic state.

        It is also the numerical difference between the liquid limit and plastic
        limit of the soil.

        .. math:: PI = LL - PL
        """
        return self.liquid_limit - self.plastic_limit

    @property
    @round_
    def A_line(self) -> float:
        """The ``A-line`` is used to determine if a soil is clayey or silty.

        .. math:: A = 0.73(LL - 20)
        """
        return 0.73 * (self.liquid_limit - 20.0)

    @property
    def fine_material_type(self) -> USCSSymbol:
        """
        Determines whether the soil is either clay or :silt.
        """
        return USCSSymbol.CLAY if self.above_A_LINE() else USCSSymbol.SILT

    def above_A_LINE(self) -> bool:
        """Checks if the soil sample is above A-Line."""
        return self.plasticity_index > self.A_line

    def limit_plot_in_hatched_zone(self) -> bool:
        """Checks if soil sample plot in the hatched zone on the atterberg
        chart.
        """
        return 4 <= self.plasticity_index <= 7 and 10 < self.liquid_limit < 30

    @round_
    def liquidity_index(self, nmc: float) -> float:
        r"""Return the liquidity index of the soil.

        Liquidity index of a soil indicates the nearness of its ``natural water
        content`` to its ``liquid limit``. When the soil is at the plastic limit
        its liquidity index is zero. Negative values of the liquidity index
        indicate that the soil is in a hard (desiccated) state. It is also known
        as Water-Plasticity ratio.

        :param int | float nmc: Moisture contents of the soil in natural
            condition.

        Notes
        -----
        The ``liquidity index`` is given by the formula:

        .. math:: I_l = \dfrac{w - PL}{PI} \cdot 100
        """
        return ((nmc - self.plastic_limit) / self.plasticity_index) * 100.0

    @round_
    def consistency_index(self, nmc: float) -> float:
        r"""Return the consistency index of the soil.

        Consistency index indicates the consistency (firmness) of soil. It shows
        the nearness of the ``natural water content`` of the soil to its
        ``plastic limit``. When the soil is at the liquid limit, the consistency
        index is zero. The soil at consistency index of zero will be extremely
        soft and has negligible shear strength. A soil at a water content equal
        to the plastic limit has consistency index of 100% indicating that the
        soil is relatively firm. A consistency index of greater than 100% shows
        the soil is relatively strong (semi-solid state). A negative value
        indicate the soil is in the liquid state. It is also known as Relative
        Consistency.

        :param int | float nmc: Moisture contents of the soil in natural
            condition.

        Notes
        -----
        The ``consistency index`` is given by the formula:

        .. math:: I_c = \dfrac{LL - w}{PI} \cdot 100
        """
        return ((self.liquid_limit - nmc) / self.plasticity_index) * 100.0


# @dataclass
class SizeDistribution(NamedTuple):
    """Features obtained from the Particle Size Distribution graph.

    :param int | float d_10: Diameter at which 10% of the soil by weight is
        finer.
    :param int | float d_30: Diameter at which 30% of the soil by weight is
        finer.
    :param int | float d_60: Diameter at which 60% of the soil by weight is
        finer.
    """

    d_10: float
    d_30: float
    d_60: float

    @property
    def coeff_of_curvature(self) -> float:
        return (self.d_30 ** 2.0) / (self.d_60 * self.d_10)

    @property
    def coeff_of_uniformity(self) -> float:
        return self.d_60 / self.d_10

    def grade(self, coarse_soil: USCSSymbol) -> USCSSymbol:
        """Grade of soil sample. Soil grade can either be well graded or poorly
        graded.

        :param str coarse_soil: Coarse fraction of the soil sample. Valid
            arguments are "G" for gravel and "S" for SAND.
        """

        if coarse_soil is USCSSymbol.GRAVEL:
            if 1 < self.coeff_of_curvature < 3 and self.coeff_of_uniformity >= 4:
                grade = USCSSymbol.WELL_GRADED
            else:
                grade = USCSSymbol.POORLY_GRADED
        elif coarse_soil is USCSSymbol.SAND:
            if 1 < self.coeff_of_curvature < 3 and self.coeff_of_uniformity >= 6:
                grade = USCSSymbol.WELL_GRADED
            else:
                grade = USCSSymbol.POORLY_GRADED
        else:
            raise NotImplementedError

        return grade


class PSD:
    r"""Quantitative proportions by mass of various sizes of particles present
    in a soil.

    Particle Size Distribution is a method of separation of soils into
    different fractions using a stack of sieves to measure the size of the
    particles in a sample and graphing the results to illustrate the
    distribution of the particle sizes.

    :param int | float fines: Percentage of fines in soil sample i.e. the
        percentage of soil sample passing through No. 200 sieve (0.075mm)
    :param int | float sand: Percentage of sand in soil sample.
    :param int | float gravel: Percentage of gravel in soil sample, defaults
        to None.

    Examples
    --------
    >>> from geolysis.soil_classifier import PSD, SizeDistribution

    >>> psd = PSD(fines=30.25, sand=53.55)

    The following code raises error because ``size_dist`` is not provided.

    >>> psd.coeff_of_curvature
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero

    >>> psd.coeff_of_uniformity
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero

    >>> size_dist = SizeDistribution(d_10=0.07, d_30=0.30, d_60=0.8)
    >>> psd = PSD(fines=10.29, sand=81.89, size_dist=size_dist)
    >>> psd.coeff_of_curvature
    1.61
    >>> psd.coeff_of_uniformity
    11.43
    """

    def __init__(self, fines: float, sand: float,
                 size_dist: Optional[SizeDistribution] = None):
        self.fines = fines
        self.sand = sand
        self.gravel = 100.0 - (fines + sand)
        self.size_dist = size_dist if size_dist else SizeDistribution(0, 0, 0)

    @property
    def coarse_material_type(self) -> USCSSymbol:
        """Determines whether the soil is either gravel or sand."""
        if self.gravel > self.sand:
            return USCSSymbol.GRAVEL
        else:
            return USCSSymbol.SAND
        # return (USCSSymbol.GRAVEL if self.gravel > self.sand
        #         else USCSSymbol.SAND)

    @property
    @round_(2)
    def coeff_of_curvature(self) -> float:
        r"""Coefficient of curvature of soil sample.

        Coefficient of curvature :math:`(C_c)` is given by the formula:

        .. math:: C_c = \dfrac{D^2_{30}}{D_{60} \times D_{10}}

        For the soil to be well graded, the value of :math:`C_c` must be
        between 1 and 3.
        """
        return self.size_dist.coeff_of_curvature

    @property
    @round_(2)
    def coeff_of_uniformity(self) -> float:
        r"""Coefficient of uniformity of soil sample.

        Coefficient of uniformity :math:`(C_u)` is given by the formula:

        .. math:: C_u = \dfrac{D_{60}}{D_{10}}

        :math:`C_u` value greater than 4 to 6 classifies the soil as well graded
        for gravels and sands respectively. When :math:`C_u` is less than 4, it
        is classified as poorly graded or uniformly graded soil.

        Higher values of :math:`C_u` indicates that the soil mass consists of
        soil particles with different size ranges.
        """
        return self.size_dist.coeff_of_uniformity

    def has_particle_sizes(self) -> bool:
        """Checks if soil sample has particle sizes."""
        return any(self.size_dist)

    def grade(self) -> USCSSymbol:
        r"""Return the grade of the soil sample, either well graded or poorly
        graded.

        Conditions for a well-graded soil:

        - :math:`1 \lt C_c \lt 3` and :math:`C_u \ge 4` (for gravels)
        - :math:`1 \lt C_c \lt 3` and :math:`C_u \ge 6` (for sands)
        """
        return self.size_dist.grade(coarse_soil=self.coarse_material_type)


class AASHTO:
    r"""American Association of State Highway and Transportation Officials
    (AASHTO) classification system.

    The AASHTO classification system is useful for classifying soils for
    highways. It categorizes soils for highways based on particle size analysis
    and plasticity characteristics. It classifies both coarse-grained and
    fine-grained soils into eight main groups (A1-A7) with subgroups, along with
    a separate category (A8) for organic soils.

    - ``A1 ~ A3`` (Granular Materials) :math:`\le` 35% pass No. 200 sieve
    - ``A4 ~ A7`` (Silt-clay Materials) :math:`\ge` 36% pass No. 200 sieve
    - ``A8`` (Organic Materials)

    The Group Index ``(GI)`` is used to further evaluate soils within a group.

    :param int | float liquid_limit: Water content beyond which soils flows
        under their own weight.
    :param int | float plasticity_index: Range of water content over which soil
        remains in plastic condition.
    :param int | float fines: Percentage of fines in soil sample i.e. the
        percentage of soil sample passing through No. 200 sieve (0.075mm).
    :param bool add_group_idx: Used to indicate whether the group index should
        be added to the classification or not. Defaults to True.

    Notes
    -----
    The ``GI`` must be mentioned even when it is zero, to indicate that the soil
    has been classified as per AASHTO system.

    .. math::

        GI = (F_{200} - 35)[0.2 + 0.005(LL - 40)] + 0.01(F_{200} - 15)(PI - 10)

    Examples
    --------
    >>> from geolysis.soil_classifier import AASHTO

    >>> aashto_clf = AASHTO(liquid_limit=30.2, plastic_limit=23.9, fines=11.18)
    >>> aashto_clf.group_index()
    0.0
    >>> aashto_clf.classify()
    'A-2-4(0)'
    >>> aashto_clf.description()
    'Silty or clayey gravel and sand'

    If you would like to exclude the group index from the classification, you
    can do the following:

    >>> aashto_clf.add_group_idx = False
    >>> aashto_clf.classify()
    'A-2-4'
    """

    def __init__(self, liquid_limit: float, plastic_limit: float, fines: float,
                 add_group_idx=True):
        self.liquid_limit = liquid_limit
        self.plastic_limit = plastic_limit
        self.plasticity_index = liquid_limit - plastic_limit
        self.fines = fines
        self.add_group_idx = add_group_idx

    def group_index(self) -> int | float:
        """Return the Group Index (GI) of the soil sample."""

        liquid_lmt = self.liquid_limit
        plasticity_idx = self.plasticity_index
        fines = self.fines

        a = 1.0 if (x_0 := fines - 35.0) < 0.0 else min(x_0, 40.0)
        b = 1.0 if (x_0 := liquid_lmt - 40.0) < 0.0 else min(x_0, 20.0)
        c = 1.0 if (x_0 := fines - 15.0) < 0.0 else min(x_0, 40.0)
        d = 1.0 if (x_0 := plasticity_idx - 10.0) < 0.0 else min(x_0, 20.0)

        return round(a * (0.2 + 0.005 * b) + 0.01 * c * d, ndigits=0)

    def description(self) -> str:
        """Return the AASHTO description of the soil."""
        tmp_state = self.add_group_idx
        self.add_group_idx = False
        soil_clf = self._classify()
        self.add_group_idx = tmp_state
        return soil_clf.description

    def classify(self) -> str:
        """Return the AASHTO classification of the soil."""
        soil_clf = self._classify().symbol

        if self.add_group_idx:
            soil_clf = f"{soil_clf}({self.group_index():.0f})"

        return soil_clf

    def _classify(self) -> AASHTOSymbol:
        # Silts A4-A7
        if self.fines > 35:
            soil_clf = self._fine_soil_classifier()
        # Coarse A1-A3
        else:
            soil_clf = self._coarse_soil_classifier()

        return soil_clf

    def _fine_soil_classifier(self) -> AASHTOSymbol:
        # A-4 -> A-5, Silty Soils
        # A-6 -> A-7, Clayey Soils
        liquid_lmt = self.liquid_limit
        plasticity_idx = self.plasticity_index

        if liquid_lmt <= 40:
            if plasticity_idx <= 10.0:
                soil_clf = AASHTOSymbol.A_4
            else:
                soil_clf = AASHTOSymbol.A_6
        else:
            if plasticity_idx <= 10.0:
                soil_clf = AASHTOSymbol.A_5
            else:
                if plasticity_idx <= (liquid_lmt - 30.0):
                    soil_clf = AASHTOSymbol.A_7_5
                else:
                    soil_clf = AASHTOSymbol.A_7_6

        return soil_clf

    def _coarse_soil_classifier(self) -> AASHTOSymbol:
        # A-3, Fine sand
        liquid_lmt = self.liquid_limit
        plasticity_idx = self.plasticity_index

        if self.fines <= 10.0 and isclose(plasticity_idx, 0.0, rel_tol=0.01):
            soil_clf = AASHTOSymbol.A_3
        # A-1-a -> A-1-b, Stone fragments, gravel, and sand
        elif self.fines <= 15 and plasticity_idx <= 6:
            soil_clf = AASHTOSymbol.A_1_a
        elif self.fines <= 25 and plasticity_idx <= 6:
            soil_clf = AASHTOSymbol.A_1_b
        # A-2-4 -> A-2-7, Silty or clayey gravel and sand
        elif liquid_lmt <= 40:
            if plasticity_idx <= 10:
                soil_clf = AASHTOSymbol.A_2_4
            else:
                soil_clf = AASHTOSymbol.A_2_6

        else:
            if plasticity_idx <= 10:
                soil_clf = AASHTOSymbol.A_2_5
            else:
                soil_clf = AASHTOSymbol.A_2_7

        return soil_clf


class USCS:
    """Unified Soil Classification System (USCS).

    The Unified Soil Classification System, initially developed by Casagrande in
    1948 and later modified in 1952, is widely utilized in engineering projects
    involving soils. It is the most popular system for soil classification and
    is similar to Casagrande's Classification System. The system relies on
    particle size analysis and atterberg limits for classification.

    In this system, soils are first classified into two categories:

    - Coarse grained soils: If more than 50% of the soils is retained on No. 200
      (0.075 mm) sieve, it is designated as coarse-grained soil.

    - Fine grained soils: If more than 50% of the soil passes through No. 200
      sieve, it is designated as fine-grained soil.

    Highly Organic soils are identified by visual inspection. These soils are
    termed as Peat. (:math:`P_t`)

    :param int | float liquid_limit: Water content beyond which soils flows
        under their own weight. It can also be defined as the minimum moisture
        content at which a soil flows upon application of a very small shear
        force.
    :param int | float plastic_limit: Water content at which plastic deformation
        can be initiated. It is also the minimum water content at which soil can
        be rolled into a thread 3mm thick (molded without breaking)
    :param int | float fines: Percentage of fines in soil sample i.e. The
        percentage of soil sample passing through No. 200 sieve (0.075mm)
    :param int | float sand: Percentage of sand in soil sample (%)
    :param bool organic: Indicates whether soil is organic or not, defaults to
        False.

    Examples
    --------
    >>> from geolysis.soil_classifier import (
    ...     AtterbergLimits,
    ...     PSD,
    ...     USCS,
    ...     SizeDistribution,
    ... )

    >>> al = AtterbergLimits(liquid_limit=34.1, plastic_limit=21.1)
    >>> psd = PSD(fines=47.88, sand=37.84)
    >>> uscs_clf = USCS(atterberg_limits=al, psd=psd)
    >>> uscs_clf.classify()
    'SC'
    >>> uscs_clf.description()
    'Clayey sands'

    >>> al = AtterbergLimits(liquid_limit=30.8, plastic_limit=20.7)
    >>> size_dist = SizeDistribution(d_10=0.07, d_30=0.3, d_60=0.8)
    >>> psd = PSD(fines=10.29, sand=81.89, size_dist=size_dist)
    >>> uscs_clf = USCS(atterberg_limits=al, psd=psd)
    >>> uscs_clf.classify()
    'SW-SC'
    >>> uscs_clf.description()
    'Well graded sand with clay'
    """

    def __init__(self, atterberg_limits: AtterbergLimits, psd: PSD,
                 organic=False):
        self.atterberg_limits = atterberg_limits
        self.psd = psd
        self.organic = organic

    def description(self) -> str | Iterable[str]:
        """Return the USCS description of the soil."""
        soil_clf = self._classify()

        if isinstance(soil_clf, USCSSymbol):
            return soil_clf.description
        elif isinstance(soil_clf, str):
            return USCSSymbol[soil_clf].description
        else:
            return tuple(map(lambda v: USCSSymbol[v].description, soil_clf))

    def classify(self) -> str | Iterable[str]:
        """Return the USCS classification of the soil."""
        soil_clf = self._classify()
        if isinstance(soil_clf, USCSSymbol):
            return soil_clf.symbol
        elif isinstance(soil_clf, str):
            return soil_clf.replace("_", "-")
        else:
            return tuple(map(lambda v: v.replace("_", "-"), soil_clf))

    def _classify(self) -> USCSSymbol | str | Iterable[str]:
        # Fine-grained, Run Atterberg
        if self.psd.fines > 50.0:
            return self._fine_soil_classifier()

        # Coarse grained, Run Sieve Analysis
        # Gravel or Sand
        return self._coarse_soil_classifier()

    def _fine_soil_classifier(self) -> USCSSymbol:
        liquid_lmt = self.atterberg_limits.liquid_limit
        plasticity_idx = self.atterberg_limits.plasticity_index

        if liquid_lmt < 50.0:
            # Low LL
            # Above A-line and PI > 7
            if self.atterberg_limits.above_A_LINE() and plasticity_idx > 7.0:
                soil_clf = USCSSymbol.CL

            # Limit plot in hatched area on plasticity chart
            elif self.atterberg_limits.limit_plot_in_hatched_zone():
                soil_clf = USCSSymbol.ML_CL

            # Below A-line or PI < 4
            else:
                soil_clf = USCSSymbol.OL if self.organic else USCSSymbol.ML

        # High LL
        else:
            # Above A-Line
            if self.atterberg_limits.above_A_LINE():
                soil_clf = USCSSymbol.CH

            # Below A-Line
            else:
                soil_clf = USCSSymbol.OH if self.organic else USCSSymbol.MH

        return soil_clf

    def _coarse_soil_classifier(self) -> USCSSymbol | str | Iterable[str]:
        coarse_material_type = self.psd.coarse_material_type

        # More than 12% pass No. 200 sieve
        if self.psd.fines > 12.0:
            # Above A-line
            if self.atterberg_limits.above_A_LINE():
                soil_clf = f"{coarse_material_type}{USCSSymbol.CLAY}"

            # Limit plot in hatched zone on plasticity chart
            elif self.atterberg_limits.limit_plot_in_hatched_zone():
                if coarse_material_type == USCSSymbol.GRAVEL:
                    soil_clf = USCSSymbol.GM_GC
                else:
                    soil_clf = USCSSymbol.SM_SC

            # Below A-line
            else:
                if coarse_material_type == USCSSymbol.GRAVEL:
                    soil_clf = USCSSymbol.GM
                else:
                    soil_clf = USCSSymbol.SM

        elif 5.0 <= self.psd.fines <= 12.0:
            # Requires dual symbol based on graduation and plasticity chart
            if self.psd.has_particle_sizes():
                soil_clf = self._dual_soil_classifier()
            else:
                fine_material_type = self.atterberg_limits.fine_material_type

                soil_clf = (f"{coarse_material_type}{USCSSymbol.WELL_GRADED}_"
                            f"{coarse_material_type}{fine_material_type}",
                            f"{coarse_material_type}{USCSSymbol.POORLY_GRADED}_"
                            f"{coarse_material_type}{fine_material_type}")

        # Less than 5% pass No. 200 sieve
        # Obtain Cc and Cu from grain size graph
        else:
            if self.psd.has_particle_sizes():
                soil_clf = f"{coarse_material_type}{self.psd.grade()}"

            else:
                soil_clf = (f"{coarse_material_type}{USCSSymbol.WELL_GRADED}",
                            f"{coarse_material_type}{USCSSymbol.POORLY_GRADED}")

        return soil_clf

    def _dual_soil_classifier(self) -> str:
        fine_material_type = self.atterberg_limits.fine_material_type
        coarse_material_type = self.psd.coarse_material_type

        return (f"{coarse_material_type}{self.psd.grade()}_"
                f"{coarse_material_type}{fine_material_type}")


def create_soil_classifier(liquid_limit: float, plastic_limit: float,
                           fines: float, sand: Optional[float] = None,
                           d_10: float = 0, d_30: float = 0, d_60: float = 0,
                           add_group_idx: bool = True, organic: bool = False,
                           clf_type: ClfType | str | None = None) -> AASHTO | USCS:
    if clf_type is None:
        raise ValueError("clf_type must be specified")

    if clf_type == ClfType.AASHTO:
        clf = AASHTO(liquid_limit=liquid_limit, plastic_limit=plastic_limit,
                     fines=fines, add_group_idx=add_group_idx)

    elif clf_type == ClfType.USCS:
        if sand is None:
            raise ValueError("sand must be specified")

        al = AtterbergLimits(liquid_limit=liquid_limit,
                             plastic_limit=plastic_limit)
        size_dist = SizeDistribution(d_10=d_10, d_30=d_30, d_60=d_60)
        psd = PSD(fines=fines, sand=sand, size_dist=size_dist)
        clf = USCS(atterberg_limits=al, psd=psd, organic=organic)

    else:
        raise ValueError(f"clf_type {clf_type} not supported")

    return clf
