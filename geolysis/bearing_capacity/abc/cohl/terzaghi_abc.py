from geolysis.foundation import Foundation
from geolysis.utils import round_

from ._core import AllowableBearingCapacity


class TerzaghiABC4PadFoundation(AllowableBearingCapacity):
    r"""Allowable bearing capacity for pad foundation on cohesionless
    soils according to ``Terzaghi & Peck (1948)``.

    :Equation:

    .. math::

         q_a(kPa) &= 12N \dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right),
                     \ B \ \le 1.2m

         q_a(kPa) &= 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2\dfrac{1}
                     {c_w f_d}\left(\dfrac{S}{25.4}\right), \ B \ \gt 1.2m

         f_d &= 1 + 0.25 \cdot \frac{D_f}{B} \le 1.25

         c_w &= 2 - \frac{D_w}{2B} \le 2, D_w \gt D_f

         c_w &= 2 - \frac{D_f}{2B} \le 2, D_w \le D_f

    ===================  ======================================  ===========
     Symbol                Description                              Unit
    ===================  ======================================  ===========
    :math:`q_a`          Allowable bearing capacity               :math:`kPa`
    :math:`N`            Corrected SPT N-value                     —
    :math:`f_d`          Depth factor                              —
    :math:`c_w`          Water correction factor                   —
    :math:`S`            Tolerable settlement                     :math:`mm`
    :math:`B`            Width of foundation footing              :math:`m`
    :math:`D_f`          Depth of foundation footing              :math:`m`
    :math:`D_w`          Depth of water below ground level        :math:`m`
    ===================  ======================================  ===========
    """

    def __init__(self, corrected_spt_n_value: float,
                 tol_settlement: float,
                 foundation_size: Foundation) -> None:
        """
        :param corrected_spt_n_value: Lowest (or average) uncorrected SPT 
                                      N-value (60% energy) within the foundation 
                                      influence zone i.e :math:`D_f` to 
                                      :math:`D_f + 2B`
        :type corrected_spt_n_value: float

        :param tol_settlement: Tolerable settlement of foundation (mm).
        :type tol_settlement: float

        :param foundation_size: Size of the foundation.
        :type foundation_size: Foundation
        """
        super().__init__(corrected_spt_n_value=corrected_spt_n_value,
                         tol_settlement=tol_settlement,
                         foundation_size=foundation_size)

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

        if water_level is None:
            return 2.0

        if water_level <= depth:
            cw = 2.0 - depth / (2.0 * width)
        else:
            cw = 2.0 - water_level / (2.0 * width)

        return min(cw, 2.0)

    @round_(ndigits=2)
    def bearing_capacity(self):
        """Calculates the allowable bearing capacity of the pad foundation."""
        n_corr = self.corrected_spt_n_value
        width = self.foundation_size.width

        if width <= 1.2:
            return 12 * n_corr * (1 / (self._cw() * self._fd())) * self._sr()

        return (8 * n_corr * ((3.28 * width + 1) / (3.28 * width)) ** 2
                * (1 / (self._cw() * self._fd())) * self._sr())


class TerzaghiABC4MatFoundation(TerzaghiABC4PadFoundation):
    r"""Allowable bearing capacity for mat foundation on cohesionless soils
    according to ``Terzaghi & Peck (1948)``.

    :Equation:

    .. math::

         q_a(kPa) &= 8N\dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right)

         f_d &= 1 + 0.25 \cdot \frac{D_f}{B} \le 1.25

         c_w &= 2 - \frac{D_w}{2B} \le 2, D_w \gt D_f

         c_w &= 2 - \frac{D_f}{2B} \le 2, D_w \le D_f

    ===================  ======================================  ===========
     Symbol                Description                              Unit
    ===================  ======================================  ===========
    :math:`q_a`          Allowable bearing capacity               :math:`kPa`
    :math:`N`            Corrected SPT N-value                     —
    :math:`f_d`          Depth factor                              —
    :math:`c_w`          Water correction factor                   —
    :math:`S`            Tolerable settlement                     :math:`mm`
    :math:`B`            Width of foundation footing              :math:`m`
    :math:`D_f`          Depth of foundation footing              :math:`m`
    :math:`D_w`          Depth of water below ground level        :math:`m`
    ===================  ======================================  ===========
    """

    @round_(ndigits=2)
    def bearing_capacity(self):
        """Calculates the allowable bearing capacity of the mat foundation."""
        n_corr = self.corrected_spt_n_value
        return 8 * n_corr * (1 / (self._cw() * self._fd())) * self._sr()
