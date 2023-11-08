"""This module provides the implementations for ``USCS`` and ``AASHTO``
classification.
"""

from dataclasses import KW_ONLY, dataclass

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

    :param liquid_limit: Water content beyond which soils flows
                         under their own weight (%). It can also be
                         defined as the minimum moisture content at
                         which a soil flows upon application of a
                         very small shear force. (%)
    :type liquid_limit: float
    :param plastic_limit: Water content at which plastic deformation
                          can be initiated. It is also the minimum
                          water content at which soil can be rolled
                          into a thread 3mm thick (molded without
                          breaking)
    :type plastic_limit: float
    :param nmc: Moisture contents of the soil in natural condition.
                (Natural Moisture Content)
    :type nmc: float, optional
    """

    def __init__(
        self,
        liquid_limit: float,
        plastic_limit: float,
        nmc: float = 0,
    ):
        self.liquid_limit = liquid_limit
        self.plastic_limit = plastic_limit
        self.nmc = nmc

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
        """Return the type of fine soil, either CLAY or SILT"""
        return CLAY if self.above_A_line() else SILT

    def above_A_line(self) -> bool:
        """Checks if the soil sample is above A-Line."""
        return self.plasticity_index > self.A_line

    def limit_plot_in_hatched_zone(self) -> bool:
        """Checks if soil sample plot in the hatched zone."""
        return isclose(
            self.plasticity_index,
            self.A_line,
            rel_tol=ERROR_TOLERANCE,
        )

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

    @property
    def liquidity_index(self) -> float:
        r"""Return the liquidity index of the soil.

        Liquidity index of a soil indicates the nearness of its
        water content to its liquid limit. When the soil is at the
        plastic limit its liquidity index is zero. Negative values
        of the liquidity index indicate that the soil is in a hard
        (desiccated) state. It is also known as ``Water-Plasticity
        ratio``.

        .. math::

            l_i = \dfrac{w - PL}{PI} \cdot 100

        - I_i: Liquidity Index
        - w: Moisture contents of the soil in natural condition.
             (Natural Moisture Content)
        - PL: Plastic Limit
        - PI: Plasticity Index
        """
        return ((self.nmc - self.plastic_limit) / self.plasticity_index) * 100

    @property
    def consistency_index(self) -> float:
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

            I_c = \dfrac{LL - w}{Plasticity Index} \cdot 100

        - I_c: Consistency Index
        - LL: Liquid Limit
        - w: Moisture contents of the soil in natural condition.
             (Natural Moisture Content)
        - PI: Plasticity Index
        """
        return ((self.liquid_limit - self.nmc) / self.plasticity_index) * 100


@dataclass
class PSD:
    """A dataclass for Particle Size Distribution.

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
    :raises exceptions.PSDValueError: Raised when soil aggregates does not
                                      approximately sum to 100%
    """

    fines: float
    sand: float
    gravel: float
    d10: float = 0
    d30: float = 0
    d60: float = 0

    def __post_init__(self):
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

    def grade(self, coarse_soil: str) -> str:
        """Return the grade of the soil sample."""
        # Gravel
        if coarse_soil == GRAVEL:
            return self._coarse_grade()

        # Sand
        return self._sand_grade()

    @property
    @round_(precision=2)
    def curvature_coefficient(self) -> float:
        r"""Return the coefficient of curvature of the soil.

        .. math::

            C_c = \dfrac{d_{30}^2}{d_{60} \cdot d_{10}}
        """
        return (self.d30**2) / (self.d60 * self.d10)

    @property
    @round_(precision=2)
    def uniformity_coefficient(self) -> float:
        r"""Return the coefficient of uniformity of the soil.

        .. math::

            C_u = \dfrac{d_{60}}{d_{10}}
        """
        return self.d60 / self.d10


