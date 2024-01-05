from geolysis.utils import round_

from ._base import FoundationSize, _chk_settlement


@round_(ndigits=2)
def bowles_cohl_abc_1997(
    spt_n_design: float,
    actual_settlement: float,
    foundation_size: FoundationSize,
):
    """Return allowable bearing capacity for cohesionless soils according to
    ``Bowles (1997)``. (:math:`kN/m^2`)

    :param float spt_n_design:
        Weighted average of corrected SPT N-values within the foundation
        influence zone i.e. :math:`D_f` |rarr| :math:`D_f + 2B`.
    :param FoundationSize foundation_size:
        Foundation size i.e. width, length and depth of the foundation
    :param float actual_settlement:
        Measured settlement in the field (mm)
    """
    allowable_settlement: float = 25.4

    _chk_settlement(actual_settlement, allowable_settlement)

    Df = foundation_size.depth
    B = foundation_size.footing_size.width
    fd = min(1 + 0.33 * Df / B, 1.33)
    settlement_ratio = actual_settlement / allowable_settlement

    if B <= 1.2:
        return 19.16 * spt_n_design * fd * settlement_ratio

    return (
        11.98
        * fd
        * spt_n_design
        * ((3.28 * B + 1) / (3.28 * B)) ** 2
        * settlement_ratio
    )


@round_(ndigits=2)
def meyerhof_cohl_abc_1956(
    spt_n_val: float,
    actual_settlement: float,
    foundation_size: FoundationSize,
):
    """Return allowable bearing capacity for cohesionless soils according to
    ``Meyerhof (1956)``. (:math:`kN/m^2`)

    :param float spt_n_val:
        Average uncorrected SPT N-values within the foundation influence
        zone i.e. :math:`D_f` |rarr| :math:`D_f + 2B`.
    :param FoundationSize foundation_size:
        Foundation size i.e. width, length and depth of the foundation
    :param float actual_settlement:
        Measured settlement in the field (mm)
    """

    allowable_settlement = 25.4

    _chk_settlement(actual_settlement, allowable_settlement)

    Df = foundation_size.depth
    B = foundation_size.footing_size.width
    fd = min(1 + 0.33 * Df / B, 1.33)
    settlement_ratio = actual_settlement / allowable_settlement

    if B <= 1.2:
        return 12 * spt_n_val * fd * settlement_ratio

    return 8 * spt_n_val * ((B + 0.3) / B) ** 2 * fd * settlement_ratio


@round_(ndigits=2)
def terzaghi_peck_cohl_abc_1948(
    spt_n_val: float,
    actual_settlement: float,
    water_depth: float,
    foundation_size: FoundationSize,
):
    """Return allowable bearing capacity for cohesionless soils according to
    ``Terzaghi & Peck (1948)``. (:math:`kN/m^2`)

    :param float spt_n_val:
        Average uncorrected SPT N-values within the foundation influence
        zone i.e. :math:`D_f` |rarr| :math:`D_f + 2B`.
    :param FoundationSize foundation_size:
        Foundation size i.e. width, length and depth of the foundation
    :param float actual_settlement:
        Measured settlement in the field (mm)
    """

    allowable_settlement = 25.4

    _chk_settlement(actual_settlement, allowable_settlement)

    Df = foundation_size.depth
    B = foundation_size.footing_size.width
    fd = min(1 + 0.25 * Df / B, 1.25)
    settlement_ratio = actual_settlement / allowable_settlement

    if water_depth <= Df:
        cw = 2 - Df / (2 * B)
    else:
        cw = 2 - water_depth / (2 * B)

    cw = min(cw, 2)

    if B <= 1.2:
        return 12 * spt_n_val * (1 / (cw * fd)) * settlement_ratio

    return (
        8
        * spt_n_val
        * (1 / (cw * fd))
        * ((3.28 * B + 1) / (3.28 * B)) ** 2
        * settlement_ratio
    )
