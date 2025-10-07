import enum
from dataclasses import dataclass
from typing import Annotated, Sequence, Optional

from func_validator import (
    validate_params,
    MustBeNonNegative,
    MustBePositive,
)

from .utils import isclose, round_

__all__ = [
    "AtterbergLimits",
    "PSD",
    "AASHTO",
    "USCS",
    "create_aashto_classifier",
    "create_uscs_classifier",
]


class SizeDistError(ZeroDivisionError):
    """Exception raised when size distribution is not provided."""


class _Clf(tuple, enum.Enum):

    def __str__(self) -> str:
        return self.name

    @property
    def symbol(self) -> str:
        return self.value[0]

    @property
    def description(self) -> str:
        return self.value[1]


class USCSSymbol(_Clf):
    """Unified Soil Classification System (USCS) symbols and descriptions.

    Each member represents a USCS soil type, grading, or plasticity symbol.
    Aliases are provided where applicable.
    """

    # General soil types
    G = ("G", "Gravel")
    """Gravel"""

    GRAVEL = G

    S = ("S", "Sand")
    """Sand"""

    SAND = S

    M = ("M", "Silt")
    """Silt"""

    SILT = M

    C = ("C", "Clay")
    """Clay"""

    CLAY = C

    O = ("O", "Organic")
    """Organic soil"""

    ORGANIC = O

    # Grading descriptors
    W = ("W", "Well graded")
    """Well graded"""

    WELL_GRADED = W

    P = ("P", "Poorly graded")
    """Poorly graded"""

    POORLY_GRADED = P

    # Plasticity descriptors
    L = ("L", "Low plasticity")
    """Low plasticity"""

    LOW_PLASTICITY = L

    H = ("H", "High plasticity")
    """High plasticity"""

    HIGH_PLASTICITY = H

    # Gravels
    GW = ("GW", "Well graded gravels")
    """Well graded gravels"""

    GP = ("GP", "Poorly graded gravels")
    """Poorly graded gravels"""

    GM = ("GM", "Silty gravels")
    """Silty gravels"""

    GC = ("GC", "Clayey gravels")
    """Clayey gravels"""

    GM_GC = ("GM-GC", "Gravelly clayey silt")
    """Gravelly clayey silt"""

    GW_GM = ("GW-GM", "Well graded gravel with silt")
    """Well graded gravel with silt"""

    GP_GM = ("GP-GM", "Poorly graded gravel with silt")
    """Poorly graded gravel with silt"""

    GW_GC = ("GW-GC", "Well graded gravel with clay")
    """Well graded gravel with clay"""

    GP_GC = ("GP-GC", "Poorly graded gravel with clay")
    """Poorly graded gravel with clay"""

    # Sands
    SW = ("SW", "Well graded sands")
    """Well graded sands"""

    SP = ("SP", "Poorly graded sands")
    """Poorly graded sands"""

    SM = ("SM", "Silty sands")
    """Silty sands"""

    SC = ("SC", "Clayey sands")
    """Clayey sands"""

    SM_SC = ("SM-SC", "Sandy clayey silt")
    """Sandy clayey silt"""

    SW_SM = ("SW-SM", "Well graded sand with silt")
    """Well graded sand with silt"""

    SP_SM = ("SP-SM", "Poorly graded sand with silt")
    """Poorly graded sand with silt"""

    SW_SC = ("SW-SC", "Well graded sand with clay")
    """Well graded sand with clay"""

    SP_SC = ("SP-SC", "Poorly graded sand with clay")
    """Poorly graded sand with clay"""

    # Silts and clays
    ML = ("ML", "Inorganic silts with low plasticity")
    """Inorganic silts with low plasticity"""

    CL = ("CL", "Inorganic clays with low plasticity")
    """Inorganic clays with low plasticity"""

    ML_CL = ("ML-CL", "Clayey silt with low plasticity")
    """Clayey silt with low plasticity"""

    OL = ("OL", "Organic clays with low plasticity")
    """Organic clays with low plasticity"""

    MH = ("MH", "Inorganic silts with high plasticity")
    """Inorganic silts with high plasticity"""

    CH = ("CH", "Inorganic clays with high plasticity")
    """Inorganic clays with high plasticity"""

    OH = ("OH", "Organic silts with high plasticity")
    """Organic silts with high plasticity"""

    Pt = ("Pt", "Highly organic soils")
    """Highly organic soils"""


