from geolysis.bearing_capacity.abc.cohl import AllowableBearingCapacity
from geolysis.foundation import FoundationSize
from geolysis.utils import round_
from geolysis import validators

class TerzaghiABC4PadFoundation(AllowableBearingCapacity):
    """Allowable bearing capacity for pad foundation on cohesionless
    soils according to ``Terzaghi & Peck (1948)``.
    """

    def __init__(self, corrected_spt_n_value: float, 
                 tol_settlement: float,
                 ground_water_level: float, 
                 foundation_size: FoundationSize) -> None:
        """
        :param corrected_spt_n_value: Lowest (or average) uncorrected SPT 
                                      N-value (60% energy) within the foundation 
                                      influence zone i.e :math:`D_f` to 
                                      :math:`D_f + 2B`
        :type corrected_spt_n_value: float

        :param tol_settlement: Tolerable settlement of foundation (mm).
        :type tol_settlement: float

        :param ground_water_level: Depth of water below ground level (mm).
        :type ground_water_level: float

        :param foundation_size: Size of the foundation.
        :type foundation_size: FoundationSize
        """
        super().__init__(corrected_spt_n_value, tol_settlement, foundation_size)
        self.ground_water_level = ground_water_level

    @property
    def ground_water_level(self) -> float:
        return self._ground_water_level

    @ground_water_level.setter
    @validators.ge(0.0)
    def ground_water_level(self, val: float) -> None:
        self._ground_water_level = val

    def _fd(self) -> float:
        """Calculate the depth factor."""
        depth = self.foundation_size.depth
        width = self.foundation_size.width

        return min(1.0 + 0.25 * depth / width, 1.25)

    def _cw(self):
        """Calculate the water correction factor."""
        depth = self.foundation_size.depth
        width = self.foundation_size.width

        if self.ground_water_level <= depth:
            cw = 2.0 - depth / (2.0 * width)
        else:
            cw = 2.0 - self.ground_water_level / (2.0 * width)

        return min(cw, 2.0)

    @round_
    def bearing_capacity(self):
        r""" Calculates the allowable bearing capacity of the pad foundation. 

        .. math::

            q_a(kPa) &= 12N \dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right),
                        \ B \ \le 1.2m

            q_a(kPa) &= 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2\dfrac{1}
                        {c_w f_d}\left(\dfrac{S}{25.4}\right), \ B \ \gt 1.2m

            f_d &= 1 + 0.25 \cdot \frac{D_f}{B} \le 1.25

        Water correction for surface footing:

        .. math:: c_w = 2 - \frac{D_w}{2B} \le 2

        Water correction for fully submerged footing :math:`D_w \le D_f`

        .. math:: c_w = 2 - \frac{D_f}{2B} \le 2
        """
        n_corr = self.corrected_spt_n_value
        width = self.foundation_size.width

        if width <= 1.2:
            return 12 * n_corr * (1 / (self._cw() * self._fd())) * self._sr()

        return 8 * n_corr * ((3.28 * width + 1) / (3.28 * width)) ** 2 \
               * (1 / (self._cw() * self._fd())) * self._sr()


class TerzaghiABC4MatFoundation(TerzaghiABC4PadFoundation):
    """Allowable bearing capacity for mat foundation on cohesionless soils
    according to ``Terzaghi & Peck (1948)``.
    """

    @round_
    def bearing_capacity(self):
        r"""Calculates the allowable bearing capacity of the mat foundation.

        .. math:: 
        
            q_a(kPa) &= 8N\dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right)

            f_d &= 1 + 0.25 \cdot \frac{D_f}{B} \le 1.25

        Water correction for surface footing:

        .. math:: c_w = 2 - \frac{D_w}{2B} \le 2

        Water correction for fully submerged footing :math:`D_w \le D_f`

        .. math:: c_w = 2 - \frac{D_f}{2B} \le 2
        """
        n_corr = self.corrected_spt_n_value
        return 8 * n_corr * (1 / (self._cw() * self._fd())) * self._sr()

