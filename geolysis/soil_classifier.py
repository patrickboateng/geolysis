from abc import abstractmethod

# from dataclasses import dataclass
from typing import NamedTuple, Protocol

from .constants import ERROR_TOL, GDict
from .constants import UnitRegistry as ureg
from .utils import ceil, isclose, round_

__all__ = [
    "GRAVEL",
    "SAND",
    "SILT",
    "CLAY",
    "ORGANIC",
    "WELL_GRADED",
    "POORLY_GRADED",
    "LOW_PLASTICITY",
    "HIGH_PLASTICITY",
    "AtterbergLimits",
    "PSD",
    "AASHTO",
    "USCS",
]


class PSDAggSumError(ValueError):
    pass


class SoilClassifier(Protocol):

    @property
    @abstractmethod
    def soil_class(self) -> str: ...

    @property
    @abstractmethod
    def soil_desc(self) -> str: ...


#: USCS symbol for gravel.
GRAVEL: str = "G"

#: USCS symbol for sand.
SAND: str = "S"

#: USCS symbol for silt.
SILT: str = "M"

#: USCS symbol for clay.
CLAY: str = "C"

#: USCS symbol for organic material.
ORGANIC: str = "O"

#: USCS symbol for well-graded material.
WELL_GRADED: str = "W"

#: USCS symbol for poorly-graded material.
POORLY_GRADED: str = "P"

#: USCS symbol for low soil plasticity.
LOW_PLASTICITY: str = "L"

#: USCS symbol for high soil plasticity.
HIGH_PLASTICITY: str = "H"


class AtterbergLimits:
    """Water contents at which soil changes from one state to the other.

    In 1911, a Swedish agriculture engineer ``Atterberg`` mentioned that a
    fined-grained soil can exist in four states, namely, liquid, plastic,
    semi-solid or solid state.

    The main use of Atterberg Limits is in the classification of soils.

    Parameters
    ----------
    liquid_limit : float
        Water content beyond which soils flows under their own weight.
        It can also be defined as the minimum moisture content at which
        a soil flows upon application of a very small shear force.
    plastic_limit : float
        Water content at which plastic deformation can be initiated. It
        is also the minimum water content at which soil can be rolled into
        a thread 3mm thick (molded without breaking)

    Attributes
    ----------
    liquid_limit : float
    plastic_limit : float
    plasticity_index : float
    A_line : float
    type_of_fines : str

    Methods
    -------
    above_A_LINE
    limit_plot_in_hatched_zone
    liquidity_index
    consistency_index
    """

    def __init__(self, liquid_limit: float, plastic_limit: float):
        self._liquid_limit = liquid_limit
        self._plastic_limit = plastic_limit

    @property
    def liquid_limit(self) -> float:
        """Water content beyond which soils flows under their own weight."""
        return self._liquid_limit

    @liquid_limit.setter
    def liquid_limit(self, __val: float):
        self._liquid_limit = __val

    @property
    def plastic_limit(self) -> float:
        """Water content at which plastic deformation can be initiated."""
        return self._plastic_limit

    @plastic_limit.setter
    def plastic_limit(self, __val: float):
        self._plastic_limit = __val

    @property
    def plasticity_index(self) -> float:
        """Return the plasticity index of the soil.

        Plasticity index is the range of water content over which the soil
        remains in the plastic state. It is also the numerical difference
        between the liquid limit and plastic limit of the soil.

        Notes
        -----
        .. math:: PI = LL - PL
        """
        return self.liquid_limit - self.plastic_limit

    @property
    @round_(ndigits=2)
    def A_line(self) -> float:
        """Return the ``A-line`` which is used to determine if a soil is clayey
        or silty.

        Notes
        -----
        .. math:: 0.73(LL - 20)
        """
        return 0.73 * (self.liquid_limit - 20)

    @property
    def type_of_fines(self) -> str:
        """Return the type of fine soil, either :data:`CLAY` or :data:`SILT`."""
        return CLAY if self.above_A_LINE() else SILT

    def above_A_LINE(self) -> bool:
        """Checks if the soil sample is above A-Line."""
        return self.plasticity_index > self.A_line

    def limit_plot_in_hatched_zone(self) -> bool:
        """Checks if soil sample plot in the hatched zone on the atterberg
        chart.
        """
        return 4 <= self.plasticity_index <= 7 and 10 < self.liquid_limit < 30

    @round_(ndigits=2)
    def liquidity_index(self, nmc: float) -> float:
        """Return the liquidity index of the soil.

        Liquidity index of a soil indicates the nearness of its ``natural water
        content`` to its ``liquid limit``. When the soil is at the plastic limit
        its liquidity index is zero. Negative values of the liquidity index
        indicate that the soil is in a hard (desiccated) state. It is also known
        as Water-Plasticity ratio.

        Parameters
        ----------
        nmc : float
            Moisture contents of the soil in natural condition. (Natural Moisture
            Content)
        """
        return ((nmc - self.plastic_limit) / self.plasticity_index) * 100

    @round_(ndigits=2)
    def consistency_index(self, nmc: float) -> float:
        """Return the consistency index of the soil.

        Consistency index indicates the consistency (firmness) of soil. It shows
        the nearness of the ``natural water content`` of the soil to its
        ``plastic limit``. When the soil is at the liquid limit, the consistency
        index is zero. The soil at consistency index of zero will be extremely
        soft and has negligible shear strength. A soil at a water content equal
        to the plastic limit has consistency index of 100% indicating that the
        soil is relatively firm. A consistency index of greater than 100% shows
        the soil is relatively strong (semi-solid state). A negative value indicate
        the soil is in the liquid state. It is also known as Relative Consistency.

        Parameters
        ----------
        nmc : float
            Moisture contents of the soil in natural condition. (Natural Moisture
            Content)
        """
        return ((self.liquid_limit - nmc) / self.plasticity_index) * 100.0


