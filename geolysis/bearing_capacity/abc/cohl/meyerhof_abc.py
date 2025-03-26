from geolysis.foundation import FoundationSize
from geolysis.utils import round_

from ._core import AllowableBearingCapacity


class MeyerhofABC4PadFoundation(AllowableBearingCapacity):
    r"""Allowable bearing capacity for pad foundation on cohesionless soils
    according to ``Meyerhof (1956)``.

    :Equation:

    .. math::

         q_a(kPa) &= 12N f_d\left(\dfrac{S}{25.4}\right), \ B \ \le 1.2m

         q_a(kPa) &= 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2 f_d\left(
                 \dfrac{S}{25.4}\right), \ B \ \gt 1.2m

         f_d &= 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33

    ===================  ======================================  ===========
     Symbol                Description                              Unit
    ===================  ======================================  ===========
    :math:`q_a`          Allowable bearing capacity               :math:`kPa`
    :math:`N`            Corrected SPT N-value                     —
    :math:`f_d`          Depth factor                              —
    :math:`S`            Tolerable settlement                     :math:`mm`
    :math:`B`            Width of foundation footing              :math:`m`
    :math:`D_f`          Depth of foundation footing              :math:`m`
    ===================  ======================================  ===========
    """

    def __init__(self, corrected_spt_n_value: float,
                 tol_settlement: float,
                 foundation_size: FoundationSize):
        """
        :param corrected_spt_n_value: Average uncorrected SPT N-value (60% 
                                      energy with dilatancy (water) correction 
                                      if applicable) within the foundation 
                                      influence  zone i.e :math:`D_f` to
                                      :math:`D_f + 2B`.
        :type corrected_spt_n_value: float

        :param tol_settlement: Tolerable settlement of foundation (mm).
        :type tol_settlement: float

        :param foundation_size: Size of the foundation.
        :type foundation_size: FoundationSize
        """
        super().__init__(corrected_spt_n_value=corrected_spt_n_value,
                         tol_settlement=tol_settlement,
                         foundation_size=foundation_size)

    @round_(ndigits=2)
    def bearing_capacity(self):
        """Calculates the allowable bearing capacity of the pad foundation."""
        n_corr = self.corrected_spt_n_value
        width = self.foundation_size.width

        if width <= 1.2:
            return 12 * n_corr * self._fd() * self._sr()

        return (8 * n_corr * ((3.28 * width + 1) / (3.28 * width)) ** 2
                * self._fd() * self._sr())


class MeyerhofABC4MatFoundation(MeyerhofABC4PadFoundation):
    r"""Allowable bearing capacity for mat foundation on cohesionless soils
    according to ``Meyerhof (1956)``.

    :Equation:

    .. math::

         q_a(kPa) &= 8 N f_d\left(\dfrac{S}{25.4}\right)

         f_d &= 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33

    ===================  ======================================  ===========
     Symbol                Description                              Unit
    ===================  ======================================  ===========
    :math:`q_a`          Allowable bearing capacity               :math:`kPa`
    :math:`N`            Corrected SPT N-value                     —
    :math:`f_d`          Depth factor                              —
    :math:`S`            Tolerable settlement                     :math:`mm`
    :math:`B`            Width of foundation footing              :math:`m`
    :math:`D_f`          Depth of foundation footing              :math:`m`
    ===================  ======================================  ===========
    """

    @round_(ndigits=2)
    def bearing_capacity(self):
        """Calculate the allowable bearing capacity of the mat foundation."""
        n_corr = self.corrected_spt_n_value
        return 8 * n_corr * self._fd() * self._sr()
