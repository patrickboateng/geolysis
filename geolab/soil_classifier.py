"""This module provides the implementations for `USCS` and `AASHTO`
classification.
"""

import math

from geolab import exceptions

GRAVEL = "G"
WELL_GRADED = "W"
POORLY_GRADED = "P"
SAND = "S"
CLAY = "C"
SILT = "M"
ORGANIC = "O"
LOW_PLASTICITY = "L"
HIGH_PLASTICITY = "H"


def _check_PSD(fines: float, sand: float, gravels: float):
    total_aggregate = fines + sand + gravels
    if not math.isclose(total_aggregate, 100, rel_tol=0.01):
        raise exceptions.PSDValueError("fines + sand + gravels != 100%")


def _check_PI(liquid_limit: float, plastic_limit: float, plasticity_index: float):
    if not math.isclose(liquid_limit - plastic_limit, plasticity_index, rel_tol=0.01):
        raise exceptions.PIValueError("PI != LL - PL")


def Cc(d10: float, d30: float, d60: float) -> float:
    r"""Calculates the coefficient of Curvature of the soil.

    $$\dfrac{d_{30}^2}{d_{60} \times d_{10}}$$

    """
    return (d30**2) / (d60 * d10)


def Cu(d10: float, d60: float) -> float:
    r"""Calculates the coefficient of uniformity of the soil.

    $$\dfrac{d_{60}}{d_{10}}$$

    """
    return d60 / d10


def grading(Cc: float, Cu: float, soil_type: str = GRAVEL) -> str:
    """Determines the grading of the soil.

    Args:
        Cc: Coefficient of curvature.
        Cu: Coefficient of uniformity.
        soil_type: Type of soil. (Gravel or Sand). Defaults to Gravel.

    Returns:
        The grading of the soil. (W or P)

    Raises:
        exceptions.SoilTypeError
    """
    if soil_type not in {GRAVEL, SAND}:
        raise exceptions.SoilTypeError(
            f"Soil type should be {GRAVEL} or {SAND} not {soil_type}"
        )

    if soil_type == GRAVEL:
        return WELL_GRADED if (1 < Cc < 3) and Cu >= 4 else POORLY_GRADED
    return WELL_GRADED if (1 < Cc < 3) and Cu >= 6 else POORLY_GRADED


def A_line(liquid_limit: float) -> float:
    return 0.73 * (liquid_limit - 20)


def _dual_symbol(liquid_limit, plasticity_index, d10, d30, d60, soil_type: str) -> str:
    cc = Cc(d10, d30, d60)
    cu = Cu(d10, d60)
    grad = grading(cc, cu, soil_type)
    type_of_fines = CLAY if plasticity_index > A_line(liquid_limit) else SILT

    return f"{soil_type}{grad}-{soil_type}{type_of_fines}"


def _classify(
    liquid_limit,
    plasticity_index,
    fines,
    d10,
    d30,
    d60,
    soil_type: str,
):
    if fines > 12:
        Aline = A_line(liquid_limit)
        if math.isclose(plasticity_index, Aline):
            return f"{soil_type}{SILT}-{soil_type}{CLAY}"
        elif plasticity_index > Aline:
            return f"{soil_type}{CLAY}"
        else:
            return f"{soil_type}{SILT}"

    elif 5 <= fines <= 12:
        if d10 and d30 and d60:
            return _dual_symbol(
                liquid_limit, plasticity_index, d10, d30, d60, soil_type
            )
        return f"{soil_type}{WELL_GRADED}-{soil_type}{SILT}, {soil_type}{POORLY_GRADED}-{soil_type}{SILT}, {soil_type}{WELL_GRADED}-{soil_type}{CLAY}, {soil_type}{POORLY_GRADED}-{soil_type}{CLAY}"

    else:
        # Obtain Cc and Cu
        if d10 and d30 and d60:
            cc = Cc(d10, d30, d60)
            cu = Cu(d10, d60)
            grad = grading(cc, cu, soil_type)
            return f"{soil_type}{grad}" if soil_type == GRAVEL else f"{soil_type}{grad}"
        return f"{soil_type}{WELL_GRADED} or {soil_type}{POORLY_GRADED}"