class AASHTOSymbol(_Clf):
    """
    AASHTO soil classification symbols and descriptions.

    Each member represents a standard AASHTO soil class used in
    pavement and highway engineering.
    """

    A_1_a = ("A-1-a", "Stone fragments, gravel, and sand")
    """Stone fragments, gravel, and sand"""

    A_1_b = ("A-1-b", "Stone fragments, gravel, and sand")
    """Stone fragments, gravel, and sand"""

    A_3 = ("A-3", "Fine sand")
    """Fine sand"""

    A_2_4 = ("A-2-4", "Silty or clayey gravel and sand")
    """Silty or clayey gravel and sand"""

    A_2_5 = ("A-2-5", "Silty or clayey gravel and sand")
    """Silty or clayey gravel and sand"""

    A_2_6 = ("A-2-6", "Silty or clayey gravel and sand")
    """Silty or clayey gravel and sand"""

    A_2_7 = ("A-2-7", "Silty or clayey gravel and sand")
    """Silty or clayey gravel and sand"""

    A_4 = ("A-4", "Silty soils")
    """Silty soils"""

    A_5 = ("A-5", "Silty soils")
    """Silty soils"""

    A_6 = ("A-6", "Clayey soils")
    """Clayey soils"""

    A_7_5 = ("A-7-5", "Clayey soils")
    """Clayey soils"""

    A_7_6 = ("A-7-6", "Clayey soils")
    """Clayey soils"""


