from geolysis.bearing_capacity import FoundationSize


class BowlesBearingCapacity:
    def __init__(self, foundation_size: FoundationSize):
        self.foundation_size = foundation_size

    @property
    def f_d(self) -> float:
        """Return the depth factor."""

        return min(1 + 0.33 * self.foundation_size.d2w, 1.33)

    def allowable_1977(self, spt_corrected_nvalue: float) -> float:
        if self.foundation_size.width <= 1.2:
            return 20 * spt_corrected_nvalue * self.f_d

        x_1 = 12.5 * spt_corrected_nvalue
        x_2 = (self.foundation_size.width + 0.3) / self.foundation_size.width
        return x_1 * x_2**2 * self.f_d
