from geolysis.bearing_capacity import FoundationSize, _chk_settlement
from geolysis.utils import round_


@round_(ndigits=2)
def bowles_abc_chl_1997(
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
