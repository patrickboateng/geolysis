r"""This module provides the implementations for ``USCS`` and ``AASHTO`` classification.

"""

import math
from typing import Optional

from geolab import ERROR_TOLERANCE, exceptions
from geolab.utils import round_

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
    if not math.isclose(total_aggregate, 100, rel_tol=ERROR_TOLERANCE):
        msg = f"fines + sand + gravels = 100% not {total_aggregate}"
        raise exceptions.PSDValueError(msg)


def _check_plasticity_idx(
    liquid_limit: float, plastic_limit: float, plasticity_index: float
):
    plasticity_idx = liquid_limit - plastic_limit
    if not math.isclose(
        plasticity_idx, plasticity_index, rel_tol=ERROR_TOLERANCE
    ):
        msg = f"PI should be equal to {plasticity_idx} not {plasticity_index}"
        raise exceptions.PIValueError(msg)


class OrganicSoil:
    pass


class InOrganicSoil:
    pass


class AtterbergLimits:
    # TODO
    # Add more description to docstring
    """Atterberg Limits.

    :param liquid_limit: Water content beyond which soils flows under their own weight (%)
    :type liquid_limit: float
    :param plastic_limit: Water content at which plastic deformation can be initiated (%)
    :type plastic_limit: float
    :param plasticity_index: Range of water content over which soil remains in plastic condition (%)
    :type plasticity_index: float
    """

    def __init__(
        self,
        liquid_limit: float,
        plastic_limit: float,
        plasticity_index: float,
    ):
        _check_plasticity_idx(liquid_limit, plastic_limit, plasticity_index)

        self.liquid_limit = liquid_limit
        self.plastic_limit = plastic_limit
        self.plasticity_index = plasticity_index

    @property
    @round_(precision=2)
    def A_line(self) -> float:
        r"""Calculates the ``A-line``.

        .. math::

            0.73 \left(LL - 20 \right)

        """
        return 0.73 * (self.liquid_limit - 20)

    def above_A_line(self) -> bool:
        return self.plasticity_index > self.A_line

    def limit_plot_in_hatched_zone(self) -> bool:
        return math.isclose(self.plasticity_index, self.A_line)


class PSD:
    # TODO
    # Add more description to the docstring
    """Particle Size Distribution.

    :param fines: Percentage of fines in soil sample (%)
    :type fines: float
    :param sand: Percentage of sand in soil sample (%)
    :type sand: float
    :param gravel: Percentage of gravel in soil sample (%)
    :type gravel: float
    :param d10: Diameter at which 30% of the soil by weight is finer
    :type d10: float
    :param d30: Diameter at which 30% of the soil by weight is finer
    :type d30: float
    :param d60: Diameter at which 60% of the soil by weight is finer
    :type d60: float
    """

    def __init__(
        self,
        fines: float,
        sand: float,
        gravel: float,
        d10: Optional[float] = None,
        d30: Optional[float] = None,
        d60: Optional[float] = None,
    ) -> None:
        _check_size_distribution(fines, sand, gravel)

        self.fines = fines
        self.sand = sand
        self.gravel = gravel
        self.d10 = d10
        self.d30 = d30
        self.d60 = d60

    def has_particle_sizes(self) -> bool:
        return all((self.d10, self.d30, self.d60))

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


def _dual_soil_classifier(
    atterberg_limits: AtterbergLimits,
    psd: PSD,
    coarse_soil: str,
) -> str:
    _soil_grd = soil_grade(
        psd.curvature_coefficient, psd.uniformity_coefficient, coarse_soil
    )
    fine_soil = CLAY if atterberg_limits.above_A_line() else SILT

    return f"{coarse_soil}{_soil_grd}-{coarse_soil}{fine_soil}"


