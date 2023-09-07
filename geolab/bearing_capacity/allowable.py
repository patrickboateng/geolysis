import functools
import statistics
from typing import Iterable

from geolab import GeotechEng
from geolab.bearing_capacity.spt import spt_corrections


class meyerhof_bearing_capacity:
    r"""Meyerhoff Bearing Capacity.

    :param recorded_spt_nvalues: list of recorded SPT N-values
    :type recorded_spt_nvalue: int
    :param foundation_depth: depth of foundation (m)
    :type foundation_depth: float
    :param foundation_width: width of foundation (m)
    :type foundation_width: float
    :param actual_settlement: foundation settlement (mm)
    :type actual_settlement: float
    """

    ALLOWABLE_SETTLEMENT = 25.4

    def __init__(
        self,
        recorded_spt_nvalues: Iterable[int],
        *,
        foundation_depth: float = 1.5,
        foundation_width: float = 1.5,
        actual_settlement: float = 25.4,
    ) -> None:
        self.recorded_spt_nvalues = recorded_spt_nvalues
        self.foundation_depth = foundation_depth
        self.foundation_width = foundation_width
        self.actual_settlement = actual_settlement

    @property
    def depth_ftr(self) -> float:
        """"""
        x1 = self.foundation_depth / self.foundation_width
        df = 1 + 0.33 * x1  # depth factor

        return min(df, 1.33)

    @functools.cached_property
    def n_design(self) -> float:
        """"""
        # n_design is computed once per instance
        skempton_correction = spt_corrections(0, eng=GeotechEng.SKEMPTON)

        spt_corrected_vals = map(
            skempton_correction, self.recorded_spt_nvalues
        )
        return statistics.mean(spt_corrected_vals)

    def allowable_bearing_capacity(self) -> float:
        """"""
        abc: float  # allowable bearing capacity

        x1 = self.n_design * self.depth_ftr
        x2 = self.actual_settlement / self.ALLOWABLE_SETTLEMENT

        if self.foundation_width <= 1.22:
            abc = 19.16 * x1 * x2

        else:
            x3 = 3.28 * self.foundation_width + 1
            x4 = 3.28 * self.foundation_width

            abc = x1 * x2 * (11.98 * (x3 / x4)) ** 2

        return abc
