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
from typing import Optional

from geolab import DECIMAL_PLACES, ERROR_TOLERANCE, exceptions

GRAVEL = "G"
WELL_GRADED = "W"
POORLY_GRADED = "P"
SAND = "S"
CLAY = "C"
SILT = "M"
ORGANIC = "O"
LOW_PLASTICITY = "L"
HIGH_PLASTICITY = "H"


def _check_psd(fines, sand, gravels):
    total_aggregate = fines + sand + gravels
    if not math.isclose(total_aggregate, 100, rel_tol=ERROR_TOLERANCE):
        msg = f"fines + sand + gravels = 100% not {total_aggregate}"
        raise exceptions.PSDValueError(msg)


def _check_pi(liquid_limit, plastic_limit, plasticity_index):
    pi = liquid_limit - plastic_limit
    if not math.isclose(pi, plasticity_index, rel_tol=ERROR_TOLERANCE):
        msg = f"PI should be equal to {pi} not {plasticity_index}"
        raise exceptions.PIValueError(msg)


class PSDCoefficient:
    """Provides methods for calculating the ``coefficient of curvature`` and
    ``coefficient of uniformity``.
    """

    def __init__(self, d10: float, d30: float, d60: float) -> None:
        """
        :param d10: diameter at which 10% of the soil by weight is finer
        :type d10: float
        :param d30: diameter at which 30% of the soil by weight is finer
        :type d30: float
        :param d60: diameter at which 60% of the soil by weight is finer
        :type d60: float
        """
        self.d10 = d10
        self.d30 = d30
        self.d60 = d60

    @property
    def curvature_coefficient(self) -> float:
        r"""Calculates the coefficient of curvature of the soil.

        .. math::

            C_c = \dfrac{d_{30}^2}{d_{60} \times d_{10}}

        :return: The coefficient of curvature of the soil
        :rtype: float
        """
        _cc = (self.d30**2) / (self.d60 * self.d10)
        return round(_cc, DECIMAL_PLACES)

    @property
    def uniformity_coefficient(self) -> float:
        r"""Calculates the coefficient of uniformity of the soil.

        .. math::

            C_u = \dfrac{d_{60}}{d_{10}}

        :return: The coefficient of uniformity of the soil
        :rtype: float
        """
        _cu = self.d60 / self.d10
        return round(_cu, DECIMAL_PLACES)


def _dual_symbol(
    liquid_limit: float,
    plasticity_index: float,
    psd_coeff: PSDCoefficient,
    soil_type: str,
) -> str:
    grad = grading(
        psd_coeff.curvature_coefficient,
        psd_coeff.uniformity_coefficient,
        soil_type,
    )
    type_of_fines = CLAY if plasticity_index > A_line(liquid_limit) else SILT

    return f"{soil_type}{grad}-{soil_type}{type_of_fines}"


def _classify(
    liquid_limit, plasticity_index, fines, psd, soil_type: str
) -> str:
    if fines > 12:
        Aline = A_line(liquid_limit)
        # Limit plot in hatched zone on plasticity chart
        if math.isclose(plasticity_index, Aline):
            return f"{soil_type}{SILT}-{soil_type}{CLAY}"

        if plasticity_index > Aline:
            return f"{soil_type}{CLAY}"

        # Below A-Line
        return f"{soil_type}{SILT}"

    if 5 <= fines <= 12:
        # Requires dual symbol based on graduation and plasticity chart
        if psd is not None:
            return _dual_symbol(
                liquid_limit,
                plasticity_index,
                PSDCoefficient(**psd),
                soil_type,
            )
        return (
            f"{soil_type}{WELL_GRADED}-{soil_type}{SILT},"
            f"{soil_type}{POORLY_GRADED}-{soil_type}{SILT},"
            f"{soil_type}{WELL_GRADED}-{soil_type}{CLAY},"
            f"{soil_type}{POORLY_GRADED}-{soil_type}{CLAY}"
        )

    # Less than 5% pass No. 200 sieve
    # Obtain Cc and Cu from grain size graph
    if psd is not None:
        psd_coeff = PSDCoefficient(**psd)
        grad = grading(
            psd_coeff.curvature_coefficient,
            psd_coeff.uniformity_coefficient,
            soil_type,
        )
        return (
            f"{soil_type}{grad}"
            if soil_type == GRAVEL
            else f"{soil_type}{grad}"
        )
    return f"{soil_type}{WELL_GRADED} or {soil_type}{POORLY_GRADED}"


def grading(
    curvature_coeff: float, uniformity_coeff: float, soil_type: str
) -> str:
    """Determines the grading of the soil.

    :param curvature_coeff: Coefficient of curvature
    :type curvature_coeff: float
    :param uniformity_coeff: Coefficient of uniformity
    :type uniformity_coeff: float
    :param soil_type: Type of soil. ``G`` for Gravel and ``S`` for Sand
    :type soil_type: str
    :raises exceptions.SoilTypeError: Raised when invalid soil type is specified
    :return: The grading of the soil (W or P)
    :rtype: str
    """
    if soil_type == GRAVEL:
        return (
            WELL_GRADED
            if (1 < curvature_coeff < 3) and (uniformity_coeff >= 4)
            else POORLY_GRADED
        )
    return (
        WELL_GRADED
        if (1 < curvature_coeff < 3) and (uniformity_coeff >= 6)
        else POORLY_GRADED
    )


