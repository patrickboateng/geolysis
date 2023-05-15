r"""This module provides the implementations for `USCS` and `AASHTO`
classification.

This module contains the following functions:

- `curvature_coefficient` $\rightarrow$ Returns the coefficient of curvature of the soil.
- `uniformity_coefficient` $\rightarrow$ Returns the coefficient of uniformity of the soil.
- `grading` $\rightarrow$ Returns the grading of the soil. (W or P)
- `A_line` $\rightarrow$ Returns the A line.
- `group_index` $\rightarrow$ Returns the group index used to further evaluate the soil.
- `uscs` $\rightarrow$ Returns the classification of the soil according to `USCS` standard.
- `aashto` $\rightarrow$ Returns the classification of the soil according to `AASHTO` standard.

"""

import math
from typing import Optional

from geolab import ERROR_TOLERANCE, exceptions

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
        raise exceptions.PSDValueError(
            f"fines + sand + gravels = 100% not {total_aggregate}"
        )


def _check_pi(liquid_limit, plastic_limit, plasticity_index):
    pi = liquid_limit - plastic_limit
    if not math.isclose(pi, plasticity_index, rel_tol=ERROR_TOLERANCE):
        raise exceptions.PIValueError(
            f"PI should be equal to {pi} not {plasticity_index}"
        )


def _dual_symbol(liquid_limit, plasticity_index, psd, soil_type) -> str:
    curvature_coeff = curvature_coefficient(**psd)
    uniformity_coeff = uniformity_coefficient(psd["d10"], psd["d60"])
    grad = grading(curvature_coeff, uniformity_coeff, soil_type)
    type_of_fines = CLAY if plasticity_index > A_line(liquid_limit) else SILT

    return f"{soil_type}{grad}-{soil_type}{type_of_fines}"


def _classify(liquid_limit, plasticity_index, fines, psd, soil_type: str) -> str:
    if fines > 12:
        Aline = A_line(liquid_limit)
        if math.isclose(plasticity_index, Aline):
            return f"{soil_type}{SILT}-{soil_type}{CLAY}"
        if plasticity_index > Aline:
            return f"{soil_type}{CLAY}"
        return f"{soil_type}{SILT}"

    if 5 <= fines <= 12:
        if psd is not None:
            return _dual_symbol(liquid_limit, plasticity_index, psd, soil_type)
        return (
            f"{soil_type}{WELL_GRADED}-{soil_type}{SILT},"
            f"{soil_type}{POORLY_GRADED}-{soil_type}{SILT},"
            f"{soil_type}{WELL_GRADED}-{soil_type}{CLAY},"
            f"{soil_type}{POORLY_GRADED}-{soil_type}{CLAY}"
        )

    # Obtain Cc and Cu
    if psd is not None:
        curvature_coeff = curvature_coefficient(**psd)
        uniformity_coeff = uniformity_coefficient(psd["d10"], psd["d60"])
        grad = grading(curvature_coeff, uniformity_coeff, soil_type)
        return f"{soil_type}{grad}" if soil_type == GRAVEL else f"{soil_type}{grad}"
    return f"{soil_type}{WELL_GRADED} or {soil_type}{POORLY_GRADED}"


def curvature_coefficient(d10: float, d30: float, d60: float) -> float:
    r"""Calculates the coefficient of curvature of the soil.

    $$\dfrac{d_{30}^2}{d_{60} \times d_{10}}$$

    Args:
        d10: diameter at which 10% of the soil by weight is finer. Defaults to 0.
        d30: diameter at which 30% of the soil by weight is finer. Defaults to 0.
        d60: diameter at which 60% of the soil by weight is finer. Defaults to 0.

    Returns:
        The coefficient of curvature of the soil.
    """
    return (d30**2) / (d60 * d10)


def uniformity_coefficient(d10: float, d60: float) -> float:
    r"""Calculates the coefficient of uniformity of the soil.

    $$\dfrac{d_{60}}{d_{10}}$$

    Args:
        d10: diameter at which 10% of the soil by weight is finer. Defaults to 0.
        d60: diameter at which 60% of the soil by weight is finer. Defaults to 0.

    Returns:
        The coefficient of uniformity of the soil sample.
    """
    return d60 / d10