class AtterbergLimits:
    """Represents the water contents at which soil changes from one state
    to the other.
    """

    class __A_LINE:

        def __get__(self, obj, objtype=None) -> float:
            return 0.73 * (obj.liquid_limit - 20.0)

    A_LINE = __A_LINE()
    """The ``A-line`` determines if a soil is clayey or silty.
    
    $A = 0.73(LL - 20.0)$
    """

    def __init__(self, liquid_limit: float, plastic_limit: float):
        """
        :param liquid_limit: Water content beyond which soils flows
                             under their own weight (%). It can also be
                             defined as the minimum moisture content at
                             which a soil flows upon application of a
                             very small shear force.
        :param plastic_limit: Water content at which plastic deformation
                              can be initiated (%). It is also the
                              minimum water content at which soil can be
                              rolled into a thread 3mm thick (molded
                              without breaking).
        """
        self.liquid_limit = liquid_limit
        self.plastic_limit = plastic_limit

    @property
    def liquid_limit(self) -> float:
        """
        Water content beyond which soils flows under their own weight (%).
        """
        return self._liquid_limit

    @liquid_limit.setter
    @validate_params
    def liquid_limit(self,
                     liquid_limit: Annotated[float, MustBeNonNegative()]):
        self._liquid_limit = liquid_limit

    @property
    def plastic_limit(self) -> float:
        """
        Water content at which plastic deformation can be initiated (%).
        """
        return self._plastic_limit

    @plastic_limit.setter
    @validate_params
    def plastic_limit(self,
                      plastic_limit: Annotated[float, MustBeNonNegative()]):
        if self.liquid_limit < plastic_limit:
            msg = (
                f"plastic_limit: {plastic_limit} cannot be greater than "
                f"liquid_limit: {self.liquid_limit}"
            )
            raise ValueError(msg)

        self._plastic_limit = plastic_limit

    @property
    @round_(2)
    def plasticity_index(self) -> float:
        """Plasticity index (PI) is the range of water content over which
        the soil remains in the plastic state.

        It is also the numerical difference between the liquid limit and
        plastic limit of the soil.

        $$PI = LL - PL$$
        """
        return self.liquid_limit - self.plastic_limit

    @property
    def fine_material_type(self) -> USCSSymbol:
        """Checks whether the soil is either clay or silt."""
        return USCSSymbol.CLAY if self.above_A_LINE() else USCSSymbol.SILT

    def above_A_LINE(self) -> bool:
        """Checks if the soil sample is above A-Line."""
        return self.plasticity_index > self.A_LINE

    def limit_plot_in_hatched_zone(self) -> bool:
        """Checks if soil sample plot in the hatched zone on the
        atterberg chart.
        """
        return 4 <= self.plasticity_index <= 7 and 10 < self.liquid_limit < 30

    @round_(ndigits=2)
    def liquidity_index(self, nmc: float) -> float:
        r"""Return the liquidity index of the soil.

        $$I_l = \dfrac{w - PL}{PI} \cdot 100$$

        Liquidity index of a soil indicates the nearness of its
        `natural water content` to its `liquid limit`. When the soil
        is at the plastic limit its liquidity index is zero. Negative
        values of the liquidity index indicate that the soil is in a
        hard (desiccated) state. It is also known as Water-Plasticity
        ratio.

        :param nmc: Moisture contents of the soil in natural condition.
        """
        return ((nmc - self.plastic_limit) / self.plasticity_index) * 100.0

    @round_(2)
    def consistency_index(self, nmc: float) -> float:
        r"""Return the consistency index of the soil.

        $$I_c = \dfrac{LL - w}{PI} \cdot 100$$

        Consistency index indicates the consistency (firmness) of soil.
        It shows the nearness of the ``natural water content`` of the
        soil to its `plastic limit`. When the soil is at the liquid
        limit, the consistency index is zero. The soil at consistency
        index of zero will be extremely soft and has negligible shear
        strength. A soil at a water content equal to the plastic limit
        has consistency index of 100% indicating that the soil is
        relatively firm. A consistency index of greater than 100% shows
        the soil is relatively strong (semi-solid state). A negative
        value indicate the soil is in the liquid state. It is also known
        as Relative Consistency.

        :param nmc: Moisture contents of the soil in natural condition.
        """
        return ((self.liquid_limit - nmc) / self.plasticity_index) * 100.0


class _SizeDistribution:
    """Particle size distribution of soil sample.

    Features obtained from the Particle Size Distribution graph.
    """

    def __init__(self, d_10: float, d_30: float, d_60: float):
        self.d_10 = d_10
        self.d_30 = d_30
        self.d_60 = d_60

    def __iter__(self):
        return iter([self.d_10, self.d_30, self.d_60])

    @property
    def coeff_of_curvature(self) -> float:
        return (self.d_30 ** 2.0) / (self.d_60 * self.d_10)

    @property
    def coeff_of_uniformity(self) -> float:
        return self.d_60 / self.d_10

    def grade(self, coarse_soil: USCSSymbol) -> USCSSymbol:
        """Grade of soil sample. Soil grade can either be well graded or
        poorly graded.

        :param coarse_soil: Coarse fraction of the soil sample.
        """
        if coarse_soil is USCSSymbol.GRAVEL:
            if 1 < self.coeff_of_curvature < 3 and self.coeff_of_uniformity >= 4:
                grade = USCSSymbol.WELL_GRADED
            else:
                grade = USCSSymbol.POORLY_GRADED
            return grade

        # coarse soil is sand
        if 1 < self.coeff_of_curvature < 3 and self.coeff_of_uniformity >= 6:
            grade = USCSSymbol.WELL_GRADED
        else:
            grade = USCSSymbol.POORLY_GRADED
        return grade

    def has_particle_sizes(self) -> bool:
        """Checks if particle sizes are provided."""
        return all((self.d_10, self.d_30, self.d_60))


