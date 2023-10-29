from geolysis.bearing_capacity import FoundationSize


class BowlesBearingCapacity:
    def __init__(self, foundation_size: FoundationSize):
        self.foundation_size = foundation_size

    @property
    def fd(self) -> float:
        r"""Return the depth factor.

        .. math::

            f_d = 1 + 0.33 \cdot \frac{D_f}{B}

        """
        return min(1 + 0.33 * self.foundation_size.d2w, 1.33)

    def allowable_1977(self, spt_corrected_nvalue: float) -> float:
        if self.foundation_size.width <= 1.2:
            return 20 * spt_corrected_nvalue * self.fd

        a = self.foundation_size.width + 0.3
        b = self.foundation_size.width
        return 12.5 * spt_corrected_nvalue * (a / b) ** 2 * self.fd
