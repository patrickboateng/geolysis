from geolab.exceptions import AllowableSettlementError


def _fd(foundation_depth: float, foundation_width: float) -> float:
    x_1 = foundation_depth / foundation_width
    fd = 1 + 0.33 * x_1  # depth factor

    return min(fd, 1.33)


class MeyerhofBearingCapacity:
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
        r"""Return the depth factor.

        .. math::

            f_d = 1 + 0.33 \cdot \frac{D_f}{B}

        """

        return _fd(self.foundation_depth, self.foundation_width)

    def net_allowable(self, n_design: float) -> float:
        r"""Return the net allowable bearing capacity.

        .. math::

            q_{a(net)} &= 19.16 \cdot N_{des} \cdot f_d \cdot \dfrac{S_e}{25.4} \, , \, B \le 1.22

            q_{a(net)} &= 11.98 \cdot N_{des} \cdot \left(\dfrac{3.28B + 1}{3.28B} \right)^2 \cdot f_d \cdot \dfrac{S_e}{25.4} \, , \, B \gt 1.22


        :raises AllowableSettlementError: If actual settlement is greater than
                                          allowable settement
        """

        if self.actual_settlement > self.ALLOWABLE_SETTLEMENT:
            msg = f"Settlement: {self.actual_settlement}should be less than \
                  Allowable Settlement: {self.ALLOWABLE_SETTLEMENT}"
            raise AllowableSettlementError(msg)

        abc: float  # allowable bearing capacity

        x_1 = n_design * self.f_d
        x_2 = self.actual_settlement / self.ALLOWABLE_SETTLEMENT

        if self.foundation_width <= 1.22:
            abc = 19.16 * x_1 * x_2

        else:
            x_3 = 3.28 * self.foundation_width + 1
            x_4 = 3.28 * self.foundation_width

            abc = x_1 * x_2 * (11.98 * (x_3 / x_4)) ** 2

        return abc

    def allowable_1956(self, spt_n60: float) -> float:
        """"""
        abc: float

        if self.foundation_width <= 1.2:
            abc = 12 * spt_n60 * self.f_d

        else:
            x_1 = 8 * spt_n60
            x_2 = (self.foundation_width + 0.3) / self.foundation_width
            abc = x_1 * x_2**2 * self.f_d

        return abc


class BowlesBearingCapacity:
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
            x_1 = 12.5 * spt_corrected_nvalue
            x_2 = (self.foundation_width + 0.3) / self.foundation_width
            abc = x_1 * x_2**2 * self.f_d

        return abc