class PSD:
    """Quantitative proportions by mass of various sizes of particles
    present in a soil.
    """

    def __init__(
            self,
            fines: float,
            sand: float,
            d_10: float | None = None,
            d_30: float | None = None,
            d_60: float | None = None,
    ):
        """
        :param fines: Percentage of fines in soil sample (%) i.e. The
                      percentage of soil sample passing through No. 200
                      sieve (0.075mm).
        :param sand: Percentage of sand in soil sample (%).
        :param d_10: Diameter at which 10% of the soil by weight is finer.
        :param d_30: Diameter at which 30% of the soil by weight is finer.
        :param d_60: Diameter at which 60% of the soil by weight is finer.
        """
        self.fines = fines
        self.sand = sand
        self.size_dist = _SizeDistribution(d_10=d_10, d_30=d_30, d_60=d_60)

    @property
    def gravel(self):
        """Percentage of gravel in soil sample (%)."""
        return 100.0 - (self.fines + self.sand)

    @property
    def coarse_material_type(self) -> USCSSymbol:
        """Determines whether the soil is either gravel or sand."""
        if self.gravel > self.sand:
            return USCSSymbol.GRAVEL
        return USCSSymbol.SAND

    @property
    @round_(ndigits=2)
    def coeff_of_curvature(self) -> float:
        r"""Coefficient of curvature of soil sample.

        $$C_c = \dfrac{D^2_{30}}{D_{60} \cdot D_{10}}$$

        For the soil to be well graded, the value of $C_c$ must be
        between 1 and 3.
        """
        return self.size_dist.coeff_of_curvature

    @property
    @round_(ndigits=2)
    def coeff_of_uniformity(self) -> float:
        r"""Coefficient of uniformity of soil sample.

        $$C_u = \dfrac{D_{60}}{D_{10}}$$

        $C_u$ value greater than 4 to 6 classifies the soil as well
        graded for gravels and sands respectively. When $C_u$ is less
        than 4, it is classified as poorly graded or uniformly graded
        soil.

        Higher values of $C_u$ indicates that the soil mass consists of
        soil particles with different size ranges.
        """
        return self.size_dist.coeff_of_uniformity

    def has_particle_sizes(self) -> bool:
        """Checks if soil sample has particle sizes."""
        return self.size_dist.has_particle_sizes()

    def grade(self) -> USCSSymbol:
        r"""Return the grade of the soil sample, either well graded or
        poorly graded.

        Conditions for a well-graded soil:

        - $1 \lt C_c \lt 3$ and $C_u \ge 4$ (for gravels)
        - $1 \lt C_c \lt 3$ and $C_u \ge 6$ (for sands)
        """
        return self.size_dist.grade(coarse_soil=self.coarse_material_type)


@dataclass(frozen=True, slots=True)
class AASHTOResult:
    symbol: str
    symbol_no_group_idx: str
    description: str
    group_index: str