def _classify_fine_soil(
    atterberg_limits: AtterbergLimits, soil_type: InOrganicSoil | OrganicSoil
) -> str:
    if atterberg_limits.liquid_limit < 50:
        # Low LL
        if (atterberg_limits.above_A_line()) and (
            atterberg_limits.plasticity_index > 7
        ):
            return f"{CLAY}{LOW_PLASTICITY}"

        if (not atterberg_limits.above_A_line()) or (
            atterberg_limits.plasticity_index < 4
        ):
            return (
                f"{ORGANIC}{LOW_PLASTICITY}"
                if isinstance(soil_type, OrganicSoil)
                else f"{SILT}{LOW_PLASTICITY}"
            )

        # Limits plot in hatched area on plasticity chart
        return f"{SILT}{LOW_PLASTICITY}-{CLAY}{LOW_PLASTICITY}"

    # High LL
    if atterberg_limits.above_A_line():
        return f"{CLAY}{HIGH_PLASTICITY}"

    # Below A-Line
    return (
        f"{ORGANIC}{HIGH_PLASTICITY}"
        if isinstance(soil_type, OrganicSoil)
        else f"{SILT}{HIGH_PLASTICITY}"
    )


def _classify_coarse_soil(
    atterberg_limits: AtterbergLimits,
    psd: PSD,
    coarse_soil: str,
) -> str:
    if psd.fines > 12:
        if atterberg_limits.limit_plot_in_hatched_zone():
            return f"{coarse_soil}{SILT}-{coarse_soil}{CLAY}"

        return (
            f"{coarse_soil}{CLAY}"
            if atterberg_limits.above_A_line()
            else f"{coarse_soil}{SILT}"
        )

    if 5 <= psd.fines <= 12:
        # Requires dual symbol based on graduation and plasticity chart
        if psd.has_particle_sizes():
            return _dual_soil_classifier(atterberg_limits, psd, coarse_soil)

        return (
            f"{coarse_soil}{WELL_GRADED}-{coarse_soil}{SILT},"
            f"{coarse_soil}{POORLY_GRADED}-{coarse_soil}{SILT},"
            f"{coarse_soil}{WELL_GRADED}-{coarse_soil}{CLAY},"
            f"{coarse_soil}{POORLY_GRADED}-{coarse_soil}{CLAY}"
        )

    # Less than 5% pass No. 200 sieve
    # Obtain Cc and Cu from grain size graph
    if psd.has_particle_sizes():
        _soil_grd = soil_grade(
            psd.curvature_coefficient,
            psd.uniformity_coefficient,
            coarse_soil,
        )
        return f"{coarse_soil}{_soil_grd}"

    return f"{coarse_soil}{WELL_GRADED} or {coarse_soil}{POORLY_GRADED}"


def soil_grade(
    curvature_coefficient: float,
    uniformity_coefficient: float,
    coarse_soil: str,
) -> str:
    # TODO
    # Modify docstrings
    """Determines the grading of the soil.

    :param coarse_soil: Type of soil. ``G`` for Gravel and ``S`` for Sand
    :type coarse_soil: str
    :return: The grading of the soil (W -> WELL GRADED or P -> POORLY GRADED)
    :rtype: str
    """

    # Gravel
    if coarse_soil == GRAVEL:
        return (
            WELL_GRADED
            if (1 < curvature_coefficient < 3)
            and (uniformity_coefficient >= 4)
            else POORLY_GRADED
        )

    # Sand
    return (
        WELL_GRADED
        if (1 < curvature_coefficient < 3) and (uniformity_coefficient >= 6)
        else POORLY_GRADED
    )


@round_(precision=0)
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
    expr_1 = 0 if (expr := fines - 35) < 0 else min(expr, 40)
    expr_2 = 0 if (expr := liquid_limit - 40) < 0 else min(expr, 20)
    expr_3 = 0 if (expr := fines - 15) < 0 else min(expr, 40)
    expr_4 = 0 if (expr := plasticity_index - 10) < 0 else min(expr, 20)

    grp_idx = (expr_1) * (0.2 + 0.005 * (expr_2)) + 0.01 * (expr_3) * (expr_4)
    return 0.0 if grp_idx <= 0 else grp_idx