def uscs(
    liquid_limit,
    plastic_limit,
    plasticity_index,
    fines,
    sand,
    gravels,
    d10=0,
    d30=0,
    d60=0,
    color=False,
    odor=False,
) -> str:
    """Unified Soil Classification System.

    Args:
        liquid_limit: Water content beyond which soils flows under their own weight. (%)
        plastic_limit: Water content at which plastic deformation can be initiated. (%)
        plasticity_index: Range of water content over which soil remains in plastic condition `PI = LL - PL` (%)
        fines: Percentage of fines in soil sample.
        sand:  Percentage of sand in soil sample.
        gravels: Percentage of gravels in soil sample.
        d10: diameter at which 10% of the soil by weight is finer. Defaults to 0.
        d30: diameter at which 30% of the soil by weight is finer. Defaults to 0.
        d60: diameter at which 60% of the soil by weight is finer. Defaults to 0.
        color: Indicates if soil has color or not. Defaults to False.
        odor: Indicates if soil has odor or not. Defaults to False.

    Raises:
        exceptions.PSDValueError: Raised when soil aggregates does not approximately sum to 100%.
        exceptions.PIValueError: Raised when PI != LL - PL.

    """

    _check_PI(liquid_limit, plastic_limit, plasticity_index)
    _check_PSD(fines, sand, gravels)

    if fines < 50:
        # Coarse grained, Run Sieve Analysis
        data = (liquid_limit, plasticity_index, fines, d10, d30, d60)
        if gravels > sand:
            # Gravel
            soil_type = GRAVEL
            return _classify(*data, soil_type)
        else:
            # Sand
            soil_type = SAND
            return _classify(*data, soil_type)
    else:
        # Fine grained, Run Atterberg
        Aline = A_line(liquid_limit)
        if liquid_limit < 50:
            # Low LL
            if (plasticity_index > Aline) and plasticity_index > 7:
                return f"{CLAY}{LOW_PLASTICITY}"

            elif (plasticity_index < Aline) or plasticity_index < 4:
                return (
                    f"{ORGANIC}{LOW_PLASTICITY}"
                    if (color or odor)
                    else f"{SILT}{LOW_PLASTICITY}"
                )

            else:
                return f"{SILT}{LOW_PLASTICITY}-{CLAY}{LOW_PLASTICITY}"

        else:
            # High LL
            if plasticity_index > A_line(liquid_limit):
                return f"{CLAY}{HIGH_PLASTICITY}"

            else:
                return (
                    f"{ORGANIC}{HIGH_PLASTICITY}"
                    if (color or odor)
                    else f"{SILT}{HIGH_PLASTICITY}"
                )


def group_index(fines, liquid_limit, plasticity_index):
    """The `Group Index (GI)` is used to further evaluate soils with a group
    (subgroups).

    $$ GI = (F_{200} - 35)[0.2 + 0.005(LL - 40)] + 0.01(F_{200} - 15)(PI - 10) $$

    - $F_{200}$: Percentage by mass passing American Sieve No. 200.
    - LL: Liquid Limit (%), expressed as a whole number.
    - PI: Plasticity Index (%), expressed as a whole number.

    """

    gi = (fines - 35) * (0.2 + 0.005 * (liquid_limit - 40)) + 0.01 * (fines - 15) * (
        plasticity_index - 10
    )

    return 0.0 if gi <= 0 else gi


def aashto(
    liquid_limit, plastic_limit, plasticity_index, fines, sand=0.0, gravels=0.0
) -> str:
    """`AASHTO` classification system.

    Args:
        liquid_limit: Water content beyond which soils flows under their own weight. (%)
        plastic_limit: Water content at which plastic deformation can be initiated. (%)
        plasticity_index: Range of water content over which soil remains in plastic condition `PI = LL - PL` (%)
        fines: Percentage of fines in soil sample.
        sand:  Percentage of sand in soil sample. Defaults to 0.0.
        gravels: Percentage of gravels in soil sample. Defaults to 0.0.

    Raises:
        exceptions.PIValueError: Raised when PI != LL - PL.
    """

    _check_PI(liquid_limit, plastic_limit, plasticity_index)
    gi = group_index(fines, liquid_limit, plasticity_index)

    if fines <= 35:
        if liquid_limit <= 40:
            return f"A-2-4({gi})" if plasticity_index <= 10 else f"A-2-6({gi})"

        else:
            return f"A-2-5({gi})" if plasticity_index <= 10 else f"A-2-7({gi})"

    else:
        # Silts A4-A7
        if liquid_limit <= 40:
            return f"A-4({gi:.0f})" if plasticity_index <= 10 else f"A-6({gi:.0f})"

        else:
            if plasticity_index <= 10:
                return f"A-5({gi:.0f})"
            else:
                return (
                    f"A-7-5({gi:.0f})"
                    if plasticity_index <= (liquid_limit - 30)
                    else f"A-7-6({gi:.0f})"
                )
