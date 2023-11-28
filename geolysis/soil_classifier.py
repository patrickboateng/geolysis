"""This module provides the implementations for ``USCS`` and ``AASHTO``
classification.
"""

from math import trunc
from types import MappingProxyType

from geolysis import ERROR_TOLERANCE, exceptions
from geolysis.utils import isclose, round_

GRAVEL = "G"
SAND = "S"
CLAY = "C"
SILT = "M"
WELL_GRADED = "W"
POORLY_GRADED = "P"
ORGANIC = "O"
LOW_PLASTICITY = "L"
HIGH_PLASTICITY = "H"


def _check_size_distribution(fines: float, sand: float, gravel: float):
    total_aggregate = fines + sand + gravel
    if not isclose(total_aggregate, 100, rel_tol=ERROR_TOLERANCE):
        msg = f"fines + sand + gravels = 100% not {total_aggregate}"
        raise exceptions.PSDValueError(msg)


class AtterbergLimits:
    """Atterberg Limits.

    In 1911, a Swedish agriculture engineer ``Atterberg`` mentioned
    that  a fined-grained soil can exist in four states, namely,
    liquid, plastic, semi-solid or solid state.

    The water contents at which the soil changes from one state to
    other are known as ``Atterberg limits`` or ``Consistency limits``.
    The main use of consistency limits is in the classification of
    soils.

    :param float liquid_limit:
        Water content beyond which soils flows under their own weight.
        It can also be defined as the minimum moisture content at
        which a soil flows upon application of a very small shear force.
    :param float plastic_limit:
        Water content at which plastic deformation can be initiated.
        It is also the minimum water content at which soil can be rolled
        into a thread 3mm thick (molded without breaking)
    """

    def __init__(self, liquid_limit: float, plastic_limit: float):
        self.liquid_limit = liquid_limit
        self.plastic_limit = plastic_limit

    @property
    @round_(precision=2)
    def A_line(self) -> float:
        r"""Return the ``A-line``.

        .. math::

            0.73 \left(LL - 20 \right)
        """
        return 0.73 * (self.liquid_limit - 20)

    @property
    def type_of_fines(self) -> str:
        """Return the type of fine soil, either CLAY or SILT."""
        return CLAY if self.above_A_LINE() else SILT

    def above_A_LINE(self) -> bool:
        """Checks if the soil sample is above A-Line."""
        return self.plasticity_index > self.A_line

    def limit_plot_in_hatched_zone(self) -> bool:
        """Checks if soil sample plot in the hatched zone."""
        return 4 <= self.plasticity_index <= 7 and 10 < self.liquid_limit < 30

    @property
    def plasticity_index(self) -> float:
        """Return the plasticity index of the soil.

        Plasticity index is the range of water content over which
        the soil remains in the plastic state. It is also the
        numerical difference between the liquid limit and plastic
        limit of the soil.

        .. math::

            PI = LL - PL

        - PI: Plasticity Index
        - LL: Liquid Limit
        - PL: Plastic Limit
        """
        return self.liquid_limit - self.plastic_limit

    def liquidity_index(self, nmc: float) -> float:
        r"""Return the liquidity index of the soil.

        Liquidity index of a soil indicates the nearness of its
        water content to its liquid limit. When the soil is at the
        plastic limit its liquidity index is zero. Negative values
        of the liquidity index indicate that the soil is in a hard
        (desiccated) state. It is also known as ``Water-Plasticity
        ratio``.

        .. math::

            I_l = \dfrac{w - PL}{PI} \cdot 100

        - I_l: Liquidity Index
        - w: Moisture contents of the soil in natural condition.
             (Natural Moisture Content)
        - PL: Plastic Limit
        - PI: Plasticity Index

        :param float nmc:
            Moisture contents of the soil in natural condition.
            (Natural Moisture Content)
        """
        return ((nmc - self.plastic_limit) / self.plasticity_index) * 100

    def consistency_index(self, nmc: float) -> float:
        r"""Return the consistency index of the soil.

        Consistency index indicates the consistency (firmness) of
        soil. It shows the nearness of the water content of the
        soil to its plastic limit. When the soil is at the liquid
        limit, the consistency index is zero. The soil at consistency
        index of zero will be extremely soft and has negligible
        shear strength. A soil at a water content equal to the
        plastic limit has consistency index of 100% indicating that
        the soil is relatively firm. A consistency index of greater
        than 100% shows the soil is relatively strong (semi-solid state).
        A negative value indicate the soil is in the liquid state.
        It is also known as ``Relative Consistency``.

        .. math::

            I_c = \dfrac{LL - w}{PI} \cdot 100

        - I_c: Consistency Index
        - LL: Liquid Limit
        - w: Moisture contents of the soil in natural condition.
             (Natural Moisture Content)
        - PI: Plasticity Index

        :param float nmc:
            Moisture contents of the soil in natural condition.
            (Natural Moisture Content)
        """
        return ((self.liquid_limit - nmc) / self.plasticity_index) * 100