def A_line(liquid_limit: float) -> float:
    r"""Calculates the ``A-line``.

    .. math::

        0.73 \left(LL - 20 \right)

    :param liquid_limit: Water content beyond which soils flows under their own weight (%)
    :type liquid_limit: float
    :return: The ``A-line`` of the soil
    :rtype: float
    """
    a_line = 0.73 * (liquid_limit - 20)
    return round(a_line, DECIMAL_PLACES)


def group_index(
    fines: float, liquid_limit: float, plasticity_index: float
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
    _gi = (fines - 35) * (0.2 + 0.005 * (liquid_limit - 40)) + 0.01 * (
        fines - 15
    ) * (plasticity_index - 10)
    return 0.0 if _gi <= 0 else round(_gi, DECIMAL_PLACES)


def uscs(
    liquid_limit: float,
    plastic_limit: float,
    plasticity_index: float,
    fines: float,
    sand: float,
    gravels: float,
    *,
    psd: Optional[dict] = None,
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

    :param liquid_limit: Water content beyond which soils flows under their own weight (%)
    :type liquid_limit: float
    :param plastic_limit: Water content at which plastic deformation can be initiated (%)
    :type plastic_limit: float
    :param plasticity_index: Range of water content over which soil remains in plastic condition (%)
    :type plasticity_index: float
    :param fines: Percentage of fines in soil sample (%)
    :type fines: float
    :param sand:  Percentage of sand in soil sample (%)
    :type sand: float
    :param gravels: Percentage of gravels in soil sample (%)
    :type gravels: float
    :param psd: Particle Size Distribution of the soil sample, defaults to None
    :type psd: dict, optional
    :param color: Indicates if soil has color or not, defaults to False
    :type color: bool, optional
    :param odor: Indicates if soil has odor or not, defaults to False
    :type odor: bool, optional
    :raises exceptions.PSDValueError: Raised when soil aggregates does not approximately sum to 100%
    :raises exceptions.PIValueError: Raised when ``PI`` is not equal to ``LL - PL``
    :return: The unified classification of the soil
    :rtype: str
    """
    _check_pi(liquid_limit, plastic_limit, plasticity_index)
    _check_psd(fines, sand, gravels)

    if fines < 50:
        # Coarse grained, Run Sieve Analysis
        soil_info = (liquid_limit, plasticity_index, fines, psd)
        if gravels > sand:
            # Gravel
            return _classify(*soil_info, soil_type=GRAVEL)
        # Sand
        return _classify(*soil_info, soil_type=SAND)

    # Fine grained, Run Atterberg
    Aline = A_line(liquid_limit)
    if liquid_limit < 50:
        # Low LL
        if (plasticity_index > Aline) and (plasticity_index > 7):
            return f"{CLAY}{LOW_PLASTICITY}"

        if (plasticity_index < Aline) or (plasticity_index < 4):
            return (
                f"{ORGANIC}{LOW_PLASTICITY}"
                if (color or odor)
                else f"{SILT}{LOW_PLASTICITY}"
            )

        # Limits plot in hatched area on plasticity chart
        return f"{SILT}{LOW_PLASTICITY}-{CLAY}{LOW_PLASTICITY}"

    # High LL
    if plasticity_index > Aline:
        return f"{CLAY}{HIGH_PLASTICITY}"

    # Below A-Line
    return (
        f"{ORGANIC}{HIGH_PLASTICITY}"
        if (color or odor)
        else f"{SILT}{HIGH_PLASTICITY}"
    )


def aashto(
    liquid_limit: float,
    plastic_limit: float,
    plasticity_index: float,
    fines: float,
) -> str:
    """American Association of State Highway and Transportation Officials (``AASHTO``)
    classification system.

    The AASHTO Classification system categorizes soils for highways based on
    Particle Size Distribution and plasticity characteristics. It classifies
    both coarse-grained and fine-grained soils into eight main groups (A1 to A7)
    with subgroups, along with a separate category (A8) for organic soils.

    :param liquid_limit: Water content beyond which soils flows under their own weight (%)
    :type liquid_limit: float
    :param plastic_limit: Water content at which plastic deformation can be initiated (%)
    :type plastic_limit: float
    :param plasticity_index: Range of water content over which soil remains in plastic condition (%)
    :type plasticity_index: float
    :param fines: Percentage of fines in soil sample (%)
    :type fines: float
    :raises exceptions.PIValueError: Raised when ``PI`` is not equal to ``LL - PL``
    :return: The ``aashto`` classification of the soil
    :rtype: str
    """
    _check_pi(liquid_limit, plastic_limit, plasticity_index)
    gi = group_index(fines, liquid_limit, plasticity_index)

    if fines <= 35:
        if liquid_limit <= 40:
            return f"A-2-4({gi})" if plasticity_index <= 10 else f"A-2-6({gi})"
        return f"A-2-5({gi})" if plasticity_index <= 10 else f"A-2-7({gi})"

    # Silts A4-A7
    if liquid_limit <= 40:
        return f"A-4({gi:.0f})" if plasticity_index <= 10 else f"A-6({gi:.0f})"

    if plasticity_index <= 10:
        return f"A-5({gi:.0f})"

    return (
        f"A-7-5({gi:.0f})"
        if plasticity_index <= (liquid_limit - 30)
        else f"A-7-6({gi:.0f})"
    )
