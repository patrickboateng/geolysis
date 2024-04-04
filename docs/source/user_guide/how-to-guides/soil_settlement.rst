***************
Soil Settlement
***************

CohesiveImmediateSettlement

.. math::

        S_i &= qB\left(\dfrac{1 - \mu^2}{E_s} \right) I

        I &= \frac{1}{\pi}\left[\ln(\frac{\sqrt{1 + m^2} + m}{\sqrt{1 + m^2} - m})
            + m \cdot \ln(\frac{\sqrt{1 + m^2} + 1}{\sqrt{1 + m^2} - 1})\right]

        m &= \frac{L}{B}

    .. list-table::
        :header-rows: 1

        * - Symbol
          - Name
          - Unit

        * - :math:`S_i`
          - Immediate settlement for cohesive soils
          - mm

        * - q
          - Uniformly distributed load
          - :math:`kN/m^2`

        * - B
          - Width of foundation footing
          - m

        * - L
          - Length of foundation footing
          - m

        * - :math:`\mu`
          - Poisson ratio
          - unitless

        * - :math:`E_s`
          - Elastic modulus
          - :math:`kN/m^2`

        * - I
          - Influence factor
          - unitless

    The equation above is applicable for footings located at the surface.
    For footings embedded in soil, the settlement would be less than the
    computed values. ``Fox (1948)`` gave correction curves. The settlement
    is obtained by multiplying the computed settlements by a depth factor
    which depends upon (:math:`\frac{D_f}{\sqrt{L \times B}}`) ratio.

CohesionlessImmediateSettlement

.. math::

        S_i &= C_1 C_2 (\overline{q} - q) \sum^{2B}_{z=0} \frac{I_z}{E_s}\Delta z

        C_1 &= 1 - 0.5\left(\frac{q}{\overline{q} - q}\right)

        C_2 &= 1 + 0.2 \log_{10}\left(\frac{time \ in \ years}{0.1}\right)

    .. list-table::
        :header-rows: 1

        * - Symbol
          - Name
          - Unit

        * - :math:`S_i`
          - Immediate settlement for cohesionless soils
          - mm

        * - :math:`C_1`
          - Correction factor for depth of foundation embedment
          - unitless

        * - :math:`C_2`
          - Correction factor for creep in soils
          - unitless

        * - :math:`\overline{q}`
          - Pressure at the foundation level
          - :math:`kN/m^2`

        * - q
          - Surcharge (:math:`\gamma D_f`)
          - :math:`kN/m^2`

        * - B
          - Width of foundation footing
          - m

        * - :math:`I_z`
          - Strain influence factor of soil
          - unitless

        * - :math:`E_s`
          - Elastic modulus
          - :math:`kN/m^2`

PrimaryConsolidationSettlement

    .. math::

        S_c = \frac{C_c H}{1 + e_o} \log \left(\frac{\sigma^{'}_o + \Delta \sigma}{\sigma^{'}_o}\right)

    .. list-table::
        :header-rows: 1

        * - Symbol
          - Name
          - Unit

        * - :math:`S_c`
          - Consolidation settlement
          - mm

        * - :math:`C_c`
          - Compression index
          - unitless

        * - H
          - Stratum thickness
          - m

        * - :math:`e_o`
          - Void ratio
          - unitless

        * - :math:`\sigma^{'}_o`
          - Effective overburden pressure
          - :math:`kN/m^2`

        * - :math:`\sigma`
          - Average pressure increase
          - :math:`kN/m^2`