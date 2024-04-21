from dataclasses import dataclass
from typing import Optional

from geolysis.constants import ERROR_TOL
from geolysis.constants import UnitRegistry as ureg
from geolysis.utils import arctan, isclose, round_

__all__ = [
    "SoilUnitWeightEst",
    "CompressionIndexEst",
    "SoilFrictionAngleEst",
    "UndrainedShearStrengthEst",
]


class EstimatorError(ValueError):
    pass


class SoilUnitWeightEst:
    r"""Estimates the ``moist``, ``saturated`` and ``submerged`` unit weight of
    soil sample from ``SPT N60``.

    Parameters
    ----------
    spt_n_60 : float
        SPT N-value standardized for field procedures considering 60% energy.

    Attributes
    ----------
    spt_n_60 : float

    Notes
    -----
    The following formulae below are used for estimating the ``moist``, ``saturated``,
    and ``submerged`` unit weight respectively.

    .. math::

        \gamma_{moist} &= 16.0 + 0.1 \cdot N_{60}

        \gamma_{sat} &= 16.8 + 0.15 \cdot N_{60}

        \gamma_{sub} &= 8.8 + 0.01 \cdot N_{60}

    Examples
    --------
    >>> from geolysis.estimators import SoilUnitWeightEst

    >>> suw_est = SoilUnitWeightEst(spt_n_60=15)
    >>> suw_est.moist_wgt()
    17.5
    >>> suw_est.saturated_wgt()
    19.05
    >>> suw_est.submerged_wgt()
    8.95
    """

    def __init__(self, spt_n_60) -> None:
        self.spt_n_60 = spt_n_60

    @round_
    def moist_wgt(self) -> float:
        """Return the ``moist unit weight`` for cohesionless soils.
        |rarr| :math:`kN/m^3`"""
        return 16.0 + 0.1 * self.spt_n_60

    @round_
    def saturated_wgt(self) -> float:
        """Return the ``saturated unit weight`` for cohesive soils.
        |rarr| :math:`kN/m^3`
        """
        return 16.8 + 0.15 * self.spt_n_60

    @round_
    def submerged_wgt(self) -> float:
        """Return the ``submerged unit weight`` for cohesionless soils.
        |rarr| :math:`kN/m^3`
        """
        return 8.8 + 0.01 * self.spt_n_60


class CompressionIndexEst:
    """Estimates the compression index of soil from ``liquid limit`` or ``void
    ratio``.

    The available estimators are ``Terzaghi et al (1967)``, ``Skempton (1994)``,
    and ``Hough (1957)``.

    Parameters
    ----------
    liquid_limit : float
        Water content beyond which soils flow under their own weight.
    void_ratio : Optional[float], default=None
        Ratio of the volume of voids to the volume of solids.

    Attributes
    ----------
    liquid_limit : float
    void_ratio : Optional[float]

    Notes
    -----
    .. note:: All values returned from methods in this class are unitless

    The formulae below are used for estimating the ``compression index`` of soil using
    ``Terzaghi et al``, ``Skempton``, and ``Hough`` relation respectively.

    .. math::

        C_i &= 0.009 (LL - 10)

        C_i &= 0.007 (LL - 10)

        C_i &= 0.29 (e_o - 0.27)

    Examples
    --------
    >>> from geolysis.estimators import CompressionIndexEst

    >>> comp_idx_est = CompressionIndexEst(liquid_limit=40)
    >>> comp_idx_est.terzaghi_et_al_ci_1967()
    0.27
    >>> comp_idx_est.skempton_ci_1994()
    0.21
    >>> comp_idx_est.hough_ci_1957()
    Traceback (most recent call last):
        ...
    EstimatorError: void_ratio cannot be None

    >>> comp_idx_est.void_ratio = 0.78
    >>> comp_idx_est.hough_ci_1957()
    0.148
    """

    def __init__(
        self, liquid_limit: float, void_ratio: Optional[float] = None
    ) -> None:
        self.liquid_limit = liquid_limit
        self.void_ratio = void_ratio

    @round_(ndigits=3)
    def terzaghi_et_al_ci_1967(self) -> float:
        """Return the compression index of soil from ``Terzaghi's`` correlation."""
        return 0.009 * (self.liquid_limit - 10.0)

    @round_(ndigits=3)
    def skempton_ci_1994(self) -> float:
        """Return the compression index of soil from ``Skempton's`` correlation."""
        return 0.007 * (self.liquid_limit - 10.0)

    @round_(ndigits=3)
    def hough_ci_1957(self) -> float:
        """Return the compression index of soil from ``Hough's`` correlation."""
        if self.void_ratio is not None:
            return 0.29 * (self.void_ratio - 0.27)

        err_msg = "void_ratio cannot be None"
        raise EstimatorError(err_msg)


