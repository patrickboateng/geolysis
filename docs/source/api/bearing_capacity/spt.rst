.. currentmodule:: geolab.bearing_capacity.spt

Standard Penetration Test 
=========================

Energy Correction
-----------------

``SPT N-value`` corrected for field procedures given by ``Skempton (1986)``.

.. math::

    N_{60} = \dfrac{E_m \cdot C_B \cdot C_s \cdot C_R \cdot N}{0.6}

.. note::

    The ``energy correction`` is to be applied irrespective of the type of soil.

Overburden Pressure Correction
------------------------------

Skempton
++++++++

.. math::

    C_N = \dfrac{2}{1 + 0.01044\sigma_o}

Bazaraa and Peck (1969)
+++++++++++++++++++++++

This is a correction given by ``Bazaraa (1967)`` and also by ``Peck and Bazaraa (1969)``
and it is one of the commonly used corrections.

According to them:

.. math::

    N_c &= \dfrac{4N_R}{1 + 0.0418 \cdot \sigma_o}, \, \sigma_o \lt 71.8kN/m^2

    N_c &= \dfrac{4N_R}{3.25 + 0.0104 \cdot \sigma_o}, \, \sigma_o \gt 71.8kN/m^2

    N_c &= N_R \, , \, \sigma_o = 71.8kN/m^2

Gibbs and Holtz (1957)
++++++++++++++++++++++

It was only as late as in ``1957`` that ``Gibbs and Holtz`` suggested that corrections
should be made for field ``SPT`` values for depth. As the correction factor came to be
considered only after ``1957``, all empirical data published before ``1957`` like those
by ``Terzaghi`` is for uncorrected values of ``SPT``.

In granular soils, the overburden pressure affects the penetration resistance.
If two soils having same relative density but different confining pressures are tested,
the one with a higher confining pressure gives a higher penetration number. As the
confining pressure in cohesionless soils increases with the depth, the penetration number
for soils at shallow depths is underestimated and that at greater depths is overestimated.
For uniformity, the N-values obtained from field tests under different effective overburden
pressures are corrected to a standard effective overburden pressure.
``Gibbs and Holtz (1957)`` recommend the use of the following equation for dry or moist clean
sand. (:cite:author:`2003:arora`, p. 428)

.. math::

    N_c = \dfrac{350}{\sigma_o + 70} \cdot N_R \, , \, \sigma_o \le 280kN/m^2

.. note::

    :math:`\frac{N_c}{N_R}` should lie between 0.45 and 2.0, if :math:`\frac{N_c}{N_R}` is
    greater than 2.0, :math:`N_c` should be divided by 2.0 to obtain the design value used in
    finding the bearing capacity of the soil. (:cite:author:`2003:arora`, p. 428)
    

Peck, Hansen and Thornburn (1974)
+++++++++++++++++++++++++++++++++

.. math::

    (N_1)_{60} &= C_N \cdot N_{60} \le 2 \cdot N_{60}

    C_N &= 0.77\log\left(\frac{1905}{\sigma}\right)


:math:`C_N` = *overburden pressure coefficient factor*

Liao and Whitman (1986)
+++++++++++++++++++++++

.. math::

    C_N = \sqrt{\frac{100}{\sigma}}

Dilatancy Correction
--------------------

SPT N-value Dilatancy Correction.

**Dilatancy Correction** is a correction for silty fine sands and fine sands
below the water table that develop pore pressure which is not easily
dissipated. The pore pressure increases the resistance of the soil hence the
penetration number (N). (:cite:author:`2003:arora`)

Correction of silty fine sands recommended by ``Terzaghi and Peck (1967)`` if
:math:`N_{60}` exceeds 15.

.. math::

    N_c &= 15 + \frac{1}{2}\left(N_{60} - 15\right) \, , \, N_{60} \gt 15

    N_c &= N_{60} \, , \, N_{60} \le 15

.. References
.. ----------


