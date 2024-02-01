from geolysis.constants import ERROR_TOL, UNITS
from geolysis.utils import arctan, isclose, round_


class EstimatorError(ValueError):
    """
    ValueError for estimators.
    """


class SoilUnitWeightEst:
    """
    Calculates the ``moist``, ``saturated`` and ``submerged`` unit weight of soil
    sample using ``SPT N60``.

    :param float spt_n_60: SPT N-value standardized for field procedures considering
        60% energy.
    """

    unit = UNITS.kilo_newton_per_cubic_metre

    def __init__(self, spt_n_60: float):
        self.spt_n_60 = spt_n_60

    @property
    @round_(ndigits=2)
    def moist_wgt(self) -> float:
        r"""
        Return the moist unit weight for cohesionless soil. (:math:`kN/m^3`)

        .. math::

            \gamma_{moist} = 16.0 + 0.1 \cdot N_{60}
        """
        return 16.0 + 0.1 * self.spt_n_60

    @property
    @round_(ndigits=2)
    def saturated_wgt(self) -> float:
        r"""
        Return the saturated unit weight for cohesive soil. (:math:`kN/m^3`)

        .. math::

            \gamma_{sat} = 16.8 + 0.15 \cdot N_{60}
        """
        return 16.8 + 0.15 * self.spt_n_60

    @property
    @round_(ndigits=2)
    def submerged_wgt(self) -> float:
        r"""
        Return the submerged unit weight of cohesionless soil. (:math:`kN/m^3`)

        .. math::

            \gamma_{sub} = 8.8 + 0.01 \cdot N_{60}
        """
        return 8.8 + 0.01 * self.spt_n_60


class CompressionIndexEst:
    """
    The compression index of soil estimated from ``liquid limit`` or ``void
    ratio``.

    The available estimators are ``Terzaghi et al (1967)``, ``Skempton (1994)``,
    and Hough (1957).
    """

    unit = UNITS.unitless

    @staticmethod
    @round_(ndigits=3)
    def terzaghi_et_al_ci_1967(liquid_limit: float) -> float:
        """
        Return the compression index of the soil using ``Terzaghi's``
        correlation.

        :param float liquid_limit: Water content beyond which soils flow under their
            own weight. (%)

        .. math::

            C_i = 0.009 (LL - 10)
        """
        return 0.009 * (liquid_limit - 10.0)

    @staticmethod
    @round_(ndigits=3)
    def skempton_ci_1994(liquid_limit: float) -> float:
        """
        Return the compression index of the soil using ``Skempton's``
        correlation.

        :param float liquid_limit: Water content beyond which soils flows under their
            own weight. (%)

        .. math::

            C_i = 0.007 (LL - 10)
        """
        return 0.007 * (liquid_limit - 10.0)

    @staticmethod
    @round_(ndigits=3)
    def hough_ci_1957(void_ratio: float) -> float:
        """
        Return the compression index of the soil using ``Hough's`` correlation.

        :param float void_ratio: Ratio of the volume of voids to the volume of solids.

        .. math::

            C_i = 0.29 (e_o - 0.27)
        """
        return 0.29 * (void_ratio - 0.27)


class SoilFrictionAngleEst:
    r"""
    Estimation of the internal angle of friction using ``SPT N60``.

    For cohesionless soils the coefficient of internal friction (:math:`\phi`) is
    determined from the minimum value between ``Wolf (1989)`` and ``Kullhawy & Mayne (1990)``.
    """

    unit = UNITS.degrees

    @staticmethod
    @round_(ndigits=3)
    def wolff_sfa_1989(spt_n_60: float) -> float:
        r"""
        Return the internal angle of friction using ``Wolff's`` correlation for
        granular soils (degrees).

        :param float spt_n_60: SPT N-value standardized for field procedures considering
            60% energy.

        .. math::

            \phi = 27.1 + 0.3 \cdot N_{60} - 0.00054 \cdot (N_{60})^2
        """
        return 27.1 + (0.3 * spt_n_60) - (0.00054 * (spt_n_60**2))

    @staticmethod
    @round_(ndigits=3)
    def kullhawy_mayne_sfa_1990(
        spt_n_60: float,
        eop: float,
        atm_pressure: float,
    ) -> float:
        r"""
        Return the internal angle of friction using ``Kullhawy & Mayne``
        correlation for cohesionless soils (degrees).

        :param float spt_n_60: SPT N-value standardized for field procedures.
        :param float eop: Effective overburden pressure, should be in the same unit as
            ``atm_pressure``.
        :param float atm_pressure: Atmospheric pressure, should be in the same unit as
            ``eop``.

        .. math::

            \phi = \left[tan^{-1}\left(\dfrac{N_{60}}{12.2 + 20.3 \cdot
                    \frac{\sigma_o}{P_a}}\right)\right]^{0.34}
        """
        if isclose(atm_pressure, 0, rel_tol=ERROR_TOL):
            err_msg = f"atm_pressure cannot be {atm_pressure}"
            raise EstimatorError(err_msg)

        return arctan(
            (spt_n_60 / (12.2 + 20.3 * (eop / atm_pressure))) ** 0.34
        )


class UndrainedShearStrengthEst:
    """
    Undrained shear strength of soil estimators.

    The available estimators are ``Stroud (1974)`` and ``Skempton (1957)``.
    """

    unit = UNITS.kilo_pascal

    @staticmethod
    @round_(ndigits=3)
    def stroud_uss_1974(spt_n_60: float, k=3.5):
        r"""
        Return the undrained shear strength using ``Stroud's`` correlation.

        :param float spt_n_60: SPT N-value standardized for field procedures.
        :param float k: stroud constants, :math:`3.5 \le k \le 6.5`. defaults to 3.5

        :raises EstimatorError: If ``k`` is not in the specified range.

        .. math::

            C_u = k \cdot N_{60}
        """
        if 3.5 <= k <= 6.5:
            return k * spt_n_60

        err_msg = f"k should be in the range 3.5 <= k <= 6.5 not {k}"
        raise EstimatorError(err_msg)

    @staticmethod
    @round_(ndigits=3)
    def skempton_uss_1957(eop: float, plasticity_index: float):
        r"""
        Return the undrained shear strength using ``Skempton's`` correlation.

        :param float eop: Effective overburden pressure. (:math:`kN/m^2`)
        :param float plasticity_index: Range of water content over which soil remains in
            plastic condition.

        .. math::

            C_u = \sigma_o (0.11 + 0.0037 \cdot PI)

        .. note::

            The value of the ratio :math:`\frac{C_u}{\sigma_o}` determined in a
            consolidated-undrained test on undisturbed samples is generally greater than
            actual value because of anisotropic consolidation in the field. The actual
            value is best determined by ``in-situ shear vane test``.
        """
        return eop * (0.11 + 0.0037 * plasticity_index)