def grading(
    curvature_coeff: float, uniformity_coeff: float, soil_type: Optional[str] = GRAVEL
) -> str:
    """Determines the grading of the soil.

    Args:
        curvature_coeff: Coefficient of curvature.
        uniformity_coeff: Coefficient of uniformity.
        soil_type: Type of soil. (`G` or `S`). `G` for Gravel and `S` for Sand. Defaults to `G`.

    Returns:
        The grading of the soil. (W or P)

    Raises:
        exceptions.SoilTypeError: Raised when invalid soil type is specified.
    """
    if soil_type not in {GRAVEL, SAND}:
        raise exceptions.SoilTypeError(
            f"Soil type should be {GRAVEL} or {SAND} not {soil_type}"
        )

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
    r"""Calculates the `A-line`.

    $$0.73 \left(LL - 20 \right)$$

    Args:
        liquid_limit: Water content beyond which soils flows under their own weight. (%)

    Returns:
        The `A-line` of the soil.
    """
    return 0.73 * (liquid_limit - 20)


def group_index(fines: float, liquid_limit: float, plasticity_index: float) -> float:
    """The `Group Index (GI)` is used to further evaluate soils with a group
    (subgroups).

    $$GI = (F_{200} - 35)[0.2 + 0.005(LL - 40)] + 0.01(F_{200} - 15)(PI - 10)$$

    Args:
        fines: Percentage of fines in the soil sample. (%)
        liquid_limit: Water content beyond which soils flows under their own weight. (%)
        plasticity_index: Range of water content over which soil remains in plastic
                          condition `PI = LL - PL` (%)

    Returns:
        The group index of the soil sample.
    """

    gi = (fines - 35) * (0.2 + 0.005 * (liquid_limit - 40)) + 0.01 * (fines - 15) * (
        plasticity_index - 10
    )

    return 0.0 if gi <= 0 else gi


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
    """Unified Soil Classification System (`USCS`).

    The `Unified Soil Classification System`, initially developed by Casagrande in 1948
    and later modified in 1952, is widely utilized in engineering projects involving soils.
    It is the most popular system for soil classification and is similar to Casagrande's
    Classification System. The system relies on Particle Size Distribution and Atterberg Limits
    for classification. Soils are categorized into three main groups: coarse-grained, fine-grained,
    and highly organic soils. Additionally, the system has been adopted by the American Society for
    Testing and Materials (`ASTM`).

    Args:
        liquid_limit: Water content beyond which soils flows under their own weight. (%)
        plastic_limit: Water content at which plastic deformation can be initiated. (%)
        plasticity_index: Range of water content over which soil remains in plastic condition
                          `PI = LL - PL`. (%)
        fines: Percentage of fines in soil sample. (%)
        sand:  Percentage of sand in soil sample. (%)
        gravels: Percentage of gravels in soil sample. (%)
        psd: Particle Size Distribution of the soil sample.
        color: Indicates if soil has color or not.
        odor: Indicates if soil has odor or not.

    Returns:
        The unified classification of the soil.

    Raises:
        exceptions.PSDValueError: Raised when soil aggregates does not approximately sum to 100%.
        exceptions.PIValueError: Raised when `PI` is not equal to `LL - PL`.
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

        return f"{SILT}{LOW_PLASTICITY}-{CLAY}{LOW_PLASTICITY}"

    # High LL
    if plasticity_index > A_line(liquid_limit):
        return f"{CLAY}{HIGH_PLASTICITY}"

    return (
        f"{ORGANIC}{HIGH_PLASTICITY}" if (color or odor) else f"{SILT}{HIGH_PLASTICITY}"
    )


def aashto(
    liquid_limit: float, plastic_limit: float, plasticity_index: float, fines: float
) -> str:
    """American Association of State Highway and Transportation Officials (`AASHTO`)
       classification system.

    The AASHTO Classification system categorizes soils for highways based on
    Particle Size Distribution and plasticity characteristics. It classifies
    both coarse-grained and fine-grained soils into eight main groups (A1 to A7)
    with subgroups, along with a separate category (A8) for organic soils

    Args:
        liquid_limit: Water content beyond which soils flows under their own weight. (%)
        plastic_limit: Water content at which plastic deformation can be initiated. (%)
        plasticity_index: Range of water content over which soil remains in plastic
                          condition `PI = LL - PL`. (%)
        fines: Percentage of fines in soil sample. (%)

    Returns:
        The `aashto` classification of the soil.

    Raises:
        exceptions.PIValueError: Raised when PI != LL - PL.
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
