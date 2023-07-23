r"""This module provides the implementations for ``USCS`` and ``AASHTO`` classification.

Public Functions
----------------

- ``curvature_coefficient``: Returns the coefficient of curvature of the soil
- ``uniformity_coefficient``: Returns the coefficient of uniformity of the soil
- `grading`: Returns the grading of the soil (W or P)
- `A_line`: Returns the A line
- `group_index`: Returns the group index used to further evaluate the soil
- `uscs`: Returns the classification of the soil according to ``USCS`` standard
- `aashto`: Returns the classification of the soil according to ``AASHTO`` standard

"""
import math
from dataclasses import dataclass, field, asdict
from typing import Optional

from geolab import ERROR_TOLERANCE, exceptions
from geolab.utils import round_

GRAVEL = "G"
WELL_GRADED = "W"
POORLY_GRADED = "P"
SAND = "S"
CLAY = "C"
SILT = "M"
ORGANIC = "O"
LOW_PLASTICITY = "L"
HIGH_PLASTICITY = "H"


def _check_size_distribution(fines, sand, gravels):
    if not math.isclose(
        total_aggregate := fines + sand + gravels, 100, rel_tol=ERROR_TOLERANCE
    ):
        msg = f"fines + sand + gravels = 100% not {total_aggregate}"
        raise exceptions.PSDValueError(msg)


def _check_plasticity_idx(liquid_limit, plastic_limit, plasticity_index):
    if not math.isclose(
        pi := liquid_limit - plastic_limit,
        plasticity_index,
        rel_tol=ERROR_TOLERANCE,
    ):
        msg = f"PI should be equal to {pi} not {plasticity_index}"
        raise exceptions.PIValueError(msg)


@dataclass(slots=True)
class AtterbergLimits:
    liquid_limit: float
    plastic_limit: float
    plasticity_index: float


@dataclass(slots=True)
class ParticleSizes:
    d10: float
    d30: float
    d60: float

    def __bool__(self):
        return all((self.d10, self.d30, self.d60))


@dataclass(slots=True)
class ParticleSizeDistribution:
    fines: float
    sands: float
    gravels: float
    particle_sizes: Optional[ParticleSizes] = field(default=None)

    def has_particle_sizes(self):
        return bool(self.particle_sizes)


@dataclass(slots=True)
class PSDCoefficient:
    """Provides methods for calculating the ``coefficient of curvature`` and
    ``coefficient of uniformity``.

    :param d10: diameter at which 10% of the soil by weight is finer
    :type d10: float
    :param d30: diameter at which 30% of the soil by weight is finer
    :type d30: float
    :param d60: diameter at which 60% of the soil by weight is finer
    :type d60: float
    """

    d10: float
    d30: float
    d60: float

    @property
    @round_(precision=2)
    def curvature_coefficient(self) -> float:
        r"""Calculates the coefficient of curvature of the soil.

        .. math::

            C_c = \dfrac{d_{30}^2}{d_{60} \times d_{10}}

        :return: The coefficient of curvature of the soil
        :rtype: float
        """
        return (self.d30**2) / (self.d60 * self.d10)

    @property
    @round_(precision=2)
    def uniformity_coefficient(self) -> float:
        r"""Calculates the coefficient of uniformity of the soil.

        .. math::

            C_u = \dfrac{d_{60}}{d_{10}}

        :return: The coefficient of uniformity of the soil
        :rtype: float
        """
        return self.d60 / self.d10


def _dual_soil_symbol(
    liquid_limit,
    plasticity_index,
    psd_coeff,
    gravel_or_sand,
) -> str:
    soil_grade = soil_grading(
        psd_coeff.curvature_coefficient,
        psd_coeff.uniformity_coefficient,
        gravel_or_sand,
    )
    clay_or_silt = CLAY if plasticity_index > A_line(liquid_limit) else SILT

    return f"{gravel_or_sand}{soil_grade}-{gravel_or_sand}{clay_or_silt}"