class ParticleSizeDistribution:
    """Particle Size Distribution.

    Particle Size Distribution is a method of separation of soils
    into different fractions based on the particle size. It
    expresses quantitatively the proportions by mass of various
    sizes of particles present in a soil. The analysis is done in
    two stages:

    #. Sieve Analysis: It is meant for coarse grained soils
       (particle size greater than 75 micron) which can easily pass
       through a set of sieves. Coarse grained soils can be subdivided
       into gravel fraction (particle size > 4.75 mm) and sand
       fraction (75 micron < particle size < 4.75 mm).

    #. Sedimentation Analysis: It meant for fine grained soils
       (particle size smaller than 75 micron)

    :param float fines:
        Percentage of fines in soil sample i.e. the percentage of soil
        sample passing through No. 200 sieve (0.075mm)
    :param float sand:
        Percentage of sand in soil sample (%)
    :param float gravel:
        Percentage of gravel in soil sample (%)
    :kwparam float d10:
        Diameter at which 30% of the soil by weight is finer
    :kwparam float d30:
        Diameter at which 30% of the soil by weight is finer
    :kwparam float d60:
        Diameter at which 60% of the soil by weight is finer

    :raises exceptions.PSDValueError:
        Raised when soil aggregates does not approximately sum
        up to 100%
    """

    def __init__(
        self,
        fines: float,
        sand: float,
        gravel: float,
        *,
        d10: float = 0,
        d30: float = 0,
        d60: float = 0,
    ):
        self.fines = fines
        self.sand = sand
        self.gravel = gravel
        self.d10 = d10
        self.d30 = d30
        self.d60 = d60

        _check_size_distribution(self.fines, self.sand, self.gravel)

    def has_particle_sizes(self) -> bool:
        """Checks if soil sample has particle sizes."""
        return all((self.d10, self.d30, self.d60))

    def _sand_grade(self) -> str:
        if (
            1 < self.curvature_coefficient < 3
            and self.uniformity_coefficient >= 6
        ):
            return WELL_GRADED

        return POORLY_GRADED

    def _coarse_grade(self) -> str:
        if (
            1 < self.curvature_coefficient < 3
            and self.uniformity_coefficient >= 4
        ):
            return WELL_GRADED

        return POORLY_GRADED

    def grade(self) -> str:
        """Return the grade of the soil sample."""
        # Gravel
        if self.gravel > self.sand:
            return self._coarse_grade()

        # Sand
        return self._sand_grade()

    @property
    def type_of_coarse(self) -> str:
        if self.gravel > self.sand:
            return GRAVEL

        return SAND

    @property
    @round_(precision=2)
    def curvature_coefficient(self) -> float:
        r"""Return the coefficient of curvature of the soil.

        .. math::

            C_c = \dfrac{D_{30}^2}{D_{60} \cdot D_{10}}
        """
        return (self.d30**2) / (self.d60 * self.d10)

    coefficient_of_curvature = curvature_coefficient
    coefficient_of_gradation = curvature_coefficient

    @property
    @round_(precision=2)
    def uniformity_coefficient(self) -> float:
        r"""Return the coefficient of uniformity of the soil.

        .. math::

            C_u = \dfrac{D_{60}}{D_{10}}
        """
        return self.d60 / self.d10

    coefficient_of_uniformity = uniformity_coefficient


