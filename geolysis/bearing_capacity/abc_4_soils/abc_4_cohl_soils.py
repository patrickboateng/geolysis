from abc import ABC, abstractmethod

from geolysis.foundation import FoundationSize
from geolysis.utils import round_

__all__ = [
    "BowlesABC4PadFoundation",
    "BowlesABC4MatFoundation",
    "MeyerhofABC4PadFoundation",
    "MeyerhofABC4MatFoundation",
    "TerzaghiABC4PadFoundation",
    "TerzaghiABC4MatFoundation",
]


class SettlementError(ValueError):
    pass


class AllowableBearingCapacity(ABC):
    #: Maximum tolerable foundation settlement.
    MAX_TOL_SETTLEMENT = 25.4

    def __init__(self, corrected_spt_number: float, tol_settlement: float,
                 foundation_size: FoundationSize) -> None:
        self.corrected_spt_number = corrected_spt_number
        self.tol_settlement = tol_settlement
        self.foundation_size = foundation_size

    @property
    def tol_settlement(self) -> float:
        return self._tol_settlement

    @tol_settlement.setter
    def tol_settlement(self, tol_settlement: float) -> None:
        self._chk_settlement(tol_settlement, self.MAX_TOL_SETTLEMENT)
        self._tol_settlement = tol_settlement

    def _sr(self) -> float:
        return self._tol_settlement / self.MAX_TOL_SETTLEMENT

    def _fd(self) -> float:
        f_d = self.foundation_size.depth
        f_w = self.foundation_size.width
        return min(1 + 0.33 * f_d / f_w, 1.33)

    @staticmethod
    def _chk_settlement(tol_settlement: float, max_tol_settlement: float):
        if tol_settlement > max_tol_settlement:
            err_msg = "tol_settlement should not be greater than 25.4."
            raise SettlementError(err_msg)

    @abstractmethod
    def bearing_capacity(self): ...


class BowlesABC4PadFoundation(AllowableBearingCapacity):
    r"""Allowable bearing capacity for mat foundation on cohesionless
    soils according to ``Bowles (1997)``.

    Notes
    -----
    Allowable bearing capacity for ``isolated/pad/spread`` foundations:

    .. math::

        q_a(kPa) &= 19.16(N_1)_{55} f_d\left(\dfrac{S}{25.4}\right),
                    \ B \ \le \ 1.2m

        q_a(kPa) &= 11.98(N_1)_{55}\left(\dfrac{3.28B + 1}{3.28B} \right)^2
                    f_d \left(\dfrac{S}{25.4}\right), \ B \ \gt 1.2m

    Depth factor:

    .. math:: f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33
    """

    def __init__(self, corrected_spt_number: float, tol_settlement: float,
                 foundation_size: FoundationSize) -> None:
        """
        :param float corrected_spt_number: Statistical average of corrected SPT
            N-value (55% energy with overburden pressure correction) within the
            foundation influence zone i.e ``0.5B`` to ``2B``.
        :param float tol_settlement: Tolerable settlement of foundation.
        :param FoundationSize foundation_size: Size of foundation.
        """
        super().__init__(corrected_spt_number, tol_settlement, foundation_size)

    @round_
    def bearing_capacity(self):
        n_corr = self.corrected_spt_number
        f_w = self.foundation_size.width

        if f_w <= 1.2:
            return 19.16 * n_corr * self._fd() * self._sr()

        return (11.98 * n_corr * ((3.28 * f_w + 1) / (
                3.28 * f_w)) ** 2 * self._fd() * self._sr())


class BowlesABC4MatFoundation(BowlesABC4PadFoundation):
    r"""Allowable bearing capacity for mat foundation on cohesionless
    soils according to ``Bowles (1997)``.

    Notes
    -----
    Allowable bearing capacity for ``raft/mat`` foundations:

    .. math:: q_a(kPa) = 11.98(N_1)_{55}f_d\left(\dfrac{S}{25.4}\right)

    Depth factor:

    .. math:: f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33
    """

    @round_
    def bearing_capacity(self) -> float:
        n_corr = self.corrected_spt_number
        return 11.98 * n_corr * self._fd() * self._sr()