def _classify_soil(
    liquid_limit: float,
    plasticity_index: float,
    psd: ParticleSizeDistribution,
    gravel_or_sand: str,
) -> str:
    if psd.fines > 12:
        Aline = A_line(liquid_limit)
        # Limit plot in hatched zone on plasticity chart
        if math.isclose(plasticity_index, Aline):
            return f"{gravel_or_sand}{SILT}-{gravel_or_sand}{CLAY}"

        if plasticity_index > Aline:
            return f"{gravel_or_sand}{CLAY}"

        # Below A-Line
        return f"{gravel_or_sand}{SILT}"

    if 5 <= psd.fines <= 12:
        # Requires dual symbol based on graduation and plasticity chart
        if psd.has_particle_sizes():
            return _dual_soil_symbol(
                liquid_limit,
                plasticity_index,
                PSDCoefficient(**asdict(psd.particle_sizes)),
                gravel_or_sand,
            )
        return (
            f"{gravel_or_sand}{WELL_GRADED}-{gravel_or_sand}{SILT},"
            f"{gravel_or_sand}{POORLY_GRADED}-{gravel_or_sand}{SILT},"
            f"{gravel_or_sand}{WELL_GRADED}-{gravel_or_sand}{CLAY},"
            f"{gravel_or_sand}{POORLY_GRADED}-{gravel_or_sand}{CLAY}"
        )

    # Less than 5% pass No. 200 sieve
    # Obtain Cc and Cu from grain size graph
    if psd.has_particle_sizes():
        psd_coeff = PSDCoefficient(**asdict(psd.particle_sizes))
        soil_grade = soil_grading(
            psd_coeff.curvature_coefficient,
            psd_coeff.uniformity_coefficient,
            gravel_or_sand,
        )
        return (
            f"{gravel_or_sand}{soil_grade}"
            if gravel_or_sand == GRAVEL
            else f"{gravel_or_sand}{soil_grade}"
        )
    return f"{gravel_or_sand}{WELL_GRADED} or {gravel_or_sand}{POORLY_GRADED}"


def soil_grading(
    curvature_coeff: float, uniformity_coeff: float, gravel_or_sand: str
) -> str:
    """Determines the grading of the soil.

    :param curvature_coeff: Coefficient of curvature
    :type curvature_coeff: float
    :param uniformity_coeff: Coefficient of uniformity
    :type uniformity_coeff: float
    :param gravel_or_sand: Type of soil. ``G`` for Gravel and ``S`` for Sand
    :type gravel_or_sand: str
    :raises exceptions.SoilTypeError: Raised when invalid soil type is specified
    :return: The grading of the soil (W -> WELL GRADED or P -> POORLY GRADED)
    :rtype: str
    """
    if gravel_or_sand == GRAVEL:
        return (
            WELL_GRADED
            if (1 < curvature_coeff < 3) and (uniformity_coeff >= 4)
            else POORLY_GRADED
        )

    # Sand
    return (
        WELL_GRADED
        if (1 < curvature_coeff < 3) and (uniformity_coeff >= 6)
        else POORLY_GRADED
    )


@round_(precision=2)
def A_line(liquid_limit: float) -> float:
    r"""Calculates the ``A-line``.

    .. math::

        0.73 \left(LL - 20 \right)

    :param liquid_limit: Water content beyond which soils flows under their own weight (%)
    :type liquid_limit: float
    :return: The ``A-line`` of the soil
    :rtype: float
    """
    return 0.73 * (liquid_limit - 20)


@round_(precision=2)
def group_index(
    fines: float,
    liquid_limit: float,
    plasticity_index: float,
) -> float:
    """The ``Group Index (GI)`` is used to further evaluate soils with a group (subgroups).

    .. math::

        GI = (F_{200} - 35)[0.2 + 0.005(LL - 40)] + 0.01(F_{200} - 15)(PI - 10)

    :param fines: Percentage of fines in the soil sample (%)
    :type fines: float
    :param liquid_limit: Water content beyond which soils flows under their own weight (%)
    :type liquid_limit: float
    :param plasticity_index: Range of water content over which soil remains in plastic condition (%)
    :type plasticity_index: float
    :return: The group index of the soil sample
    :rtype: float
    """
    grp_idx = (fines - 35) * (0.2 + 0.005 * (liquid_limit - 40)) + 0.01 * (
        fines - 15
    ) * (plasticity_index - 10)
    return 0.0 if grp_idx <= 0 else grp_idx