class AASHTO:
    r"""American Association of State Highway and Transportation
    Officials (AASHTO) classification system.

    The AASHTO classification system is useful for classifying soils for
    highways. It categorizes soils for highways based on particle size
    analysis and plasticity characteristics. It classifies both
    coarse-grained and fine-grained soils into eight main groups (A1-A7)
    with subgroups, along with a separate category (A8) for organic
    soils.

    - `A1 ~ A3` (Granular Materials) $\le$ 35% pass No. 200 sieve
    - `A4 ~ A7` (Silt-clay Materials) $\ge$ 36% pass No. 200 sieve
    - `A8` (Organic Materials)

    The Group Index `(GI)` is used to further evaluate soils within a
    group.

    !!! note

        The `GI` must be mentioned even when it is zero, to indicate
        that the soil has been classified as per AASHTO system.


    $$
    GI = (F_{200} - 35)[0.2 + 0.005(LL - 40)] + 0.01(F_{200} - 15)(PI - 10)
    $$
    """

    def __init__(self, atterberg_limits: AtterbergLimits, fines: float):
        """
        :param atterberg_limits: Atterberg limits of soil sample.

        :param fines: Percentage of fines in soil sample (%) i.e. The
                      percentage of soil sample passing through No. 200
                      sieve (0.075mm).
        """
        self.atterberg_limits = atterberg_limits
        self.fines = fines

    @property
    def fines(self) -> float:
        """Percentage of fines in soil sample (%)."""
        return self._fines

    @fines.setter
    @validate_params
    def fines(self, fines: Annotated[float, MustBeNonNegative()]):
        self._fines = fines

    @round_(ndigits=0)
    def group_index(self) -> float:
        """Return the Group Index (GI) of the soil sample."""
        liquid_lmt = self.atterberg_limits.liquid_limit
        plasticity_idx = self.atterberg_limits.plasticity_index
        fines = self.fines

        x_1 = 1.0 if (x_0 := fines - 35.0) < 0.0 else min(x_0, 40.0)
        x_2 = 1.0 if (x_0 := liquid_lmt - 40.0) < 0.0 else min(x_0, 20.0)
        x_3 = 1.0 if (x_0 := fines - 15.0) < 0.0 else min(x_0, 40.0)
        x_4 = 1.0 if (x_0 := plasticity_idx - 10.0) < 0.0 else min(x_0, 20.0)

        return x_1 * (0.2 + 0.005 * x_2) + 0.01 * x_3 * x_4

    def classify(self) -> AASHTOResult:
        """Return the AASHTO classification of the soil."""
        soil_clf = self._classify()

        symbol_no_grp_idx, description = soil_clf.symbol, soil_clf.description
        group_idx = f"{self.group_index():.0f}"
        symbol = f"{symbol_no_grp_idx}({group_idx})"

        return AASHTOResult(
            symbol=symbol,
            symbol_no_group_idx=symbol_no_grp_idx,
            description=description,
            group_index=group_idx,
        )

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
        liquid_lmt = self.atterberg_limits.liquid_limit
        plasticity_idx = self.atterberg_limits.plasticity_index

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
        liquid_lmt = self.atterberg_limits.liquid_limit
        plasticity_idx = self.atterberg_limits.plasticity_index

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


@dataclass(frozen=True, slots=True)
class USCSResult:
    symbol: str
    description: str


class USCS:
    """Unified Soil Classification System (USCS).

    The Unified Soil Classification System, initially developed by
    Casagrande in 1948 and later modified in 1952, is widely utilized in
    engineering projects involving soils. It is the most popular system
    for soil classification and is similar to Casagrande's
    Classification System. The system relies on particle size analysis
    and atterberg limits for classification.

    In this system, soils are first classified into two categories:

    - Coarse grained soils: If more than 50% of the soils is retained on
      No. 200 (0.075 mm) sieve, it is designated as coarse-grained soil.

    - Fine grained soils: If more than 50% of the soil passes through
      No. 200 sieve, it is designated as fine-grained soil.

    Highly Organic soils are identified by visual inspection. These
    soils are termed as Peat ($P_t$).
    """

    def __init__(
            self,
            atterberg_limits: AtterbergLimits,
            psd: PSD,
            organic=False,
    ):
        """
        :param atterberg_limits: Atterberg limits of the soil.
        :param psd: Particle size distribution of the soil.
        :param organic: Indicates whether soil is organic or not.
        """
        self.atterberg_limits = atterberg_limits
        self.psd = psd
        self.organic = organic

    def classify(self):
        """Return the USCS classification of the soil."""
        soil_clf = self._classify()

        # Ensure soil_clf is of type USCSSymbol
        if isinstance(soil_clf, str):
            soil_clf = USCSSymbol[soil_clf]

        if isinstance(soil_clf, USCSSymbol):
            soil_clf = USCSResult(
                symbol=soil_clf.symbol,
                description=soil_clf.description,
            )
        else:
            # Handling tuple or list case for dual classification
            first_clf, second_clf = map(lambda clf: USCSSymbol[clf], soil_clf)
            comb_symbol = f"{first_clf.symbol},{second_clf.symbol}"
            comb_desc = f"{first_clf.description},{second_clf.description}"
            soil_clf = USCSResult(symbol=comb_symbol, description=comb_desc)

        return soil_clf

    def _classify(self) -> USCSSymbol | str | Sequence[str]:
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

    def _coarse_soil_classifier(self) -> USCSSymbol | str | Sequence[str]:
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
                soil_clf = (
                    f"{coarse_material_type}{USCSSymbol.WELL_GRADED}_"
                    f"{coarse_material_type}{fine_material_type}",
                    f"{coarse_material_type}{USCSSymbol.POORLY_GRADED}_"
                    f"{coarse_material_type}{fine_material_type}",
                )

        # Less than 5% pass No. 200 sieve
        # Obtain Cc and Cu from grain size graph
        else:
            if self.psd.has_particle_sizes():
                soil_clf = f"{coarse_material_type}{self.psd.grade()}"

            else:
                soil_clf = (
                    f"{coarse_material_type}{USCSSymbol.WELL_GRADED}",
                    f"{coarse_material_type}{USCSSymbol.POORLY_GRADED}",
                )

        return soil_clf

    def _dual_soil_classifier(self) -> str:
        fine_material_type = self.atterberg_limits.fine_material_type
        coarse_material_type = self.psd.coarse_material_type

        return (
            f"{coarse_material_type}{self.psd.grade()}_"
            f"{coarse_material_type}{fine_material_type}"
        )


