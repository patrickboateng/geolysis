def _fd(foundation_depth: float, foundation_width: float) -> float:
    x1 = foundation_depth / foundation_width
    fd = 1 + 0.33 * x1  # depth factor

    return min(fd, 1.33)


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
        *,
        foundation_depth: float = 1.5,
        foundation_width: float = 1.5,
        actual_settlement: float = 25.4,
    ) -> None:
        self.foundation_depth = foundation_depth
        self.foundation_width = foundation_width
        self.actual_settlement = actual_settlement

    @property
    def f_d(self) -> float:
        """Return the depth factor."""

        return _fd(self.foundation_depth, self.foundation_width)

    def net_allowable(self, n_design: float) -> float:
        """"""
        abc: float  # allowable bearing capacity

        x1 = n_design * self.f_d
        x2 = self.actual_settlement / self.ALLOWABLE_SETTLEMENT

        if self.foundation_width <= 1.22:
            abc = 19.16 * x1 * x2

        else:
            x3 = 3.28 * self.foundation_width + 1
            x4 = 3.28 * self.foundation_width

            abc = x1 * x2 * (11.98 * (x3 / x4)) ** 2

        return abc

    def allowable_1956(self, spt_n60: float) -> float:
        """"""
        abc: float

        if self.foundation_width <= 1.2:
            abc = 12 * spt_n60 * self.f_d

        else:
            x1 = 8 * spt_n60
            x2 = (self.foundation_width + 0.3) / self.foundation_width
            abc = x1 * x2**2 * self.f_d

        return abc


class bowles_bearing_capacity:
    def __init__(
        self,
        foundation_depth: float,
        foundation_width: float,
    ):
        self.foundation_depth = foundation_depth
        self.foundation_width = foundation_width

    @property
    def f_d(self) -> float:
        """Return the depth factor."""

        return _fd(self.foundation_depth, self.foundation_width)

    def allowable_1977(self, spt_corrected_nvalue: float) -> float:
        abc: float
        if self.foundation_width <= 1.2:
            abc = 20 * spt_corrected_nvalue * self.f_d
        else:
            x1 = 12.5 * spt_corrected_nvalue
            x2 = (self.foundation_width + 0.3) / self.foundation_width
            abc = x1 * x2**2 * self.f_d

        return abc