@dataclass
class AASHTO:
    """American Association of State Highway and Transportation Officials
    (``AASHTO``) classification system.

    The AASHTO Classification system categorizes soils for highways based on
    Particle Size Distribution and plasticity characteristics. It classifies
    both coarse-grained and fine-grained soils into eight main groups (A1 to
    A7) with subgroups, along with a separate category (A8) for organic soils.

    :param liquid_limit: Water content beyond which soils flows under their own
        weight (%)
    :type liquid_limit: float
    :param plasticity_index: Range of water content over which soil remains in
        plastic condition (%)
    :param fines: Percentage of fines in soil sample (%)
    :type fines: float
    """

    liquid_limit: float
    plasticity_index: float
    fines: float

    @round_(precision=0)
    def group_index(self) -> float:
        """Return the ``Group Index GI`` of the soil sample.

        The ``(GI)`` is used to further evaluate soils with a group (subgroups).

        .. math::

            GI = (F_{200} - 35)[0.2 + 0.005(LL - 40)] + 0.01(F_{200} - 15)(PI - 10)
        """
        x_1 = 0 if (x_0 := self.fines - 35) < 0 else min(x_0, 40)
        x_2 = 0 if (x_0 := self.liquid_limit - 40) < 0 else min(x_0, 20)
        x_3 = 0 if (x_0 := self.fines - 15) < 0 else min(x_0, 40)
        x_4 = 0 if (x_0 := self.plasticity_index - 10) < 0 else min(x_0, 20)
        grp_idx = x_1 * (0.2 + 0.005 * x_2) + 0.01 * x_3 * x_4

        return 0.0 if grp_idx <= 0 else grp_idx

    @property
    def _grp_idx(self) -> str:
        grp_idx = self.group_index()
        grp_idx = f"{grp_idx:.0f}"

        return grp_idx

    def _classify_coarse_soil(self) -> str:
        if self.liquid_limit <= 40:
            if self.plasticity_index <= 10:
                clf = f"A-2-4({self._grp_idx})"
            else:
                clf = f"A-2-6({self._grp_idx})"

        else:
            if self.plasticity_index <= 10:
                clf = f"A-2-5({self._grp_idx})"
            else:
                clf = f"A-2-7({self._grp_idx})"

        return clf

    def _classify_fine_soil(self) -> str:
        if self.liquid_limit <= 40:
            if self.plasticity_index <= 10:
                clf = f"A-4({self._grp_idx})"
            else:
                clf = f"A-6({self._grp_idx})"

        else:
            if self.plasticity_index <= 10:
                clf = f"A-5({self._grp_idx})"
            else:
                if self.plasticity_index <= (self.liquid_limit - 30):
                    clf = f"A-7-5({self._grp_idx})"
                else:
                    clf = f"A-7-6({self._grp_idx})"

        return clf

    def classify(self) -> str:
        """Return the AASHTO classification of the soil sample."""

        # Coarse A1-A3
        if self.fines <= 35:
            return self._classify_coarse_soil()

        # Silts A4-A7
        return self._classify_fine_soil()


@dataclass
class USCS:
    """Unified Soil Classification System (``USCS``).

    The Unified Soil Classification System, initially developed by Casagrande
    in 1948 and later modified in 1952, is widely utilized in engineering
    projects involving soils. It is the most popular system for soil classification
    and is similar to Casagrande's Classification System. The system relies on
    Particle Size Distribution and Atterberg Limits for classification. Soils are
    categorized into three main groups: coarse-grained, fine-grained, and highly
    organic soils. Additionally, the system has been adopted by the American Society
    for Testing and Materials (``ASTM``).
    """

    atterberg_limits: AtterbergLimits
    psd: PSD

    _: KW_ONLY
    organic: bool = False

    def _dual_soil_classifier(self, coarse_soil: str) -> str:
        soil_grd = self.psd.grade(coarse_soil)
        fine_soil = self.atterberg_limits.type_of_fines

        return f"{coarse_soil}{soil_grd}-{coarse_soil}{fine_soil}"

    def _classify_coarse_soil(self, coarse_soil: str) -> str:
        if self.psd.fines > 12:
            if self.atterberg_limits.limit_plot_in_hatched_zone():
                clf = f"{coarse_soil}{SILT}-{coarse_soil}{CLAY}"

            elif self.atterberg_limits.above_A_line():
                clf = f"{coarse_soil}{CLAY}"

            else:
                clf = f"{coarse_soil}{SILT}"

        elif 5 <= self.psd.fines <= 12:
            # Requires dual symbol based on graduation and plasticity chart
            if self.psd.has_particle_sizes():
                clf = self._dual_soil_classifier(coarse_soil)

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
                _soil_grd = self.psd.grade(coarse_soil)
                clf = f"{coarse_soil}{_soil_grd}"

            else:
                clf = f"{coarse_soil}{WELL_GRADED} or {coarse_soil}{POORLY_GRADED}"

        return clf

    def _classify_fine_soil(self) -> str:
        clf: str

        if self.atterberg_limits.liquid_limit < 50:
            # Low LL
            if (self.atterberg_limits.above_A_line()) and (
                self.atterberg_limits.plasticity_index > 7
            ):
                clf = f"{CLAY}{LOW_PLASTICITY}"

            elif (not self.atterberg_limits.above_A_line()) or (
                self.atterberg_limits.plasticity_index < 4
            ):
                if self.organic:
                    clf = f"{ORGANIC}{LOW_PLASTICITY}"

                else:
                    clf = f"{SILT}{LOW_PLASTICITY}"

            # Limits plot in hatched area on plasticity chart
            else:
                clf = f"{SILT}{LOW_PLASTICITY}-{CLAY}{LOW_PLASTICITY}"

        # High LL
        else:
            # Above A-Line
            if self.atterberg_limits.above_A_line():
                clf = f"{CLAY}{HIGH_PLASTICITY}"

            # Below A-Line
            else:
                if self.organic:
                    clf = f"{ORGANIC}{HIGH_PLASTICITY}"
                else:
                    clf = f"{SILT}{HIGH_PLASTICITY}"

        return clf

    def classify(self) -> str:
        """Return the ``USCS`` classification of the soil."""
        # Coarse grained, Run Sieve Analysis
        if self.psd.fines < 50:
            if self.psd.gravel > self.psd.sand:
                # Gravel
                return self._classify_coarse_soil(coarse_soil=GRAVEL)

            # Sand
            return self._classify_coarse_soil(coarse_soil=SAND)

        # Fine grained, Run Atterberg
        return self._classify_fine_soil()