def create_aashto_classifier(
        liquid_limit: float,
        plastic_limit: float,
        fines: float,
) -> AASHTO:
    """A helper function that encapsulates the creation of a AASHTO
    classifier.

    :param liquid_limit: Water content beyond which soils flows under
                         their own weight (%). It can also be defined as
                         the minimum moisture content at which a soil
                         flows upon application of a very small shear
                         force.
    :param plastic_limit: Water content at which plastic deformation can
                          be initiated (%). It is also the minimum water
                          content at which soil can be rolled into a
                          thread 3mm thick (molded without breaking).
    :param fines: Percentage of fines in soil sample (%) i.e. The
                  percentage of soil sample passing through No. 200
                  sieve (0.075mm).
    """
    atterberg_limits = AtterbergLimits(liquid_limit, plastic_limit)
    return AASHTO(atterberg_limits, fines)


@validate_params
def create_uscs_classifier(
        liquid_limit: float,
        plastic_limit: float,
        fines: float,
        sand: float,
        d_10: Annotated[Optional[float], MustBePositive()] = None,
        d_30: Annotated[Optional[float], MustBePositive()] = None,
        d_60: Annotated[Optional[float], MustBePositive()] = None,
        organic: bool = False,
):
    """A helper function that encapsulates the creation of a USCS
    classifier.

    :param liquid_limit: Water content beyond which soils flows under
                         their own weight (%). It can also be defined as
                         the minimum moisture content at which a soil
                         flows upon application of a very small shear
                         force.
    :param plastic_limit: Water content at which plastic deformation can
                          be initiated (%). It is also the minimum water
                          content at which soil can be rolled into a
                          thread 3mm thick. (molded without breaking)
    :param fines: Percentage of fines in soil sample (%) i.e. The
                  percentage of soil sample passing through No. 200
                  sieve (0.075mm).
    :param sand: Percentage of sand in soil sample (%).
    :param d_10: Diameter at which 10% of the soil by weight is finer.
    :param d_30: Diameter at which 30% of the soil by weight is finer.
    :param d_60: Diameter at which 60% of the soil by weight is finer.
    :param organic: Indicates whether soil is organic or not.
    """
    atterberg_lmts = AtterbergLimits(liquid_limit, plastic_limit)
    psd = PSD(fines=fines, sand=sand, d_10=d_10, d_30=d_30, d_60=d_60)
    return USCS(atterberg_limits=atterberg_lmts, psd=psd, organic=organic)