class AASHTO:
    """American Association of State Highway and Transportation Officials (``AASHTO``)
    classification system.

    The AASHTO Classification system categorizes soils for highways based on
    Particle Size Distribution and plasticity characteristics. It classifies
    both coarse-grained and fine-grained soils into eight main groups (A1 to A7)
    with subgroups, along with a separate category (A8) for organic soils.

    :param atterberg_limits: Atterberg Limits
    :type atterberg_limits: AtterbergLimits
    :param fines: Percentage of fines in soil sample (%)
    :type fines: float
    :raises exceptions.PIValueError: Raised when ``PI`` is not equal to ``LL - PL``
    :return: The ``AASHTO`` classification of the soil
    :rtype: str
    """

    def __init__(
        self,
        liquid_limit: float,
        plasticity_index: float,
        fines: float,
    ) -> None:
        self.liquid_limit = liquid_limit
        self.plasticity_index = plasticity_index
        self.fines = fines

    def classify(self) -> str:
        grp_idx = group_index(
            self.fines, self.liquid_limit, self.plasticity_index
        )
        grp_idx = f"{grp_idx:.0f}"  # convert grp_idx to a whole number

        if self.fines <= 35:
            if self.liquid_limit <= 40:
                return (
                    f"A-2-4({grp_idx})"
                    if self.plasticity_index <= 10
                    else f"A-2-6({grp_idx})"
                )
            return (
                f"A-2-5({grp_idx})"
                if self.plasticity_index <= 10
                else f"A-2-7({grp_idx})"
            )

        # Silts A4-A7
        if self.liquid_limit <= 40:
            return (
                f"A-4({grp_idx})"
                if self.plasticity_index <= 10
                else f"A-6({grp_idx})"
            )

        if self.plasticity_index <= 10:
            return f"A-5({grp_idx})"

        return (
            f"A-7-5({grp_idx})"
            if self.plasticity_index <= (self.liquid_limit - 30)
            else f"A-7-6({grp_idx})"
        )


class USCS:
    """Unified Soil Classification System (``USCS``).

    The Unified Soil Classification System, initially developed by Casagrande in 1948
    and later modified in 1952, is widely utilized in engineering projects involving soils.
    It is the most popular system for soil classification and is similar to Casagrande's
    Classification System. The system relies on Particle Size Distribution and Atterberg Limits
    for classification. Soils are categorized into three main groups: coarse-grained, fine-grained,
    and highly organic soils. Additionally, the system has been adopted by the American Society for
    Testing and Materials (``ASTM``).

    :param atterberg_limits: Atterberg Limits
    :type atterberg_limits: AtterbergLimits
    :param particle_size_distribution: Particle Size Distribution
    :type particle_size_distribution: ParticleSizeDistribution
    :param soil_type: Indicates the type of soil
    :type soil_type: InOrganicSoil or OrganicSoil, optional
    :raises exceptions.PSDValueError: Raised when soil aggregates does not approximately sum to 100%
    :raises exceptions.PIValueError: Raised when ``PI`` is not equal to ``LL - PL``
    :return: The unified classification of the soil
    :rtype: str
    """

    def __init__(
        self,
        liquid_limit: float,
        plastic_limit: float,
        plasticity_index: float,
        fines: float,
        sand: float,
        gravel: float,
        *,
        d10: Optional[float] = None,
        d30: Optional[float] = None,
        d60: Optional[float] = None,
        soil_type: Optional[InOrganicSoil | OrganicSoil] = InOrganicSoil,
    ) -> None:
        self.atterberg_limits = AtterbergLimits(
            liquid_limit,
            plastic_limit,
            plasticity_index,
        )
        self.psd = PSD(fines, sand, gravel, d10, d30, d60)
        self.soil_type = soil_type

    def classify(self) -> str:
        if self.psd.fines < 50:
            # Coarse grained, Run Sieve Analysis
            if self.psd.gravel > self.psd.sand:
                # Gravel
                return _classify_coarse_soil(
                    self.atterberg_limits, self.psd, coarse_soil=GRAVEL
                )

            # Sand
            return _classify_coarse_soil(
                self.atterberg_limits, self.psd, coarse_soil=SAND
            )

        # Fine grained, Run Atterberg
        return _classify_fine_soil(self.atterberg_limits, self.soil_type)
