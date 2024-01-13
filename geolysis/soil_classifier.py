"""This module provides the implementations for ``USCS`` and ``AASHTO``
classification.
"""

from math import trunc
from types import MappingProxyType
from typing import NamedTuple

from .constants import (
    CLAY,
    ERROR_TOL,
    GRAVEL,
    HIGH_PLASTICITY,
    LOW_PLASTICITY,
    ORGANIC,
    POORLY_GRADED,
    SAND,
    SILT,
    WELL_GRADED,
)
from .utils import isclose, round_


class PSDValueError(ValueError):
    """Exception raised when soil aggregates does not approximately sum up to
    100%.
    """


class SoilClassificationError(ValueError):
    pass


def _chk_psd(fines, sand, gravel):
    total_agg = fines + sand + gravel
    if not isclose(total_agg, 100.0, rel_tol=ERROR_TOL):
        msg = f"fines + sand + gravels = 100% not {total_agg}"
        raise PSDValueError(msg)


class AtterbergLimits:
    """Atterberg Limits.

    :param float liquid_limit: Water content beyond which soils flows under
        their own weight. It can also be defined as the minimum moisture
        content at which a soil flows upon application of a very small shear
        force.
    :param float plastic_limit: Water content at which plastic deformation can
        be initiated. It is also the minimum water content at which soil can be
        rolled into a thread 3mm thick (molded without breaking)
    """

    def __init__(self, liquid_limit: float, plastic_limit: float):
        self.liquid_limit = liquid_limit
        self.plastic_limit = plastic_limit

    @property
    def plasticity_index(self) -> float:
        """Return the plasticity index of the soil."""
        return self.liquid_limit - self.plastic_limit

    @property
    @round_(ndigits=2)
    def A_line(self) -> float:
        """Return the ``A-line`` which is used to determine if a soil is clay
        or silt.
        """
        return 0.73 * (self.liquid_limit - 20)

    @property
    def type_of_fines(self) -> str:
        """Return the type of fine soil, either :data:`~geolysis.CLAY`
        or :data:`~geolysis.SILT`."""
        return CLAY if self.above_A_LINE() else SILT

    def above_A_LINE(self) -> bool:
        """Checks if the soil sample is above A-Line."""
        return self.plasticity_index > self.A_line

    def limit_plot_in_hatched_zone(self) -> bool:
        """Checks if soil sample plot in the hatched zone."""
        return 4 <= self.plasticity_index <= 7 and 10 < self.liquid_limit < 30

    @round_(ndigits=2)
    def liquidity_index(self, nmc: float) -> float:
        r"""Return the liquidity index of the soil.

        :param float nmc: Moisture contents of the soil in natural condition.
            (Natural Moisture Content)
        """
        return ((nmc - self.plastic_limit) / self.plasticity_index) * 100

    @round_(ndigits=2)
    def consistency_index(self, nmc: float) -> float:
        r"""Return the consistency index of the soil.

        :param float nmc: Moisture contents of the soil in natural condition.
            (Natural Moisture Content)
        """
        return ((self.liquid_limit - nmc) / self.plasticity_index) * 100


