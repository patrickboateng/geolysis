from geolysis.bearing_capacity import (
    CircularFooting,
    FoundationSize,
    RectangularFooting,
    SquareFooting,
)
from geolysis.utils import round_


def nc4strpf(Df, B) -> float:
    return min(5 * (1 + 0.2 * Df / B), 7.5)


def nc4sqrf(Df, B) -> float:
    return min(6 * (1 + 0.2 * Df / B), 9)


def nc4rectf(Df, L, B) -> float:
    if Df / B <= 2.5:
        nc = 5 * (1 + 0.2 * B / L) * (1 + 0.2 * Df / B)

    else:
        nc = 7.5 * (1 + 0.2 * B / L)

    return min(nc, 9)


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
    if isinstance(
        foundation_size.footing_size, (SquareFooting, CircularFooting)
    ):
        nc = nc4sqrf(foundation_size.depth, foundation_size.footing_size.width)

    elif isinstance(foundation_size.footing_size, RectangularFooting):
        nc = nc4rectf(
            foundation_size.depth,
            foundation_size.footing_size.length,
            foundation_size.footing_size.width,
        )

    else:
        nc = nc4strpf(
            foundation_size.depth, foundation_size.footing_size.width
        )

    return 2 * spt_n_60 * nc


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
    if isinstance(
        foundation_size.footing_size, (SquareFooting, CircularFooting)
    ):
        nc = nc4sqrf(foundation_size.depth, foundation_size.footing_size.width)

    elif isinstance(foundation_size.footing_size, RectangularFooting):
        nc = nc4rectf(
            foundation_size.depth,
            foundation_size.footing_size.length,
            foundation_size.footing_size.width,
        )

    else:
        nc = nc4strpf(
            foundation_size.depth, foundation_size.footing_size.width
        )
    return 2 * spt_n_design * nc
