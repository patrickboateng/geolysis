"""Meyerhof Bearing Capacity Analysis."""

from geolab import DECIMAL_PLACES
from geolab.bearing_capacity import depth_factor
from geolab.exceptions import AllowableSettlementError


def _check_foundation_settlement(
    actual_settlement: float, allow_settlement: float
):
    if actual_settlement > allow_settlement:
        msg = f"actual_settlement: {actual_settlement} cannot be greater than {allow_settlement}"
        raise AllowableSettlementError(msg)


def nc():
    ...


def nq():
    ...


def ngamma():
    ...


def meyerhof_allow_bearing_capacity(
    n_design,
    foundation_depth,
    foundation_width,
    actual_settlement,
) -> float:
    r"""Allowable bearing capacity :math:`q_{a(net)}` for a given tolerable
        settlement proposed by ``Meyerhof``.

        .. math::

            if B \le 1.22:

                q_{a(net)} = 19.16 N_des F_d \frac{S_e}{25.4}

            if B \gt 1.22:

                q_{a(net)} = 11.98 N_des (\frac{3.28B + 1}{3.28B})^2 F_d \frac{S_e}{25.4}

    :param n_design: average corrected number of blows from ``SPT N-value``
    :type n_design: float
    :param foundation_depth: depth of foundation (m)
    :type foundation_depth: float
    :param foundation_width: width of foundation (m)
    :type foundation_width: float
    :param actual_settlement: foundation settlement (mm)
    :type actual_settlement: float
    :raises AllowableSettlementError: Raised when ``allow_settlement`` is greater than ``25.4mm``
    :return: allowable bearing capacity
    :rtype: float

    """
    ALLOWABLE_SETTLEMENT = 25.4
    _check_foundation_settlement(actual_settlement, ALLOWABLE_SETTLEMENT)

    expr = (
        n_design
        * depth_factor(foundation_depth, foundation_width)
        * (actual_settlement / ALLOWABLE_SETTLEMENT)
    )
    if foundation_width <= 1.22:
        _abc = 19.16 * expr  # allow_bearing_capacity
        return round(_abc, DECIMAL_PLACES)

    # allow_bearing_capacity
    _abc = (
        11.98
        * ((3.28 * foundation_width + 1) / (3.28 * foundation_width)) ** 2
        * expr
    )
    return round(_abc, DECIMAL_PLACES)
