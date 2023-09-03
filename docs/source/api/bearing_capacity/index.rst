Bearing Capacity Analysis
=========================

Terzaghi Bearing Capacity
-------------------------

Strip Footing
+++++++++++++

:math:`\displaystyle q_u = c \, N_c + \gamma \, D_f \, N_q + 0.5 \, \gamma \, B \, N_\gamma`

Square Footing
++++++++++++++

:math:`\displaystyle q_u = 1.2 \, c \, N_c + \gamma \, D_f \, N_q + 0.4 \, \gamma \, B \, N_\gamma`

Circular Footing
++++++++++++++++

:math:`\displaystyle q_u = 1.2 \, c \, N_c + \gamma \, D_f \, N_q + 0.3 \, \gamma \, B \, N_\gamma`

Bearing Capacity Factors
++++++++++++++++++++++++

N_c
^^^

:math:`\displaystyle N_c = \cot \phi \left(N_q - 1 \right)`

N_q
^^^

:math:`\displaystyle N_q = \dfrac{e^{(\frac{3\pi}{2}-\phi)\tan\phi}}{2\cos^2\left(45^{\circ}+\frac{\phi}{2}\right)}`

N_gamma
^^^^^^^

.. note::

    Exact values of :math:`N_\gamma` are not directly obtainable; values have
    been proposed by ``Brinch Hansen (1968)`` which are widely used in Europe,
    and also by ``Meyerhof (1963)``, which have been adopted in North America.

The formulas shown below are ``Brinch Hansen`` and ``Meyerhof`` respectively.

:math:`\displaystyle N_\gamma = 1.8 \left(N_q - 1 \right) \tan \phi`

:math:`\displaystyle N_\gamma = \left(N_q -1 \right)\tan(1.4\phi)`

Meyerhof Bearing Capacity
-------------------------

if B :math:`\le 1.22`:

:math:`\displaystyle q_{a(net)} = 19.16 N_{des} D_f \frac{S_e}{25.4}`

if B :math:`\gt 1.22`:

:math:`\displaystyle q_{a(net)} = 11.98 N_{des} \left(\frac{3.28B + 1}{3.28B} \right)^2 D_f \frac{S_e}{25.4}`

Depth Factor
++++++++++++

:math:`\displaystyle k = 1 + 0.33 \frac{D_f}{B}`

Hansen Bearing Capacity
-----------------------

:math:`\displaystyle q_u = c \, N_c \, s_c \, d_c \, i_c + q \, N_q \, s_q \, d_q \, i_q \, + 0.5 \, \gamma \, B \, N_\gamma \, s_\gamma \, d_\gamma \, i_\gamma`

Bearing Capacity Factors
++++++++++++++++++++++++

N_c
^^^

:math:`\displaystyle N_c = (N_q - 1) \cot \phi`

N_q
^^^

:math:`\displaystyle N_q = \tan^2 \left(45 + \frac{\phi}{2} \right)\left(e^{\pi \tan \phi}\right)`

N_gamma
^^^^^^^

:math:`\displaystyle N_\gamma = 1.8(N_q - 1) \tan \phi`

Depth Factors
+++++++++++++

d_c 
^^^

:math:`\displaystyle d_c = 1 + 0.35 \left(\frac{D_f}{B}\right)`

d_q 
^^^

:math:`\displaystyle d_q = 1 + 0.35 \left(\frac{D_f}{B}\right)`

d_gamma
^^^^^^^

:math:`\displaystyle d_\gamma = 1.0`

Shape Factors
+++++++++++++

s_c
^^^

if footing shape is continuous(strip): 

:math:`\displaystyle s_c = 1` 

if footing shape is rectangular:

:math:`\displaystyle s_c = 1 + 0.2 \frac{B}{L}`

if footing shape is square:

:math:`\displaystyle s_c = 1.3`

if footing shape is circular:

:math:`\displaystyle s_c = 1.3`

s_q
^^^

if footing shape is continuous(strip):

:math:`\displaystyle s_q = 1`

if footing shape is rectangular:

:math:`\displaystyle s_q = 1 + 0.2 \frac{B}{L}`

if footing shape is square:

:math:`\displaystyle s_q = 1.2`

if footing shape is circular:

:math:`\displaystyle s_q = 1.2`

s_gamma
^^^^^^^^

if footing shape is continuous(strip):

:math:`s_\gamma = 1`

if footing shape is rectangular:

:math:`\displaystyle s_\gamma = 1 - 0.4 \frac{B}{L}`

if footing shape is square:

:math:`\displaystyle s_\gamma = 0.8`

if footing shape is circular:

:math:`\displaystyle s_\gamma = 0.6`

Inclination Factors
+++++++++++++++++++

i_c
^^^

