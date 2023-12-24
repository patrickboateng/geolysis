from geolysis.bearing_capacity import FootingShape, FoundationSize
from geolysis.utils import round_


def bcf(foundation_size: FoundationSize) -> float:
    """Return bearing capacity factor."""
    Df = foundation_size.depth
    B = foundation_size.width
    L = foundation_size.length

    if foundation_size.is_strip_footing():
        _bcf = min(5 * (1 + 0.2 * Df / B), 7.5)

    elif (
        foundation_size.footing_shape is FootingShape.SQUARE
        or foundation_size.footing_shape is FootingShape.CIRCULAR
    ):
        _bcf = min(6 * (1 + 0.2 * Df / B), 9)

    else:
        if Df / B <= 2.5:
            _bcf = 5 * (1 + 0.2 * B / L) * (1 + 0.2 * Df / B)

        else:
            _bcf = 7.5 * (1 + 0.2 * B / L)

        _bcf = min(_bcf, 9)

    return _bcf


@round_(ndigits=2)
def skempton_net_sbc_coh_1957(
    spt_n_60: float,
    foundation_size: FoundationSize,
) -> float:
    """Return net safe bearing capacity for cohesive soils according to
    ``Skempton (1957)``.

    :param float spt_n_60:
        SPT N-value standardized for field procedures
    :param FoundationSize foundation_size:
        Foundation size i.e. width, length and depth of the foundation
    """
    _bcf = bcf(foundation_size)
    return 2 * spt_n_60 * _bcf


@round_(ndigits=2)
def skempton_net_abc_coh_1957(
    spt_n_design: float,
    foundation_size: FoundationSize,
) -> float:
    """Return net allowable bearing capacity for cohesive soils according to
    ``Skempton (1957)``.

    :param float spt_n_design:
        Weighted average of corrected SPT N-values within the foundation
        influence zone i.e. :math:`D_f` |rarr| :math:`D_f + 2B`.
    :param FoundationSize foundation_size:
        Foundation size i.e. width, length and depth of the foundation
    """
    _bcf = bcf(foundation_size)
    return 2 * spt_n_design * _bcf
