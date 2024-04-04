*************************************
How to estimate soil bearing capacity
*************************************

Importing objects
=================

.. code:: python

    >>> from geolysis.bearing_capacity.abc import (
    ...      BowlesABC1997,
    ...      MeyerhofABC1956,
    ...      TerzaghiABC1948,
    ... )
    >>> from geolysis.foundation import FoundationSize, SquareFooting

Allowable Bearing Capacity
==========================

Computing allowable bearing capacity using relations from
``Bowles (1997)``, ``Meyerhof (1956)``, and ``Terzaghi (1948)``
respectively ::

    >>> fs = FoundationSize(depth=1.5, footing_shape=SquareFooting(width=1.2))
    >>> bowles_abc = BowlesABC1997(avg_corrected_spt_val=11.0,
    ...                            tol_settlement=20.0,
    ...                            foundation_size=fs)
    >>> bowles_abc.abc_cohl_4_isolated_foundation()
    220.72
    >>> meyerhof_abc = MeyerhofABC1956(avg_uncorrected_spt_val=11.0, 
    ...                                tol_settlement=20.0,
    ...                                foundation_size=fs)
    >>> meyerhof_abc.abc_cohl_4_isolated_foundation()
    138.24
    >>> terzaghi_abc = TerzaghiABC1948(lowest_uncorrected_spt_val=11, 
    ...                                tol_settlement=20,
    ...                                water_depth=1.2, foundation_size=fs)
    >>> terzaghi_abc.abc_cohl_4_isolated_foundation()
    60.47

Bowles

.. math::

            f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33

        .. list-table::

            * - :math:`D_f`
              - Depth of foundation. (m)

            * - B
              - Width of foundation footing. (m)

for B :math:`\le` 1.2m:

        .. math::

            q_a(kPa) = 19.16(N_1)_{55} f_d\left(\dfrac{S}{25.4}\right)

        for B :math:`\gt` 1.2m:

        .. math::

            q_a(kPa) = 11.8(N_1)_{55}\left(\dfrac{3.28B + 1}{3.28B} \right)^2 f_d
            \left(\dfrac{S}{25.4}\right)

        .. list-table::

            * - :math:`(N_1)_{55}`
              - Statistical average of corrected SPT N-value within the foundation
                influence zone.

            * - B
              - Width of foundation footing. (m)

            * - :math:`f_d`
              - Depth factor

            * - S
              - Tolerable settlement. (mm)

.. math::

            q_a(kPa) = 11.98(N_1)_{55}f_d\left(\dfrac{S}{25.4}\right)

        .. list-table::

            * - :math:`(N_1)_{55}`
              - Statistical average of corrected SPT N-value within the foundation
                influence zone.

            * - :math:`f_d`
              - Depth factor

            * - S
              - Tolerable settlement. (mm)

Meyerhof

.. math::

            f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33

        .. list-table::

            * - :math:`D_f`
              - Depth of foundation. (m)

            * - B
              - Width of foundation footing. (m)

for B :math:`\le` 1.2m:

        .. math::

            q_a(kPa) = 12N f_d\left(\dfrac{S}{25.4}\right)

        for B :math:`\gt` 1.2m:

        .. math::

            q_a(kPa) = 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2 f_d\left(\dfrac{S}{25.4}\right)

        .. list-table::

            * - :math:`(N_1)_{55}`
              - Average uncorrected SPT N-value within the foundation influence zone.

            * - B
              - Width of foundation footing. (m)

            * - :math:`f_d`
              - Depth factor

            * - S
              - Tolerable settlement. (mm)

.. math::

            q_a(kPa) = 8 N f_d\left(\dfrac{S}{25.4}\right)

        .. list-table::

            * - :math:`(N_1)_{55}`
              - Statistical average of corrected SPT N-value within the foundation
                influence zone.

            * - :math:`f_d`
              - Depth factor

            * - S
              - Tolerable settlement. (mm)

Terzaghi 

.. math::

            f_d = 1 + 0.25 \cdot \frac{D_f}{B} \le 1.25

        .. list-table::

            * - :math:`D_f`
              - Depth of foundation. (m)

            * - B
              - Width of foundation footing. (m)

for surface footing:

        .. math::

            c_w = 2 - \frac{D_w}{2B} \le 2

        for fully submerged footing :math:`D_w \le D_f`

        .. math::

            c_w = 2 - \frac{D_f}{2B} \le 2

        .. list-table::

            * - :math:`D_w`
              - Depth of water. (m)

            * - :math:`D_f`
              - Depth of foundation. (m)

            * - B
              - Width of foundation footing. (m)

for B :math:`\le` 1.2m:

        .. math::

            q_a(kPa) = 12N \dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right)

        for B :math:`\gt` 1.2m:

        .. math::

            q_a(kPa) = 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2\dfrac{1}{c_w f_d}
                       \left(\dfrac{S}{25.4}\right)

        .. list-table::

            * - N
              - Lowest (or average) uncorrected SPT N-values within the foundation
                influence zone.

            * - B
              - Width of foundation footing. (m)

            * - :math:`c_w`
              - Water correction factor.

            * - :math:`f_d`
              - Depth factor

            * - S
              - Tolerable settlement. (mm)

.. math::

            q_a(kPa) = 8N\dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right)

        .. list-table::

            * - N
              - Lowest (or average) uncorrected SPT N-values within the foundation
                influence zone.

            * - :math:`c_w`
              - Water correction factor.

            * - :math:`f_d`
              - Depth factor

            * - S
              - Tolerable settlement. (mm)