:math:`displaystyle i_c = 1 - \frac{\beta}{2cBL}`

i_q
^^^

:math:`\displaystyle i_q = 1 - 1.5 \times \frac{\beta}{V}`

i_gamma
^^^^^^^

:math:`\displaystyle i_\gamma = \left(1 - 1.5 \times \frac{\beta}{V} \right)^2`

Vesic Bearing Capacity
----------------------

:math:`\displaystyle q_u = c \, N_c \, s_c \, d_c \, i_c + q \, N_q \, s_q \, d_q \, i_q \, + 0.5 \, \gamma \, B \, N_\gamma \, s_\gamma \, d_\gamma \, i_\gamma`

Bearing Capacity Factors
++++++++++++++++++++++++

N_c
^^^

:math:`\displaystyle N_c = (N_q - 1) \cdot \cot \phi`

N_q
^^^

:math:`\displaystyle N_q = \tan^2 \left(45 + \frac{\phi}{2} \right) \cdot (e^{\pi \tan \phi})`

N_gamma
^^^^^^^

:math:`\displaystyle N_\gamma = 2 \cdot (N_q + 1) \cdot \tan \phi`

Depth Factors
+++++++++++++

d_c
^^^
    
:math:`\displaystyle d_c = 1 + 0.4 \cdot \left(\frac{D_f}{B} \right)`

d_q
^^^

:math:`\displaystyle d_q = 1 + 2 \cdot \tan \phi \cdot (1 - \sin \phi)^2 \cdot \dfrac{D_f}{B}`

d_gamma
^^^^^^^

:math:`\displaystyle d_\gamma = 1.0`

Shape Factors
+++++++++++++

s_c
^^^

if footing shape is continuous(strip):

:math:`s_c = 1`

if footing shape is rectangular:

:math:`s_c = 1 + \dfrac{B}{L} \cdot \dfrac{N_q}{N_c}`

if footing shape is square or circular:

:math:`s_c = 1 + \left(\dfrac{N_q}{N_c} \right)`

s_q
^^^

if footing shape is continuous(strip):

:math:`s_q = 1`

if  footing  shape  is  rectangular:

:math:`s_q = 1 + \dfrac{B}{L} \cdot \tan \phi`

if footing shape is square or circular:

:math:`s_c = 1 + \tan \phi`

s_gamma
^^^^^^^

if footing shape is continuous(strip):

:math:`s_\gamma = 1`

if footing shape is rectangular:

:math:`s_\gamma = 1 - 0.4 \cdot \dfrac{B}{L}`

if  footing  shape  is  square  or  circular:

:math:`s_\gamma = 0.6`

Inclination Factors
+++++++++++++++++++

i_c
^^^
    
:math:`\displaystyle i_c = \left(1 - \frac{\beta}{90} \right)^2`

i_q
^^^

:math:`\displaystyle i_q = \left(1 - \frac{\beta}{90} \right)^2`

i_gamma
^^^^^^^

:math:`i_\gamma = \left(1 - \dfrac{\beta}{\phi} \right)^2`


Standard Penetration Test 
-------------------------

Overburden Pressure Correction
++++++++++++++++++++++++++++++

Skempton
^^^^^^^^

SPT N-value corrected for field procedures according to ``Skempton (1986)``.

.. note::

    This correction is to be applied irrespective of the type of soil.

.. math::

    N_{60} &= \dfrac{E_m \times C_B \times C_s \times C_R \times N_r}{0.6}

    C_N &= \dfrac{2}{1 + 0.01044\sigma_o}

Bazaraa and Peck (1969)
^^^^^^^^^^^^^^^^^^^^^^^

This is a correction given by ``Bazaraa (1967)`` and also by ``Peck and Bazaraa (1969)``
and it is one of the commonly used corrections.

According to them:

.. math::

    N_c &= \dfrac{4N_R}{1 + 0.0418 \cdot \sigma_o}, \, \sigma_o \lt 71.8kN/m^2

    N_c &= \dfrac{4N_R}{3.25 + 0.0104 \cdot \sigma_o}, \, \sigma_o \gt 71.8kN/m^2

    N_c &= N_R \, , \, \sigma_o = 71.8kN/m^2

Gibbs and Holtz (1957)
^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. math::

    (N_1)_{60} &= C_N \cdot N_{60} \le 2 \cdot N_{60}

    C_N &= 0.77\log\left(\frac{1905}{\sigma}\right)


:math:`C_N` = *overburden pressure coefficient factor*

Liao and Whitman (1986)
^^^^^^^^^^^^^^^^^^^^^^^

.. math::

    C_N = \sqrt{\frac{100}{\sigma}}

Dilatancy Correction
++++++++++++++++++++

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

References
++++++++++

.. bibliography::