class MeyerhofABC4PadFoundation(AllowableBearingCapacity):
    r"""Allowable bearing capacity for pad foundation on cohesionless
    soils according to ``Meyerhof (1956)``.

    Notes
    -----
    Allowable bearing capacity for ``isolated/pad/spread`` foundations:

    .. math::

        q_a(kPa) &= 12N f_d\left(\dfrac{S}{25.4}\right), \ B \ \le 1.2m

        q_a(kPa) &= 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2 f_d\left(
                     \dfrac{S}{25.4}\right), \ B \ \gt 1.2m

    Depth factor:

    .. math:: f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33
    """

    def __init__(self, corrected_spt_number: float, tol_settlement: float,
                 foundation_size: FoundationSize):
        """
        :param float corrected_spt_number: Average uncorrected SPT N-value (60%
        energy with dilatancy (water) correction if applicable) within the
        foundation influence zone i.e :math:`D_f` to :math:`D_f + 2B`.
        :param float tol_settlement: Tolerable settlement of foundation.
        :param FoundationSize foundation_size: Size of foundation.
        """
        super().__init__(corrected_spt_number, tol_settlement, foundation_size)

    @round_
    def bearing_capacity(self):
        n_corr = self.corrected_spt_number
        f_w = self.foundation_size.width

        if f_w <= 1.2:
            return 12 * n_corr * self._fd() * self._sr()

        return (8 * n_corr * ((3.28 * f_w + 1) / (
                3.28 * f_w)) ** 2 * self._fd() * self._sr())


class MeyerhofABC4MatFoundation(MeyerhofABC4PadFoundation):
    r"""Allowable bearing capacity for mat foundation on cohesionless
    soils according to ``Meyerhof (1956)``.

    Notes
    -----
    Allowable bearing capacity for ``raft/mat`` foundations:

    .. math:: q_a(kPa) = 8 N f_d\left(\dfrac{S}{25.4}\right)

    Depth factor:

    .. math:: f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33
    """

    @round_
    def bearing_capacity(self):
        n_corr = self.corrected_spt_number
        return 8 * n_corr * self._fd() * self._sr()


class TerzaghiABC4PadFoundation(AllowableBearingCapacity):
    r"""Allowable bearing capacity for pad foundation on cohesionless
    soils according to ``Terzaghi & Peck (1948)``.

    Notes
    -----
    Allowable bearing capacity for ``isolated/pad/spread`` foundations:

    .. math::

        q_a(kPa) &= 12N \dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right),
                    \ B \ \le 1.2m

        q_a(kPa) &= 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2\dfrac{1}
                    {c_w f_d}\left(\dfrac{S}{25.4}\right), \ B \ \gt 1.2m

    Depth factor:

    .. math:: f_d = 1 + 0.25 \cdot \frac{D_f}{B} \le 1.25

    Water correction for surface footing:

    .. math:: c_w = 2 - \frac{D_w}{2B} \le 2

    Water correction for fully submerged footing :math:`D_w \le D_f`

    .. math:: c_w = 2 - \frac{D_f}{2B} \le 2
    """

    def __init__(self, corrected_spt_number: float, tol_settlement: float,
                 water_depth: float, foundation_size: FoundationSize) -> None:
        """
        :param float corrected_spt_number: Lowest (or average) uncorrected SPT
            N-value (60% energy) within the foundation influence zone i.e
            :math:`D_f` to :math:`D_f + 2B`
        :param float tol_settlement: Tolerable settlement of foundation.
        :param float water_depth: Depth of water below ground surface.
        :param FoundationSize foundation_size: Size of foundation.
        """
        super().__init__(corrected_spt_number, tol_settlement, foundation_size)
        self.water_depth = water_depth

    def _cw(self):
        f_d = self.foundation_size.depth
        f_w = self.foundation_size.width

        if self.water_depth <= f_d:
            cw = 2 - f_d / (2 * f_w)
        else:
            cw = 2 - self.water_depth / (2 * f_w)

        return min(cw, 2)

    @round_
    def bearing_capacity(self):
        n_corr = self.corrected_spt_number
        f_w = self.foundation_size.width

        if f_w <= 1.2:
            return 12 * n_corr * (1 / (self._cw() * self._fd())) * self._sr()

        return (8 * n_corr * ((3.28 * f_w + 1) / (3.28 * f_w)) ** 2 * (
                1 / (self._cw() * self._fd())) * self._sr())


class TerzaghiABC4MatFoundation(TerzaghiABC4PadFoundation):
    r"""Allowable bearing capacity for mat foundation on cohesionless soils
    according to ``Terzaghi & Peck (1948)``.

    Notes
    -----
    Allowable bearing capacity for ``isolated/pad/spread`` foundations:

    .. math:: q_a(kPa) = 8N\dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right)

    Depth factor:

    .. math:: f_d = 1 + 0.25 \cdot \frac{D_f}{B} \le 1.25

    Water correction for surface footing:

    .. math:: c_w = 2 - \frac{D_w}{2B} \le 2

    Water correction for fully submerged footing :math:`D_w \le D_f`

    .. math:: c_w = 2 - \frac{D_f}{2B} \le 2

    """

    @round_
    def bearing_capacity(self):
        n_corr = self.corrected_spt_number
        return 8 * n_corr * (1 / (self._cw() * self._fd())) * self._sr()