class SoilFrictionAngleEst:
    r"""Estimates the internal angle of friction from ``SPT N60``.

    For cohesionless soils the coefficient of internal friction (:math:`\phi`)
    is determined from the minimum value between ``Wolff (1989)`` and
    ``Kullhawy & Mayne (1990)``.

    Parameters
    ----------
    spt_n_60 : float
        SPT N-value standardized for field procedures.
    eop : Optional[float], default=None, unit = :math:`kN/m^2`
        Effective overburden pressure, ``eop`` should be in the same unit as
        ``atm_pressure``.
    atm_pressure : Optional[float], default=None, unit = :math:`kN/m^2`
        Atmospheric pressure, ``atm_pressure`` should be in the same unit as ``eop``.

    Attributes
    ----------
    spt_n_60 : float
    eop : Optional[float]
    atm_pressure : Optional[float]

    Notes
    -----
    The formulae below are used for estimating the ``internal angle of friction`` of
    soil using ``Wolff``, and ``Kullhawy & Mayne`` relation respectively.

    .. math::

        \phi &= 27.1 + 0.3 \cdot N_{60} - 0.00054 \cdot (N_{60})^2

        \phi &= tan^{-1}\left[\left(\dfrac{N_{60}}{12.2 + 20.3 \cdot
                    \frac{\sigma_o}{P_a}}\right)^{0.34}\right]

    Examples
    --------
    >>> from geolysis.estimators import SoilFrictionAngleEst

    >>> sfa_est = SoilFrictionAngleEst(spt_n_60=15)
    >>> sfa_est.wolff_sfa_1989()
    31.48

    >>> sfa_est.kullhawy_mayne_sfa_1990()
    Traceback (most recent call last):
        ...
    EstimatorError: eop or atm_pressure cannot be None

    >>> sfa_est.eop = 103.8
    >>> sfa_est.atm_pressure = 101.3
    >>> sfa_est.kullhawy_mayne_sfa_1990()
    37.41

    >>> sfa_est.atm_pressure = 0.0
    >>> sfa_est.kullhawy_mayne_sfa_1990()
    Traceback (most recent call last):
        ...
    EstimatorError: atm_pressure cannot be close to zero (0)
    """

    def __init__(
        self,
        spt_n_60: float,
        eop: Optional[float] = None,
        atm_pressure: Optional[float] = None,
    ) -> None:
        self.spt_n_60 = spt_n_60
        self.eop = eop
        self.atm_pressure = atm_pressure

    @round_(ndigits=2)
    def wolff_sfa_1989(self) -> float:
        """Return the internal angle of friction from ``Wolff's`` correlation
        for granular soils. |rarr| degrees
        """
        return 27.1 + (0.3 * self.spt_n_60) - (0.00054 * (self.spt_n_60**2))

    @round_(ndigits=2)
    def kullhawy_mayne_sfa_1990(self) -> float:
        """Return the internal angle of friction from ``Kullhawy & Mayne``
        correlation for cohesionless soils. |rarr| degrees
        """
        if self.eop is None or self.atm_pressure is None:
            err_msg = "eop or atm_pressure cannot be None"
            raise EstimatorError(err_msg)

        if isclose(self.atm_pressure, 0, rel_tol=ERROR_TOL):
            err_msg = f"atm_pressure cannot be close to zero (0)"
            raise EstimatorError(err_msg)

        return arctan(
            (self.spt_n_60 / (12.2 + 20.3 * (self.eop / self.atm_pressure)))
            ** 0.34
        )


class UndrainedShearStrengthEst:
    r"""Undrained shear strength of soil estimators.

    The available estimators are ``Stroud (1974)`` and ``Skempton (1957)``.

    Parameters
    ----------
    spt_n_60 : float
        SPT N-value standardized for field procedures.
    k : float, default=3.5, unit = :math:`kN/m^2`
        Stroud constant. :math:`3.5 \le k \le 6.5`
    eop : Optional[float], default=None, unit = :math:`kN/m^2`
        Effective overburden pressure.
    plasticity_index : Optional[float], default=None
        Range of water content over which soil remains in plastic condition.

    Attributes
    ----------
    spt_n_60 : float
    k : float
    eop : float
    plasticity_index : float

    Raises
    ------
    EstimatorError
        If ``k`` is not in the specified range. :math:`3.5 \le k \le 6.5`

    Notes
    -----
    The formulae below are used for estimating the ``undrained shear strength`` of
    soil using ``Stroud``, and ``Skempton`` relation respectively.

    .. math::

        C_u &= k \cdot N_{60}

        C_u &= \sigma_o (0.11 + 0.0037 \cdot PI)

    The value of the ratio :math:`\frac{C_u}{\sigma_o}` determined in a consolidated-undrained
    test on undisturbed samples is generally greater than actual value because of anisotropic
    consolidation in the field. The actual value is best determined by ``in-situ shear vane test``.

    Examples
    --------
    >>> from geolysis.estimators import UndrainedShearStrengthEst

    >>> uss_est = UndrainedShearStrengthEst(spt_n_60=10)
    >>> uss_est.stroud_uss_1974()
    35.0
    >>> uss_est.k = 7
    >>> uss_est.stroud_uss_1974()
    Traceback (most recent call last):
        ...
    EstimatorError: k should be in the range 3.5 <= k <= 6.5

    >>> uss_est.skempton_uss_1957()
    Traceback (most recent call last):
        ...
    EstimatorError: eop and plasticity_index cannot be None

    >>> uss_est.eop = 76.8
    >>> uss_est.plasticity_index = 25.7
    >>> uss_est.skempton_uss_1957()
    15.75
    """

    def __init__(
        self,
        spt_n_60: float,
        k=3.5,
        eop: Optional[float] = None,
        plasticity_index: Optional[float] = None,
    ) -> None:
        self.spt_n_60 = spt_n_60
        self.k = k
        self.eop = eop
        self.plasticity_index = plasticity_index

    @round_(ndigits=2)
    def stroud_uss_1974(self) -> float:
        """Return the undrained shear strength using ``Stroud's`` correlation.
        |rarr| :math:`kN/m^2`
        """
        if 3.5 <= self.k <= 6.5:
            return self.k * self.spt_n_60

        err_msg = "k should be in the range 3.5 <= k <= 6.5"
        raise EstimatorError(err_msg)

    @round_(ndigits=2)
    def skempton_uss_1957(self) -> float:
        """Return the undrained shear strength using ``Skempton's`` correlation.
        |rarr| :math:`kN/m^2`
        """
        if self.eop is None or self.plasticity_index is None:
            err_msg = "eop and plasticity_index cannot be None"
            raise EstimatorError(err_msg)

        return self.eop * (0.11 + 0.0037 * self.plasticity_index)
