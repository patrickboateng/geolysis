from geolysis.bearing_capacity import FoundationSize, check_settlement
from geolysis.utils import round_


@round_(ndigits=2)
def meyerhof_abc_chl_1956(
    spt_n_val: float,
    actual_settlement: float,
    foundation_size: FoundationSize,
):
    """Return allowable bearing capacity for cohesionless soils according to
    ``Meyerhof (1956)``.

    :param float spt_n_val:
        Average uncorrected SPT N-values within the foundation influence
        zone i.e. :math:`D_f` |rarr| :math:`D_f + 2B`.
    :param FoundationSize foundation_size:
        Foundation size i.e. width, length and depth of the foundation
    :param float actual_settlement:
        Measured settlement in the field (mm)
    """

    allowable_settlement = 25.4

    check_settlement(actual_settlement, allowable_settlement)

    B = foundation_size.footing_size.width
    fd = min(1 + 0.33 * foundation_size.depth / B, 1.33)
    settlement_ratio = actual_settlement / allowable_settlement

    if B <= 1.2:
        return 12 * spt_n_val * fd * settlement_ratio

    return 8 * spt_n_val * ((B + 0.3) / B) ** 2 * fd * settlement_ratio