def unified_soil_classification(
    atterberg_limits: AtterbergLimits,
    psd: ParticleSizeDistribution,
    *,
    color: Optional[bool] = False,
    odor: Optional[bool] = False,
) -> str:
    """Unified Soil Classification System (``USCS``).

    The Unified Soil Classification System, initially developed by Casagrande in 1948
    and later modified in 1952, is widely utilized in engineering projects involving soils.
    It is the most popular system for soil classification and is similar to Casagrande's
    Classification System. The system relies on Particle Size Distribution and Atterberg Limits
    for classification. Soils are categorized into three main groups: coarse-grained, fine-grained,
    and highly organic soils. Additionally, the system has been adopted by the American Society for
    Testing and Materials (``ASTM``).

    :param atterberg_limits:
    :type atterberg_limits:
    :param psd:
    :type psd:
    :param color: Indicates if soil has color or not, defaults to False
    :type color: bool, optional
    :param odor: Indicates if soil has odor or not, defaults to False
    :type odor: bool, optional
    :raises exceptions.PSDValueError: Raised when soil aggregates does not approximately sum to 100%
    :raises exceptions.PIValueError: Raised when ``PI`` is not equal to ``LL - PL``
    :return: The unified classification of the soil
    :rtype: str
    """
    _check_plasticity_idx(
        atterberg_limits.liquid_limit,
        atterberg_limits.plastic_limit,
        atterberg_limits.plasticity_index,
    )
    _check_size_distribution(psd.fines, psd.sands, psd.gravels)

    if psd.fines < 50:
        # Coarse grained, Run Sieve Analysis
        soil_properties = (
            atterberg_limits.liquid_limit,
            atterberg_limits.plasticity_index,
            psd,
        )
        if psd.gravels > psd.sands:
            # Gravel
            return _classify_soil(*soil_properties, gravel_or_sand=GRAVEL)
        # Sand
        return _classify_soil(*soil_properties, gravel_or_sand=SAND)

    # Fine grained, Run Atterberg
    Aline = A_line(atterberg_limits.liquid_limit)
    if atterberg_limits.liquid_limit < 50:
        # Low LL
        if (atterberg_limits.plasticity_index > Aline) and (
            atterberg_limits.plasticity_index > 7
        ):
            return f"{CLAY}{LOW_PLASTICITY}"

        if (atterberg_limits.plasticity_index < Aline) or (
            atterberg_limits.plasticity_index < 4
        ):
            return (
                f"{ORGANIC}{LOW_PLASTICITY}"
                if (color or odor)
                else f"{SILT}{LOW_PLASTICITY}"
            )

        # Limits plot in hatched area on plasticity chart
        return f"{SILT}{LOW_PLASTICITY}-{CLAY}{LOW_PLASTICITY}"

    # High LL
    if atterberg_limits.plasticity_index > Aline:
        return f"{CLAY}{HIGH_PLASTICITY}"

    # Below A-Line
    return (
        f"{ORGANIC}{HIGH_PLASTICITY}"
        if (color or odor)
        else f"{SILT}{HIGH_PLASTICITY}"
    )


def aashto_soil_classification(
    atterberg_limits: AtterbergLimits,
    fines: float,
) -> str:
    """American Association of State Highway and Transportation Officials (``AASHTO``)
    classification system.

    The AASHTO Classification system categorizes soils for highways based on
    Particle Size Distribution and plasticity characteristics. It classifies
    both coarse-grained and fine-grained soils into eight main groups (A1 to A7)
    with subgroups, along with a separate category (A8) for organic soils.

    :param atterberg_limits:
    :type atterberg_limits:
    :param fines: Percentage of fines in soil sample (%)
    :type fines: float
    :raises exceptions.PIValueError: Raised when ``PI`` is not equal to ``LL - PL``
    :return: The ``aashto`` classification of the soil
    :rtype: str
    """
    _check_plasticity_idx(
        atterberg_limits.liquid_limit,
        atterberg_limits.plastic_limit,
        atterberg_limits.plasticity_index,
    )
    grp_idx = f"{group_index(fines, atterberg_limits.liquid_limit, atterberg_limits.plasticity_index):.0f}"

    if fines <= 35:
        if atterberg_limits.liquid_limit <= 40:
            return (
                f"A-2-4({grp_idx})"
                if atterberg_limits.plasticity_index <= 10
                else f"A-2-6({grp_idx})"
            )
        return (
            f"A-2-5({grp_idx})"
            if atterberg_limits.plasticity_index <= 10
            else f"A-2-7({grp_idx})"
        )

    # Silts A4-A7
    if atterberg_limits.liquid_limit <= 40:
        return (
            f"A-4({grp_idx})"
            if atterberg_limits.plasticity_index <= 10
            else f"A-6({grp_idx})"
        )

    if atterberg_limits.plasticity_index <= 10:
        return f"A-5({grp_idx})"

    return (
        f"A-7-5({grp_idx})"
        if atterberg_limits.plasticity_index
        <= (atterberg_limits.liquid_limit - 30)
        else f"A-7-6({grp_idx})"
    )