class _SizeDistribution(NamedTuple):
    """Features obtained from the Particle Size Distribution graph."""

    d_10: float
    d_30: float
    d_60: float

    @property
    @round_(ndigits=2)
    def coeff_of_curvature(self) -> float:
        """Coefficient of curvature of soil sample."""
        return (self.d_30**2) / (self.d_60 * self.d_10)

    @property
    @round_(ndigits=2)
    def coeff_of_uniformity(self) -> float:
        """Coefficient of uniformity of soil sample."""
        return self.d_60 / self.d_10

    def grade(self, coarse_soil: str) -> str:
        """Grade of soil sample. Soil grade can either be ``WELL_GRADED`` or
        ``POORLY_GRADED``.

        Parameters
        ----------
        coarse_soil : str
            Coarse fraction of the soil sample. Valid arguments are :data:`GRAVEL`
            or :data:`SAND`.
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


class PSD:
    """Quantitative proportions by mass of various sizes of particles present
    in a soil.

    Particle Size Distribution is a method of separation of soils into
    different fractions using a stack of sieves to measure the size of the
    particles in a sample and graphing the results to illustrate the
    distribution of the particle sizes.

    Parameters
    ----------
    fines : float
        Percentage of fines in soil sample i.e. the percentage of soil sample
        passing through No. 200 sieve (0.075mm)
    sand : float
        Percentage of sand in soil sample. (%)
    gravel : float
        Percentage of gravel in soil sample. (%)
    d_10 : float, unit=millimetre
        Diameter at which 10% of the soil by weight is finer.
    d_30 : float, unit=millimetre
        Diameter at which 30% of the soil by weight is finer.
    d_60 : float, unit=millimetre
        Diameter at which 60% of the soil by weight is finer.

    Attributes
    ----------
    fines : float
    sand : float
    gravel : float
    d_10 : float
    d_30 : float
    d_60 : float
    UNITS : GDict
        Unit registry for attributes and values returned from
        functions.

    Raises
    ------
    PSDAggSumError
        Raised when soil aggregates does not approximately sum up to 100%.
    """

    UNITS = GDict(d_10=ureg.mm, d_30=ureg.mm, d_60=ureg.mm)

    def __init__(
        self,
        fines: float,
        sand: float,
        gravel: float,
        d_10: float = 0,
        d_30: float = 0,
        d_60: float = 0,
    ):
        self.fines = fines
        self.sand = sand
        self.gravel = gravel
        self.size_dist = _SizeDistribution(d_10, d_30, d_60)

        total_agg = self.fines + self.sand + self.gravel

        if not isclose(total_agg, 100.0, rel_tol=ERROR_TOL):
            err_msg = f"fines + sand + gravels = 100% not {total_agg}"
            raise PSDAggSumError(err_msg)

    def _has_particle_sizes(self) -> bool:
        """Checks if soil sample has particle sizes."""
        return all(self.size_dist)

    @property
    def d_10(self) -> float:
        return self.size_dist.d_10

    @property
    def d_30(self) -> float:
        return self.size_dist.d_30

    @property
    def d_60(self) -> float:
        return self.size_dist.d_60

    @property
    def type_of_coarse(self) -> str:
        """Return the type of coarse material i.e. either :data:`GRAVEL` or
        :data:`SAND`.
        """
        return GRAVEL if self.gravel > self.sand else SAND

    @property
    def coeff_of_curvature(self) -> float:
        """Return the coefficient of curvature of the soil."""
        return self.size_dist.coeff_of_curvature

    @property
    def coeff_of_uniformity(self) -> float:
        """Return the coefficient of uniformity of the soil."""
        return self.size_dist.coeff_of_uniformity

    def grade(self) -> str:
        r"""Return the grade of the soil sample, either :data:`WELL_GRADED`
        or :data:`POORLY_GRADED`.

        Conditions for a well-graded soil:

        - :math:`1 \lt C_c \lt 3` and :math:`C_u \ge 4` (for gravels)
        - :math:`1 \lt C_c \lt 3` and :math:`C_u \ge 6` (for sands)
        """
        return self.size_dist.grade(coarse_soil=self.type_of_coarse)


class AASHTO:
    r"""American Association of State Highway and Transportation Officials
    (AASHTO) classification system.

    The AASHTO classification system is useful for classifying soils for highways.
    It categorizes soils for highways based on particle size analysis and
    plasticity characteristics. It classifies both coarse-grained and fine-grained
    soils into eight main groups (A1-A7) with subgroups, along with a separate
    category (A8) for organic soils.

    - ``A1 ~ A3`` (Granular Materials) :math:`\le` 35% pass No. 200 sieve
    - ``A4 ~ A7`` (Silt-clay Materials) :math:`\ge` 36% pass No. 200 sieve

    The Group Index ``(GI)`` is used to further evaluate soils within a group.
    When calculating ``GI`` from the equation below, if any term in the parenthesis
    becomes negative, it is drop and not given a negative value. The maximum values
    of :math:`(F_{200} - 35)` and :math:`(F_{200} - 15)` are taken as 40 and
    :math:`(LL - 40)` and :math:`(PI - 10)` as 20.

    If the computed value for ``GI`` is negative, it is reported as zero.

    In general, the rating for the pavement subgrade is inversely proportional to
    the ``GI`` (lower the ``GI``, better the material). For e.g., a ``GI`` of zero
    indicates a good subgrade, whereas a group index of 20 or greater shows a very
    poor subgrade.

    Parameters
    ----------
    liquid_limit : float
        Water content beyond which soils flows under their own weight.
    plasticity_index : float
        Range of water content over which soil remains in plastic condition.
    fines : float
        Percentage of fines in soil sample i.e. the percentage of soil sample passing
        through No. 200 sieve (0.075mm).
    add_group_idx : bool, default=True
        Used to indicate whether the group index should be added to the classification
        or not. Defaults to True.

    Attributes
    ----------
    liquid_limit : float
    plasticity_index : float
    fines : float
    add_group_idx : bool
    soil_desc : str
    AASHTO_SOIL_DESC : GDict
        Descriptions for all AASHTO soil classes.

    Notes
    -----
    The ``GI`` must be mentioned even when it is zero, to indicate that the soil has been
    classified as per AASHTO system.

    .. math:: GI = (F_{200} - 35)[0.2 + 0.005(LL - 40)] + 0.01(F_{200} - 15)(PI - 10)
    """

    #: Descriptions for various AASHTO soil classes.
    AASHTO_SOIL_DESC = GDict(
        {
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
    )

    def __init__(
        self,
        liquid_limit: float,
        plasticity_index: float,
        fines: float,
        add_group_idx=True,
    ):
        self.liquid_limit = liquid_limit
        self.plasticity_index = plasticity_index
        self.fines = fines
        self.add_group_idx = add_group_idx

    def _classify(self) -> str:
        # Silts A4-A7
        if self.fines > 35:
            return self._fine_soil_classifier()

        # Coarse A1-A3
        return self._coarse_soil_classifier()

    def _coarse_soil_classifier(self) -> str:
        # A-3, Fine sand
        if self.fines <= 10 and isclose(
            self.plasticity_index, 0, rel_tol=ERROR_TOL
        ):
            clf = "A-3"

        # A-1-a -> A-1-b, Stone fragments, gravel, and sand
        elif self.fines <= 15 and self.plasticity_index <= 6:
            clf = "A-1-a"

        elif self.fines <= 25 and self.plasticity_index <= 6:
            clf = "A-1-b"

        # A-2-4 -> A-2-7, Silty or clayey gravel and sand
        elif self.liquid_limit <= 40:
            if self.plasticity_index <= 10:
                clf = "A-2-4"
            else:
                clf = "A-2-6"

        else:
            if self.plasticity_index <= 10:
                clf = "A-2-5"
            else:
                clf = "A-2-7"

        return f"{clf}({self.group_index()})" if self.add_group_idx else clf

    def _fine_soil_classifier(self) -> str:
        # A-4 -> A-5, Silty Soils
        # A-6 -> A-7, Clayey Soils
        if self.liquid_limit <= 40:
            clf = "A-4" if self.plasticity_index <= 10 else "A-6"

        else:
            if self.plasticity_index <= 10:
                clf = "A-5"
            else:
                _x = self.liquid_limit - 30
                clf = "A-7-5" if self.plasticity_index <= _x else "A-7-6"

        return f"{clf}({self.group_index()})" if self.add_group_idx else clf

    @property
    def soil_desc(self) -> str:
        """Return the AASHTO description of the soil."""
        tmp_state = self.add_group_idx
        try:
            self.add_group_idx = False
            return self.AASHTO_SOIL_DESC[self._classify()]
        finally:
            self.add_group_idx = tmp_state

    def group_index(self) -> float:
        """Return the Group Index (GI) of the soil sample."""
        x_1 = 1 if (x_0 := self.fines - 35) < 0 else min(x_0, 40)
        x_2 = 1 if (x_0 := self.liquid_limit - 40) < 0 else min(x_0, 20)
        x_3 = 1 if (x_0 := self.fines - 15) < 0 else min(x_0, 40)
        x_4 = 1 if (x_0 := self.plasticity_index - 10) < 0 else min(x_0, 20)

        grp_idx = round(x_1 * (0.2 + 0.005 * x_2) + 0.01 * x_3 * x_4, 0)

        return 0 if grp_idx <= 0 else ceil(grp_idx)

    def soil_class(self) -> str:
        """Return the AASHTO classification of the soil."""
        return self._classify()


class USCS:
    """Unified Soil Classification System (USCS).

    The Unified Soil Classification System, initially developed by Casagrande in
    1948 and later modified in 1952, is widely utilized in engineering projects
    involving soils. It is the most popular system for soil classification and is
    similar to Casagrande's Classification System. The system relies on particle
    size analysis and atterberg limits for classification.

    In this system, soils are first classified into two categories:

    - Coarse grained soils: If more than 50% of the soils is retained on No. 200
      (0.075 mm) sieve, it is designated as coarse-grained soil.

    - Fine grained soils: If more than 50% of the soil passes through No. 200 sieve,
      it is designated as fine grained soil.

    Highly Organic soils are identified by visual inspection. These soils are termed
    as Peat. (:math:`P_t`)

    Parameters
    ----------
    liquid_limit : float
        Water content beyond which soils flows under their own weight. It can also
        be defined as the minimum moisture content at which a soil flows upon
        application of a very small shear force.
    plastic_limit : float
        Water content at which plastic deformation can be initiated. It is also the
        minimum water content at which soil can be rolled into a thread 3mm thick
        (molded without breaking)
    fines : float
        Percentage of fines in soil sample i.e. The percentage of soil sample passing
        through No. 200 sieve (0.075mm)
    sand : float
        Percentage of sand in soil sample (%)
    gravel : float
        Percentage of gravel in soil sample (%)
    d_10 : float, unit=millimetre
        Diameter at which 10% of the soil by weight is finer.
    d_30 : float, unit=millimetre
        Diameter at which 30% of the soil by weight is finer.
    d_60 : float, unit=millimetre
        Diameter at which 60% of the soil by weight is finer.
    organic : bool, default=False
        Indicates whether soil is organic or not.

    Attributes
    ----------
    atterberg_limits : AtterbergLimits
    psd : PSD
    organic : bool
    soil_desc : str
    USCS_SOIL_DESC : GDict
        Descriptions for all USCS soil classes.
    """

    #: Descriptions for all USCS soil classes.
    USCS_SOIL_DESC = GDict(
        {
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
    )

    def __init__(
        self,
        liquid_limit: float,
        plastic_limit: float,
        fines: float,
        sand: float,
        gravel: float,
        *,
        d_10=0,
        d_30=0,
        d_60=0,
        organic=False,
    ):
        self.atterberg_limits = AtterbergLimits(liquid_limit, plastic_limit)
        self.psd = PSD(fines, sand, gravel, d_10, d_30, d_60)
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
            if self.psd._has_particle_sizes():
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
            if self.psd._has_particle_sizes():
                soil_class = f"{coarse_soil}{self.psd.grade()}"

            else:
                soil_class = f"{coarse_soil}{WELL_GRADED} or {coarse_soil}{POORLY_GRADED}"

        return soil_class

    def _fine_soil_classifier(self) -> str:
        if self.atterberg_limits.liquid_limit < 50:
            # Low LL
            # Above A-line and PI > 7
            if (self.atterberg_limits.above_A_LINE()) and (
                self.atterberg_limits.plasticity_index > 7
            ):
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

    @property
    def soil_desc(self) -> str:
        """Return the USCS description of the soil."""
        return self.USCS_SOIL_DESC[self._classify()]

    def soil_class(self) -> str:
        """Return the USCS Classification of the soil."""
        return self._classify()
