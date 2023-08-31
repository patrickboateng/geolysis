"""Meyerhof Bearing Capacity Analysis."""

from typing import Iterable

from geolab.bearing_capacity import depth_ftr
from geolab.exceptions import AllowableSettlementError

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


def _check_foundation_settlement(
    actual_settlement: float, allow_settlement: float
):
    if actual_settlement > allow_settlement:
        msg = f"actual_settlement: {actual_settlement} cannot be greater than {allow_settlement}"
        raise AllowableSettlementError(msg)


class meyerhoff_bearing_capacity:
    def __init__(
        self,
        *,
        recorded_spt_nvalues: Iterable,
        foundation_depth: float,
        foundation_width: float,
        actual_settlement: float,
    ) -> None:
        self.recorded_spt_nvalues = recorded_spt_nvalues
        self.foundation_depth = foundation_depth
        self.foundation_width = foundation_width
        self.actual_settlement = actual_settlement

    @property
    def n_design(self) -> float:
        ...

    def allowable_bearing_capacity(self) -> float:
        abc: float  # allowable bearing capacity

        ALLOWABLE_SETTLEMENT = 25.4
        _check_foundation_settlement(
            self.actual_settlement, ALLOWABLE_SETTLEMENT
        )

        x1 = n_design * depth_ftr(foundation_depth, foundation_width)  # type: ignore
        x2 = self.actual_settlement / ALLOWABLE_SETTLEMENT

        if self.foundation_width <= 1.22:
            abc = 19.16 * x1 * x2

        else:
            x3 = (
                11.98
                * (3.28 * self.foundation_width + 1)
                / (3.28 * self.foundation_width)
            )

            abc = x1 * x2 * x3**2

        return abc

    def nc(self):
        ...

    def nq(self):
        ...

    def ngamma(self):
        ...