class SizeDistribution(NamedTuple):
    """Size distribution of the soil sample.

    :kwparam float d_10: Diameter at which 10% of the soil by weight is finer.
    :kwparam float d_30: Diameter at which 30% of the soil by weight is finer.
    :kwparam float d_60: Diameter at which 60% of the soil by weight is finer.
    """

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

    def _grade(self, coarse_soil: str) -> str:
        """Grade of soil sample. Soil grade can either be ``WELL_GRADED`` or
        ``POORLY_GRADED``.

        :param str coarse_soil: Coarse fraction of the soil sample. Valid arguments
            are ``GRAVEL`` or ``SAND``.
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


class ParticleSizeDistribution:
    """Particle Size Distribution.

    :param float fines: Percentage of fines in soil sample i.e. the percentage of
        soil sample passing through No. 200 sieve (0.075mm)
    :param float sand: Percentage of sand in soil sample (%)
    :param float gravel: Percentage of gravel in soil sample (%)
    :param SizeDistribution size_dist: Size distribution in the soil sample. It is
        a namedtuple with values for ``d_10``, ``d_30``, and ``d_60`` respectively.
        Defaults to SizeDistribution(0, 0, 0)

    :raises PSDValueError: Raised when soil aggregates does not approximately sum up
        to 100%.
    """

    def __init__(
        self,
        fines: float,
        sand: float,
        gravel: float,
        *,
        size_dist=SizeDistribution(0, 0, 0),
    ):
        self.fines = fines
        self.sand = sand
        self.gravel = gravel
        self.size_dist = size_dist

        _chk_psd(self.fines, self.sand, self.gravel)

    @property
    def type_of_coarse(self) -> str:
        """Return the type of coarse material i.e. either :data:`geolysis.GRAVEL` or
        :data:`geolysis.SAND`.
        """
        if self.gravel > self.sand:
            return GRAVEL

        return SAND

    @property
    def coeff_of_curvature(self) -> float:
        r"""Return the coefficient of curvature of the soil."""
        return self.size_dist.coeff_of_curvature

    @property
    def coeff_of_uniformity(self) -> float:
        r"""Return the coefficient of uniformity of the soil."""
        return self.size_dist.coeff_of_uniformity

    def has_particle_sizes(self) -> bool:
        """Checks if soil sample has particle sizes."""
        return all(self.size_dist)

    def grade(self) -> str:
        """Return the grade of the soil sample."""
        return self.size_dist._grade(coarse_soil=self.type_of_coarse)


class AASHTOClassification:
    """American Association of State Highway and Transportation Officials
    (``AASHTO``) classification system.

    :param float liquid_limit: Water content beyond which soils flows under their own weight.
    :param float plasticity_index: Range of water content over which soil remains in plastic
        condition.
    :param float fines: Percentage of fines in soil sample i.e. the percentage of soil
        sample passing through No. 200 sieve (0.075mm).
    :kwparam bool add_group_idx: Used to indicate whether the group index should be added to
        the classification or not. Defaults to True.

    .. note::

        You can use :class:`AASHTOClassification` and :class:`AASHTO <AASHTOClassification>` interchangeably.
    """

    def __init__(
        self,
        liquid_limit: float,
        plasticity_index: float,
        fines: float,
        *,
        add_group_idx: bool = True,
    ):
        self.liquid_limit = liquid_limit
        self.plasticity_index = plasticity_index
        self.fines = fines
        self.add_group_idx = add_group_idx

    def group_index(self) -> float:
        """Return the Group Index (GI) of the soil sample."""
        x_1 = 1 if (x_0 := self.fines - 35) < 0 else min(x_0, 40)
        x_2 = 1 if (x_0 := self.liquid_limit - 40) < 0 else min(x_0, 20)
        x_3 = 1 if (x_0 := self.fines - 15) < 0 else min(x_0, 40)
        x_4 = 1 if (x_0 := self.plasticity_index - 10) < 0 else min(x_0, 20)

        grp_idx = round(x_1 * (0.2 + 0.005 * x_2) + 0.01 * x_3 * x_4, 0)

        return 0 if grp_idx <= 0 else trunc(grp_idx)

    def classify(self) -> str:
        """Return the AASHTO classification of the soil sample."""

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


class UnifiedSoilClassification:
    """Unified Soil Classification System (USCS).

    :param AtterbergLimits atterberg_limits: Water content at which soil changes from one
        state to other.
    :param ParticleSizeDistribution psd: Distribution of soil particles in the soil sample.
    :kwparam bool organic: Indicates whether the soil is organic or not.

    .. note::

        You can use :class:`UnifiedSoilClassification` and
        :class:`USCS <UnifiedSoilClassification>` interchangeably.
    """

    soil_descriptions = MappingProxyType(
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

    def classify(self) -> str:
        """Return the Unified Soil Classification of the soil sample."""
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
                clf = f"{coarse_soil}{self.psd.grade()}"

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

    @classmethod
    def soil_description(cls, clf: str) -> str:
        """Return the typical names of soils classified with ``USCS``.

        :param str clf: Soil classification based on USCS.
        :raises SoilClassificationError: Exception raised when a wrong
            classification is provided.
        """
        clf = clf.strip()

        try:
            return cls.soil_descriptions[clf]
        except KeyError as exc:
            msg = (
                f"{clf} is not a valid USCS classification. "
                "Use geolysis.USCS.soil_descriptions.keys() "
                "to obtain all available USCS  classifications."
            )
            raise SoilClassificationError(msg) from exc


# *****************ALIASES*******************

AL = AtterbergLimits
PSD = ParticleSizeDistribution
AASHTO = AASHTOClassification
USCS = UnifiedSoilClassification
