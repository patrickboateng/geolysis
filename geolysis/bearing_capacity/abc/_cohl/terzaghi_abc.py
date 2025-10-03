from geolysis.foundation import Foundation
from geolysis.utils import round_, isinf

from ._core import AllowableBearingCapacity, AllowableBearingCapacityResult


class TerzaghiABC4PadFoundation(AllowableBearingCapacity):
    """Allowable bearing capacity for pad foundation on cohesionless
    soils according to `Terzaghi & Peck (1948)`.

    See [implementation](../formulas/allowable-bearing-capacity.md/#terzaghi-bearing-capacity-for-pad-foundation)
    for more details on bearing capacity equation used.

    """

    def __init__(
        self,
        corrected_spt_n_value: float,
        tol_settlement: float,
        foundation_size: Foundation,
    ) -> None:
        """
        :param corrected_spt_n_value: Lowest (or average) uncorrected
                                      SPT N-value (60% energy) within
                                      the foundation influence zone i.e.
                                      $D_f$ to $D_f + 2B$
        :param tol_settlement: Tolerable settlement of foundation (mm).
        :param foundation_size: Size of the foundation.
        """
        super().__init__(
            corrected_spt_n_value=corrected_spt_n_value,
            tol_settlement=tol_settlement,
            foundation_size=foundation_size,
        )

    def _fd(self) -> float:
        """Calculate the depth factor."""
        depth = self.foundation_size.depth
        width = self.foundation_size.width

        return min(1.0 + 0.25 * depth / width, 1.25)

    def _cw(self):
        """Calculate the water correction factor."""
        depth = self.foundation_size.depth
        width = self.foundation_size.width
        water_level = self.foundation_size.ground_water_level

        if isinf(water_level):
            return 2.0

        if water_level <= depth:
            cw = 2.0 - depth / (2.0 * width)
        else:
            cw = 2.0 - water_level / (2.0 * width)

        return min(cw, 2.0)

    @round_(ndigits=2)
    def _bearing_capacity(self):
        """
        Calculates the allowable bearing capacity of the pad foundation.
        """
        n_corr = self.corrected_spt_n_value
        width = self.foundation_size.width

        if width <= 1.2:
            return 12 * n_corr * (1 / (self._cw() * self._fd())) * self._sr()

        return (
            8
            * n_corr
            * ((3.28 * width + 1) / (3.28 * width)) ** 2
            * (1 / (self._cw() * self._fd()))
            * self._sr()
        )

    def bearing_capacity_results(self) -> AllowableBearingCapacityResult:
        res = super().bearing_capacity_results()
        res.water_correction_factor = self._cw()
        return res


class TerzaghiABC4MatFoundation(TerzaghiABC4PadFoundation):
    """Allowable bearing capacity for mat foundation on cohesionless
    soils according to `Terzaghi & Peck (1948)`.

    See [implementation](../formulas/allowable-bearing-capacity.md/#terzaghi-bearing-capacity-for-mat-foundation)
    for more details on bearing capacity equation used.

    """

    @round_(ndigits=2)
    def _bearing_capacity(self):
        """
        Calculates the allowable bearing capacity of the mat foundation.
        """
        n_corr = self.corrected_spt_n_value
        return 8 * n_corr * (1 / (self._cw() * self._fd())) * self._sr()