class AASHTOClassification:
    """American Association of State Highway and Transportation
    Officials (``AASHTO``) classification system.

    The AASHTO classification system is useful for classifying soils
    for highways. It categorizes soils for highways based on particle
    size analysis and plasticity characteristics. It classifies both
    coarse-grained and fine-grained soils into eight main groups
    (A1-A7) with subgroups, along with a separate category (A8) for
    organic soils.

    :param float liquid_limit:
        Water content beyond which soils flows under their own weight
    :param float plasticity_index:
        Range of water content over which soil remains in plastic
        condition
    :param float fines:
        Percentage of fines in soil sample i.e. the percentage of soil
        sample passing through No. 200 sieve (0.075mm)
    :param bool grp_idx:
        Used to indicate whether the group index should be added to
        the classification or not. Defaults to True.
    """

    def __init__(
        self,
        liquid_limit: float,
        plasticity_index: float,
        fines: float,
        add_group_index: bool = True,
    ):
        self.liquid_limit = liquid_limit
        self.plasticity_index = plasticity_index
        self.fines = fines
        self.add_group_index = add_group_index

    def group_index(self) -> float:
        """Return the ``Group Index (GI)`` of the soil sample.

        The ``(GI)`` is used to further evaluate soils with a group
        (subgroups). When calculating ``GI`` from the equation below,
        if any term in the parenthesis becomes negative, it is drop
        and not given a negative value. The maximum values of
        :math:`(F_{200} - 35)` and :math:`(F_{200} - 15)` are taken
        as 40 and :math:`(LL - 40)` and :math:`(PI - 10)` as 20.
        If the computed value for ``GI`` is negative, it is reported
        as zero. In general, the rating for the pavement subgrade is
        inversely proportional to the ``GI`` (lower the ``GI``, better
        the material).
        For e.g., a ``GI`` of zero indicates a good subgrade, whereas
        a group index of 20 or greater shows a very poor subgrade.

        .. math::

            GI = (F_{200} - 35)[0.2 + 0.005(LL - 40)] + 0.01(F_{200} - 15)(PI - 10)

        .. note::

            The ``GI`` must be mentioned even when it is zero, to
            indicate that the soil has been classified as per AASHTO
            system.
        """
        x_1 = 1 if (x_0 := self.fines - 35) < 0 else min(x_0, 40)
        x_2 = 1 if (x_0 := self.liquid_limit - 40) < 0 else min(x_0, 20)
        x_3 = 1 if (x_0 := self.fines - 15) < 0 else min(x_0, 40)
        x_4 = 1 if (x_0 := self.plasticity_index - 10) < 0 else min(x_0, 20)
        grp_idx = round(x_1 * (0.2 + 0.005 * x_2) + 0.01 * x_3 * x_4, 0)

        return 0 if grp_idx <= 0 else trunc(grp_idx)

    def _coarse_soil_classifier(self) -> str:
        # A-3, Fine sand
        if self.fines <= 10 and isclose(self.plasticity_index, 0):
            clf = f"A-3"

        # A-1-a -> A-1-b, Stone fragments, gravel, and sand
        elif self.fines <= 15 and self.plasticity_index <= 6:
            clf = f"A-1-a"

        elif self.fines <= 25 and self.plasticity_index <= 6:
            clf = f"A-1-b"

        # A-2-4 -> A-2-7, Silty or clayey gravel and sand
        elif self.liquid_limit <= 40:
            if self.plasticity_index <= 10:
                clf = f"A-2-4"
            else:
                clf = f"A-2-6"

        else:
            if self.plasticity_index <= 10:
                clf = f"A-2-5"
            else:
                clf = f"A-2-7"

        if self.add_group_index:
            return clf + f"({self.group_index()})"
        else:
            return clf

    def _fine_soil_classifier(self) -> str:
        # A-4 -> A-5, Silty Soils
        # A-6 -> A-7, Clayey Soils
        if self.liquid_limit <= 40:
            if self.plasticity_index <= 10:
                clf = f"A-4"
            else:
                clf = f"A-6"

        else:
            if self.plasticity_index <= 10:
                clf = f"A-5"
            else:
                if self.plasticity_index <= (self.liquid_limit - 30):
                    clf = f"A-7-5"
                else:
                    clf = f"A-7-6"

        if self.add_group_index:
            return clf + f"({self.group_index()})"
        else:
            return clf

    def classify(self) -> str:
        """Return the AASHTO classification of the soil sample."""

        # Coarse A1-A3
        if self.fines <= 35:
            return self._coarse_soil_classifier()

        # Silts A4-A7
        return self._fine_soil_classifier()


