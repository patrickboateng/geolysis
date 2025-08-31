from geolysis.foundation import Foundation
from geolysis.utils import round_

from ._core import AllowableBearingCapacity


class BowlesABC4PadFoundation(AllowableBearingCapacity):
    r"""Allowable bearing capacity for pad foundation on cohesionless
    soils according to `Bowles (1997)`.

    $$
     q_a(kPa) = 19.16(N_1)_{55} f_d\left(\dfrac{S}{25.4}\right),
                \ B \ \le \ 1.2m
     $$

     $$
     q_a(kPa) = 11.98(N_1)_{55}\left(\dfrac{3.28B + 1}{3.28B} \right)^2
                     f_d \left(\dfrac{S}{25.4}\right), \ B \ \gt 1.2m
     $$

     $$
     f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33
     $$

    - $q_a$ (kPa): Allowable bearing capacity
    - $N$: Corrected SPT N-value
    - $f_d$: Depth factor
    - $S$ (mm): Tolerable settlement
    - $B$ (m): Width of foundation footing
    - $D_f$ (m): Depth of foundation footing
    - $D_w$ (m): Depth of water below ground level

    """

    def __init__(
            self,
            corrected_spt_n_value: float,
            tol_settlement: float,
            foundation_size: Foundation,
    ) -> None:
        """
        :param corrected_spt_n_value: Statistical average of corrected
                                      SPT N-value (55% energy with
                                      overburden pressure correction)
                                      within the foundation influence
                                      zone i.e `0.5B` to `2B`.
        :param tol_settlement: Tolerable settlement of foundation (mm).
        :param foundation_size: Size of the foundation.
        """
        super().__init__(
            corrected_spt_n_value=corrected_spt_n_value,
            tol_settlement=tol_settlement,
            foundation_size=foundation_size,
        )

    @round_(ndigits=2)
    def bearing_capacity(self) -> float:
        """
        Calculate the allowable bearing capacity of the pad foundation.
        """
        n_corr = self.corrected_spt_n_value
        width = self.foundation_size.width

        if width <= 1.2:
            return 19.16 * n_corr * self._fd() * self._sr()

        return (
                11.98
                * n_corr
                * ((3.28 * width + 1) / (3.28 * width)) ** 2
                * self._fd()
                * self._sr()
        )


class BowlesABC4MatFoundation(BowlesABC4PadFoundation):
    r"""Allowable bearing capacity for mat foundation on cohesionless
    soils according to `Bowles (1997)`.

    $$
     q_a(kPa) = 11.98(N_1)_{55}f_d\left(\dfrac{S}{25.4}\right)
    $$

    $$
    f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33
    $$

    - $q_a$ (kPa): Allowable bearing capacity
    - $N$: Corrected SPT N-value
    - $f_d$: Depth factor
    - $S$ (mm): Tolerable settlement
    - $B$ (m): Width of foundation footing
    - $D_f$ (m): Depth of foundation footing
    - $D_w$ (m): Depth of water below ground level
    """

    @round_(ndigits=2)
    def bearing_capacity(self) -> float:
        """
        Calculate the allowable bearing capacity of the mat foundation.
        """
        n_corr = self.corrected_spt_n_value
        return 11.98 * n_corr * self._fd() * self._sr()
