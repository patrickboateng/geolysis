from geolysis.foundation import Foundation
from geolysis.utils import round_

from ._core import AllowableBearingCapacity


class MeyerhofABC4PadFoundation(AllowableBearingCapacity):
    """Allowable bearing capacity for pad foundation on cohesionless
    soils according to `Meyerhof (1956)`.

    See [implementation](../formulas/allowable-bearing-capacity.md/#meyerhof-bearing-capacity-for-pad-foundation)
    for more details on bearing capacity equation used.

    """

    def __init__(
            self,
            corrected_spt_n_value: float,
            tol_settlement: float,
            foundation_size: Foundation,
    ):
        """
        :param corrected_spt_n_value: Average uncorrected SPT N-value
                                      (60% energy with dilatancy (water)
                                      correction if applicable) within
                                      the foundation influence zone i.e.
                                      $D_f$ to $D_f + 2B$.
        :param tol_settlement: Tolerable settlement of foundation (mm).
        :param foundation_size: Size of the foundation.
        """
        super().__init__(
            corrected_spt_n_value=corrected_spt_n_value,
            tol_settlement=tol_settlement,
            foundation_size=foundation_size,
        )

    @round_(ndigits=2)
    def _bearing_capacity(self):
        """
        Calculates the allowable bearing capacity of the pad foundation.
        """
        n_corr = self.corrected_spt_n_value
        width = self.foundation_size.width

        if width <= 1.2:
            return 12 * n_corr * self._fd() * self._sr()

        return (
                8
                * n_corr
                * ((3.28 * width + 1) / (3.28 * width)) ** 2
                * self._fd()
                * self._sr()
        )


class MeyerhofABC4MatFoundation(MeyerhofABC4PadFoundation):
    """Allowable bearing capacity for mat foundation on cohesionless
    soils according to `Meyerhof (1956)`.

    See [implementation](../formulas/allowable-bearing-capacity.md/#meyerhof-bearing-capacity-for-mat-foundation)
    for more details on bearing capacity equation used.

    """

    @round_(ndigits=2)
    def _bearing_capacity(self):
        """Calculate the allowable bearing capacity of the mat foundation."""
        n_corr = self.corrected_spt_n_value
        return 8 * n_corr * self._fd() * self._sr()