# @dataclass
class UnifiedSoilClassification:
    """Unified Soil Classification (``USC``) System.

    The Unified Soil Classification System, initially developed
    by Casagrande in 1948 and later modified in 1952, is widely
    utilized in engineering projects involving soils. It is the
    most popular system for soil classification and is similar
    to Casagrande's Classification System. The system relies on
    particle size analysis and atterberg limits for classification.

    In this system, soils are first classified into two categories:

    #. Coarse grained soils: If more than 50% of the soils is
       retained on No. 200 (0.075 mm) sieve, it is designated as
       coarse-grained soil.

    #. Fine grained soils: If more than 50% of the soil passes
       through No. 200 sieve, it is designated as fine grained soil.

    Highly Organic soils are identified by visual inspection.
    These soils are termed as Peat. (:math:`P_t`)

    :param AtterbergLimits atterberg_limits:
        Water content at which soil changes from one state to
        other
    :param ParticleSizeDistribution psd:
        Distribution of soil particles in the soil sample
    """

    soil_descriptions: MappingProxyType[str, str] = MappingProxyType(
        {
            "GW": "Well graded gravels",
            "GP": "Poorly graded gravels",
            "GM": "Silty gravels",
            "GC": "Clayey gravels",
            "GW-GM": "Well graded gravel with silt",
            "GP-GM": "Poorly graded gravel with silt",
            "GW-GC": "Well graded gravel with clay",
            "GP-GC": "Poorly graded gravel with clay",
            "SW": "Well graded sands",
            "SP": "Poorly graded sands",
            "SM": "Silty sands",
            "SC": "Clayey sands",
            "SW-SM": "Well graded sand with silt",
            "SP-SM": "Poorly graded sand with silt",
            "SW-SC": "Well graded sand with clay",
            "SP-SC": "Poorly graded sand with clay",
            "ML": "Inorganic silts of low plasticity",
            "CL": "Inorganic clays of low plasticity",
            "OL": "Organic silts of low plasticity",
            "MH": "Inorganic silts of high plasticity",
            "CH": "Inorganic clays of high plasticity",
            "OH": "Organic silts of high plasticity",
            "Pt": "Highly organic soils",
        }
    )

    def __init__(
        self,
        atterberg_limits: AtterbergLimits,
        psd: ParticleSizeDistribution,
        *,
        organic: bool = False,
    ):
        self.atterberg_limits = atterberg_limits
        self.psd = psd
        self.organic = organic

    def _dual_soil_classifier(self) -> str:
        soil_grd = self.psd.grade()
        fine_soil = self.atterberg_limits.type_of_fines
        coarse_soil = self.psd.type_of_coarse

        return f"{coarse_soil}{soil_grd}-{coarse_soil}{fine_soil}"

    def _coarse_soil_classifier(self) -> str:
        coarse_soil = self.psd.type_of_coarse

        # More than 12% pass No. 200 sieve
        if self.psd.fines > 12:
            # Above A-line
            if self.atterberg_limits.above_A_LINE():
                clf = f"{coarse_soil}{CLAY}"

            # Limit plot in hatched zone on plasticity chart
            elif self.atterberg_limits.limit_plot_in_hatched_zone():
                clf = f"{coarse_soil}{SILT}-{coarse_soil}{CLAY}"

            # Below A-line
            else:
                clf = f"{coarse_soil}{SILT}"

        elif 5 <= self.psd.fines <= 12:
            # Requires dual symbol based on graduation and plasticity chart
            if self.psd.has_particle_sizes():
                clf = self._dual_soil_classifier()

            else:
                fine_soil = self.atterberg_limits.type_of_fines
                clf = (
                    f"{coarse_soil}{WELL_GRADED}-{coarse_soil}{fine_soil},"
                    f"{coarse_soil}{POORLY_GRADED}-{coarse_soil}{fine_soil}"
                )

        # Less than 5% pass No. 200 sieve
        # Obtain Cc and Cu from grain size graph
        else:
            if self.psd.has_particle_sizes():
                soil_grd = self.psd.grade()
                clf = f"{coarse_soil}{soil_grd}"

            else:
                clf = f"{coarse_soil}{WELL_GRADED} or {coarse_soil}{POORLY_GRADED}"

        return clf

    def _fine_soil_classifier(self) -> str:
        if self.atterberg_limits.liquid_limit < 50:
            # Low LL
            # Above A-line and PI > 7
            if (self.atterberg_limits.above_A_LINE()) and (
                self.atterberg_limits.plasticity_index > 7
            ):
                clf = f"{CLAY}{LOW_PLASTICITY}"

            # Limit plot in hatched area on plasticity chart
            elif self.atterberg_limits.limit_plot_in_hatched_zone():
                clf = f"{SILT}{LOW_PLASTICITY}-{CLAY}{LOW_PLASTICITY}"

            # Below A-line or PI < 4
            else:
                if self.organic:
                    clf = f"{ORGANIC}{LOW_PLASTICITY}"

                else:
                    clf = f"{SILT}{LOW_PLASTICITY}"

        # High LL
        else:
            # Above A-Line
            if self.atterberg_limits.above_A_LINE():
                clf = f"{CLAY}{HIGH_PLASTICITY}"

            # Below A-Line
            else:
                if self.organic:
                    clf = f"{ORGANIC}{HIGH_PLASTICITY}"
                else:
                    clf = f"{SILT}{HIGH_PLASTICITY}"

        return clf

    def classify(self) -> str:
        """Return the Unified Soil Classification of the soil sample."""
        # Fine grained, Run Atterberg
        if self.psd.fines > 50:
            return self._fine_soil_classifier()

        # Coarse grained, Run Sieve Analysis
        # Gravel or Sand
        return self._coarse_soil_classifier()

    @classmethod
    def soil_description(cls, clf: str) -> str:
        """Return the typical names of soils classified with ``USC``.

        :param str clf:
            Soil classification based on Unified Soil Classification
            System

        :raises KeyError:
            When ``clf`` is not a valid key
        """
        return cls.soil_descriptions[clf]
