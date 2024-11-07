import enum
from typing import Final, Optional

import attrs

from geolysis.core.utils import isclose, round_

__all__ = ["AtterbergLimits", "PSD", "AASHTO", "USCS"]


class SizeDistError(ZeroDivisionError):
    pass


@enum.global_enum
class USCSSoilSymbol(enum.StrEnum):
    GRAVEL = "G"
    SAND = "S"
    SILT = "M"
    CLAY = "C"
    ORGANIC = "O"
    WELL_GRADED = "W"
    POORLY_GRADED = "P"
    LOW_PLASTICITY = "L"
    HIGH_PLASTICITY = "H"


@enum.global_enum
class AASHTOSoilSymbol(enum.StrEnum):
    A_1_a = "A-1-a"
    A_1_b = "A-1-b"
    A_3 = "A-3"
    A_2_4 = "A-2-4"
    A_2_5 = "A-2-5"
    A_2_6 = "A-2-6"
    A_2_7 = "A-2-7"
    A_4 = "A-4"
    A_5 = "A-5"
    A_6 = "A-6"
    A_7_5 = "A-7-5"
    A_7_6 = "A-7-6"


# Soil classification type
class SCType(enum.StrEnum):
    AASHTO = enum.auto()
    USCS = enum.auto()


@attrs.define
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
    >>> from geolysis.core.soil_classifier import AtterbergLimits as AL

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

    liquid_limit: int | float
    plastic_limit: int | float

    @property
    @round_
    def plasticity_index(self) -> int | float:
        """Plasticity index (PI) is the range of water content over which the
        soil remains in the plastic state.

        It is also the numerical difference between the liquid limit and plastic
        limit of the soil.

        .. math:: PI = LL - PL
        """
        return self.liquid_limit - self.plastic_limit

    @property
    @round_
    def A_line(self) -> int | float:
        """The ``A-line`` is used to determine if a soil is clayey or silty.

        .. math:: A = 0.73(LL - 20)
        """
        return 0.73 * (self.liquid_limit - 20.0)

    @property
    def type_of_fines(self) -> str:
        """
        Determines whether the soil is either clay or :silt.
        """
        return CLAY if self.above_A_LINE() else SILT

    def above_A_LINE(self) -> bool:
        """Checks if the soil sample is above A-Line."""
        return self.plasticity_index > self.A_line

    def limit_plot_in_hatched_zone(self) -> bool:
        """Checks if soil sample plot in the hatched zone on the atterberg
        chart.
        """
        return 4 <= self.plasticity_index <= 7 and 10 < self.liquid_limit < 30

    @round_
    def liquidity_index(self, nmc: int | float) -> int | float:
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
        return ((nmc - self.plastic_limit) / self.plasticity_index) * 100

    @round_
    def consistency_index(self, nmc: int | float) -> int | float:
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


@attrs.define(slots=True)
class SizeDistribution:
    """Features obtained from the Particle Size Distribution graph.

    :param int | float d_10: Diameter at which 10% of the soil by weight is
        finer.
    :param int | float d_30: Diameter at which 30% of the soil by weight is
        finer.
    :param int | float d_60: Diameter at which 60% of the soil by weight is
        finer.
    """

    d_10: int | float
    d_30: int | float
    d_60: int | float

    @property
    def coeff_of_curvature(self) -> int | float:
        return (self.d_30**2) / (self.d_60 * self.d_10)

    @property
    def coeff_of_uniformity(self) -> int | float:
        return self.d_60 / self.d_10

    def grade(self, coarse_soil: str) -> str:
        """Grade of soil sample. Soil grade can either be well graded or poorly
        graded.

        :param str coarse_soil: Coarse fraction of the soil sample. Valid
            arguments are "G" for gravel and "S" for SAND.
        """

        if coarse_soil == GRAVEL and (
            1 < self.coeff_of_curvature < 3 and self.coeff_of_uniformity >= 4
        ):
            grade = WELL_GRADED

        elif coarse_soil == SAND and (
            1 < self.coeff_of_curvature < 3 and self.coeff_of_uniformity >= 6
        ):
            grade = WELL_GRADED

        else:
            grade = POORLY_GRADED

        return grade


