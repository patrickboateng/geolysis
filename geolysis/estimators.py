""" Provide implementations for common geotechnical engineering parameter 
estimators.
"""

from geolysis.utils import arctan, round_


class SoilUnitWeight:
    """Calculates the ``moist``, ``saturated`` and ``submerged`` unit weight
    of soil sample using
    :class:`SPT N60 <geolysis.bearing_capacity.spt.SPTCorrection.spt_n60>`.

    :param float spt_n_60:
        SPT N-value standardized for field procedures.
    """

    __slots__ = ("spt_n_60",)

    def __init__(self, spt_n_60: float):
        self.spt_n_60 = spt_n_60

    @property
    @round_(ndigits=2)
    def est_moist_wgt(self) -> float:
        """Return the moist unit weight for cohesionless soil."""
        return 16.0 + 0.1 * self.spt_n_60

    @property
    @round_(ndigits=2)
    def est_saturated_wgt(self) -> float:
        """Return the saturated unit weight for cohesive soil."""
        return 16.8 + 0.15 * self.spt_n_60

    @property
    @round_(ndigits=2)
    def est_submerged_wgt(self) -> float:
        """Return the submerged unit weight of cohesionless soil."""
        return 8.8 + 0.01 * self.spt_n_60


class CompressionIndexEst:
    """The compression index of soil estimated from ``liquid limit`` or
    ``void ratio``.

    The available correlations used are  :meth:`SKEMPTON (1994) <.skempton_1994>`,
    :meth:`TERZAGHI ET AL (1967) <.terzaghi_et_al_1967>`,
    :meth:`HOUGH (1957) <.hough_1957>`.
    """

    @staticmethod
    @round_(ndigits=3)
    def terzaghi_et_al_1967(liquid_limit: float) -> float:
        """Return the compression index of the soil using ``Terzaghi's``
        correlation.

        :param float liquid_limit:
            Water content beyond which soils flow under their own weight (%)
        """
        return 0.009 * (liquid_limit - 10)

    @staticmethod
    @round_(ndigits=3)
    def skempton_1994(liquid_limit: float) -> float:
        """Return the compression index of the soil using ``Skempton's``
        correlation.

        :param float liquid_limit:
            Water content beyond which soils flows under their own weight (%)
        """
        return 0.007 * (liquid_limit - 10.0)

    @staticmethod
    @round_(ndigits=3)
    def hough_1957(void_ratio: float) -> float:
        """Return the compression index of the soil using ``Hough's``
        correlation.

        :param float void_ratio:
            Ratio of the volume of voids to the volume of solids (unitless)
        """
        return 0.29 * (void_ratio - 0.27)


class SoilFrictionAngleEst:
    r"""Estimation of the internal angle of friction using ``SPT N60``.

    For cohesionless soils the coefficient of internal friction (:math:`\phi`)
    was determined from the minimum value from :meth:`WOLFF (1989) <.wolff_1989>`
    and :meth:`KULLHAWY & MAYNE (1990) <.kullhawy_mayne_1990>`.
    """

    @staticmethod
    @round_(ndigits=3)
    def wolff_1989(spt_n_60: float) -> float:
        """Return the internal angle of friction using ``Wolff's`` correlation
        for granular soils (degrees).

        :param float spt_n_60:
            SPT N-value standardized for field procedures.
        """
        return 27.1 + (0.3 * spt_n_60) - (0.00054 * (spt_n_60**2))

    @staticmethod
    @round_(ndigits=3)
    def kullhawy_mayne_1990(
        spt_n_60: float,
        eop: float,
        atm_pressure: float,
    ) -> float:
        """Return the internal angle of friction using ``Kullhawy & Mayne``
        correlation for cohesionless soils (degrees).

        :param float spt_n_60:
            SPT N-value standardized for field procedures.
        :param float eop:
            Effective overburden pressure (:math:`kN/m^2`), defaults to 0
        :param float atm_pressure:
            Atmospheric pressure (:math:`kN/m^2`), defaults to 0

        .. note::

            Effective overburden pressure and atmospheric pressure should all
            be in the same unit.
        """
        return arctan(
            (spt_n_60 / (12.2 + 20.3 * (eop / atm_pressure))) ** 0.34
        )


class UndrainedShearStrengthEst:
    """Estimations of undrained shear strength of soil.

    The available correlations used are :meth:`STROUD (1974) <.stroud_1974>`
    and :meth:`SKEMPTON (1957) <.skempton_1957>`.
    """

    @staticmethod
    @round_(ndigits=3)
    def stroud_1974(spt_n_60: float, k=3.5):
        """Return the undrained shear strength using ``Stroud's`` correlation.

        :param float spt_n60:
            SPT N-value standardized for field procedures.
        :param float k:
            stroud parameter, defaults to 3.5

        :raises ValueError: If ``k`` is not in the specified range.
        """
        if 3.5 <= k <= 6.5:
            return k * spt_n_60

        msg = f"k should be in the range 3.5 <= k <= 6.5 not {k}"
        raise ValueError(msg)

    @staticmethod
    @round_(ndigits=3)
    def skempton_1957(eop: float, plasticity_index: float):
        """Return the undrained shear strength using ``Skempton's``
        correlation.

        :param float eop:
            Effective overburden pressure :math:`kN/m^2`, defaults to 0
        :param float plasticity_index:
            Range of water content over which soil remains in plastic condition,
            defaults to 0
        """
        return eop * (0.11 + 0.0037 * plasticity_index)