# @attrs.define
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
    >>> from geolysis.core.soil_classifier import PSD, SizeDistribution

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

    def __init__(
        self,
        fines: int | float,
        sand: int | float,
        size_dist: Optional[SizeDistribution] = None,
    ):
        self.fines = fines
        self.sand = sand
        self.gravel = 100 - (fines + sand)
        self.size_dist = size_dist if size_dist else SizeDistribution(0, 0, 0)

    @property
    def type_of_coarse(self) -> str:
        """Determines whether the soil is either gravel or sand."""
        return GRAVEL if self.gravel > self.sand else SAND

    @property
    @round_(2)
    def coeff_of_curvature(self) -> int | float:
        r"""Coefficient of curvature of soil sample.

        Coefficient of curvature :math:`(C_c)` is given by the formula:

        .. math:: C_c = \dfrac{D^2_{30}}{D_{60} \times D_{10}}

        For the soil to be well graded, the value of :math:`C_c` must be
        between 1 and 3.
        """
        return self.size_dist.coeff_of_curvature

    @property
    @round_(2)
    def coeff_of_uniformity(self) -> int | float:
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
        return any(attrs.astuple(self.size_dist))

    def grade(self) -> str:
        r"""Return the grade of the soil sample, either well graded or poorly
        graded.

        Conditions for a well-graded soil:

        - :math:`1 \lt C_c \lt 3` and :math:`C_u \ge 4` (for gravels)
        - :math:`1 \lt C_c \lt 3` and :math:`C_u \ge 6` (for sands)
        """
        return self.size_dist.grade(coarse_soil=self.type_of_coarse)


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
    >>> from geolysis.core.soil_classifier import AASHTO

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

    SOIL_DESCRIPTIONS: Final = {
        "A-1-a": "Stone fragments, gravel, and sand",
        "A-1-b": "Stone fragments, gravel, and sand",
        "A-3": "Fine sand",
        "A-2-4": "Silty or clayey gravel and sand",
        "A-2-5": "Silty or clayey gravel and sand",
        "A-2-6": "Silty or clayey gravel and sand",
        "A-2-7": "Silty or clayey gravel and sand",
        "A-4": "Silty soils",
        "A-5": "Silty soils",
        "A-6": "Clayey soils",
        "A-7-5": "Clayey soils",
        "A-7-6": "Clayey soils",
    }

    def __init__(
        self,
        liquid_limit: int | float,
        plastic_limit: int | float,
        fines: int | float,
        add_group_idx=True,
    ):
        self.liquid_limit = liquid_limit
        self.plastic_limit = plastic_limit
        self.plasticity_index = liquid_limit - plastic_limit
        self.fines = fines
        self.add_group_idx = add_group_idx

    def _classify(self) -> str:
        # Silts A4-A7
        if self.fines > 35:
            soil_class = self._fine_soil_classifier()
        # Coarse A1-A3
        else:
            soil_class = self._coarse_soil_classifier()
        if self.add_group_idx:
            soil_class = f"{soil_class}({self.group_index():.0f})"
        return str(soil_class)

    def _coarse_soil_classifier(self) -> str:
        # A-3, Fine sand
        LL = self.liquid_limit
        PI = self.plasticity_index

        if self.fines <= 10 and isclose(PI, 0, rel_tol=0.01):
            soil_class = A_3
        # A-1-a -> A-1-b, Stone fragments, gravel, and sand
        elif self.fines <= 15 and PI <= 6:
            soil_class = A_1_a
        elif self.fines <= 25 and PI <= 6:
            soil_class = A_1_b
        # A-2-4 -> A-2-7, Silty or clayey gravel and sand
        elif LL <= 40:
            soil_class = A_2_4 if PI <= 10 else A_2_6
        else:
            soil_class = A_2_5 if PI <= 10 else A_2_7

        return soil_class

    def _fine_soil_classifier(self) -> str:
        # A-4 -> A-5, Silty Soils
        # A-6 -> A-7, Clayey Soils
        LL = self.liquid_limit
        PI = self.plasticity_index

        if LL <= 40:
            soil_class = A_4 if PI <= 10 else A_6
        else:
            if PI <= 10:
                soil_class = A_5
            else:
                soil_class = A_7_5 if PI <= (LL - 30) else A_7_6
        return soil_class

    def classify(self) -> str:
        """Return the AASHTO classification of the soil."""
        return self._classify()

    def description(self) -> str:
        """Return the AASHTO description of the soil."""
        tmp_state = self.add_group_idx
        self.add_group_idx = False
        soil_cls = self.classify()
        self.add_group_idx = tmp_state
        return AASHTO.SOIL_DESCRIPTIONS[soil_cls]

    def group_index(self) -> int | float:
        """Return the Group Index (GI) of the soil sample."""

        LL = self.liquid_limit
        PI = self.plasticity_index
        F_200 = self.fines

        a = 1 if (x_0 := F_200 - 35) < 0 else min(x_0, 40)
        b = 1 if (x_0 := LL - 40) < 0 else min(x_0, 20)
        c = 1 if (x_0 := F_200 - 15) < 0 else min(x_0, 40)
        d = 1 if (x_0 := PI - 10) < 0 else min(x_0, 20)

        return round(a * (0.2 + 0.005 * b) + 0.01 * c * d, 0)


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
      sieve, it is designated as fine grained soil.

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
    >>> from geolysis.core.soil_classifier import (
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

    SOIL_DESCRIPTIONS: Final = {
        "G": "Gravel",
        "S": "Sand",
        "M": "Silt",
        "C": "Clay",
        "O": "Organic",
        "W": "Well graded",
        "P": "Poorly graded",
        "L": "Low plasticity",
        "H": "High plasticity",
        "GW": "Well graded gravels",
        "GP": "Poorly graded gravels",
        "GM": "Silty gravels",
        "GC": "Clayey gravels",
        "GM-GC": "Gravelly clayey silt",
        "GW-GM": "Well graded gravel with silt",
        "GP-GM": "Poorly graded gravel with silt",
        "GW-GC": "Well graded gravel with clay",
        "GP-GC": "Poorly graded gravel with clay",
        "SW": "Well graded sands",
        "SP": "Poorly graded sands",
        "SM": "Silty sands",
        "SC": "Clayey sands",
        "SM-SC": "Sandy clayey silt",
        "SW-SM": "Well graded sand with silt",
        "SP-SM": "Poorly graded sand with silt",
        "SW-SC": "Well graded sand with clay",
        "SP-SC": "Poorly graded sand with clay",
        "ML": "Inorganic silts with low plasticity",
        "CL": "Inorganic clays with low plasticity",
        "ML-CL": "Clayey silt with low plasticity",
        "OL": "Organic clays with low plasticity",
        "MH": "Inorganic silts with high plasticity",
        "CH": "Inorganic clays with high plasticity",
        "OH": "Organic silts with high plasticity",
        "Pt": "Highly organic soils",
    }

    def __init__(
        self,
        atterberg_limits: AtterbergLimits,
        psd: PSD,
        organic=False,
    ):
        self.atterberg_limits = atterberg_limits
        self.psd = psd
        self.organic = organic

    def _classify(self) -> str:
        # Fine grained, Run Atterberg
        if self.psd.fines > 50:
            return self._fine_soil_classifier()

        # Coarse grained, Run Sieve Analysis
        # Gravel or Sand
        return self._coarse_soil_classifier()

    def _dual_soil_classifier(self) -> str:
        fine_soil = self.atterberg_limits.type_of_fines
        coarse_soil = self.psd.type_of_coarse

        return f"{coarse_soil}{self.psd.grade()}-{coarse_soil}{fine_soil}"

    def _coarse_soil_classifier(self) -> str:
        coarse_soil = self.psd.type_of_coarse

        # More than 12% pass No. 200 sieve
        if self.psd.fines > 12:
            # Above A-line
            if self.atterberg_limits.above_A_LINE():
                soil_class = f"{coarse_soil}{CLAY}"

            # Limit plot in hatched zone on plasticity chart
            elif self.atterberg_limits.limit_plot_in_hatched_zone():
                soil_class = f"{coarse_soil}{SILT}-{coarse_soil}{CLAY}"

            # Below A-line
            else:
                soil_class = f"{coarse_soil}{SILT}"

        elif 5 <= self.psd.fines <= 12:
            # Requires dual symbol based on graduation and plasticity chart
            if self.psd.has_particle_sizes():
                soil_class = self._dual_soil_classifier()

            else:
                fine_soil = self.atterberg_limits.type_of_fines
                soil_class = (
                    f"{coarse_soil}{WELL_GRADED}-{coarse_soil}{fine_soil},"
                    f"{coarse_soil}{POORLY_GRADED}-{coarse_soil}{fine_soil}"
                )

        # Less than 5% pass No. 200 sieve
        # Obtain Cc and Cu from grain size graph
        else:
            if self.psd.has_particle_sizes():
                soil_class = f"{coarse_soil}{self.psd.grade()}"

            else:
                soil_class = (
                    f"{coarse_soil}{WELL_GRADED},{coarse_soil}{POORLY_GRADED}"
                )

        return soil_class

    def _fine_soil_classifier(self) -> str:
        LL = self.atterberg_limits.liquid_limit
        PI = self.atterberg_limits.plasticity_index

        if LL < 50:
            # Low LL
            # Above A-line and PI > 7
            if (self.atterberg_limits.above_A_LINE()) and (PI > 7):
                soil_class = f"{CLAY}{LOW_PLASTICITY}"

            # Limit plot in hatched area on plasticity chart
            elif self.atterberg_limits.limit_plot_in_hatched_zone():
                soil_class = f"{SILT}{LOW_PLASTICITY}-{CLAY}{LOW_PLASTICITY}"

            # Below A-line or PI < 4
            else:
                if self.organic:
                    soil_class = f"{ORGANIC}{LOW_PLASTICITY}"
                else:
                    soil_class = f"{SILT}{LOW_PLASTICITY}"

        # High LL
        else:
            # Above A-Line
            if self.atterberg_limits.above_A_LINE():
                soil_class = f"{CLAY}{HIGH_PLASTICITY}"

            # Below A-Line
            else:
                if self.organic:
                    soil_class = f"{ORGANIC}{HIGH_PLASTICITY}"
                else:
                    soil_class = f"{SILT}{HIGH_PLASTICITY}"

        return soil_class

    def classify(self) -> str:
        """Return the USCS classification of the soil."""
        return self._classify()

    def description(self) -> str:
        """Return the USCS description of the soil."""
        clf = self.classify()
        soil_desc = [USCS.SOIL_DESCRIPTIONS[cls] for cls in clf.split(",")]
        return " or ".join(soil_desc)


def create_soil_classifier(
    *,
    liquid_limit: int | float,
    plastic_limit: int | float,
    fines: int | float,
    sand: Optional[float] = None,
    d_10: int | float = 0,
    d_30: int | float = 0,
    d_60: int | float = 0,
    add_group_idx: bool = True,
    organic: bool = False,
    clf_type: SCType = SCType.AASHTO,
) -> AASHTO | USCS:
    if clf_type is SCType.AASHTO:
        return AASHTO(
            liquid_limit=liquid_limit,
            plastic_limit=plastic_limit,
            fines=fines,
            add_group_idx=add_group_idx,
        )

    if sand is None:
        raise ValueError("sand is required for USCS classification")

    al = AtterbergLimits(
        liquid_limit=liquid_limit,
        plastic_limit=plastic_limit,
    )
    size_dist = SizeDistribution(d_10=d_10, d_30=d_30, d_60=d_60)
    psd = PSD(fines=fines, sand=sand, size_dist=size_dist)
    return USCS(atterberg_limits=al, psd=psd, organic=organic)
