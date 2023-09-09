Ultimate Bearing Capacity
=========================

Terzaghi Bearing Capacity
-------------------------

Ultimate bearing capacity for ``strip``, ``square`` and ``circular`` foundation
respectively.

.. math:: 

    q_u &= c \cdot N_c + \gamma \cdot D_f \cdot N_q + 0.5 \cdot \gamma \cdot B \cdot N_\gamma

    q_u &= 1.2 \cdot c \cdot N_c + \gamma \cdot D_f \cdot N_q + 0.4 \cdot \gamma \cdot B \cdot N_\gamma

    q_u &= 1.2 \cdot c \cdot N_c + \gamma \cdot D_f \cdot N_q + 0.3 \cdot \gamma \cdot B \cdot N_\gamma


Bearing Capacity Factors
++++++++++++++++++++++++

.. math:: 

    N_c &= \cot \phi \left(N_q - 1 \right)

    N_q &= \dfrac{e^{(\frac{3\pi}{2}-\phi)\tan\phi}}{2\cos^2\left(45^{\circ}+\frac{\phi}{2}\right)}

.. note::

    Exact values of :math:`N_\gamma` are not directly obtainable; values have
    been proposed by ``Brinch Hansen (1968)`` which are widely used in Europe,
    and also by ``Meyerhof (1963)``, which have been adopted in North America.

The formulas shown below are ``Brinch Hansen`` and ``Meyerhof`` respectively.

.. math:: 

    N_\gamma &= 1.8 \left(N_q - 1 \right) \tan \phi

    N_\gamma &= \left(N_q -1 \right)\tan(1.4\phi)


Hansen Bearing Capacity
-----------------------

.. math:: 

    q_u = c \cdot N_c \cdot s_c \cdot d_c \cdot i_c \,
    + q \cdot N_q \cdot s_q \cdot d_q \cdot i_q \, 
    + 0.5 \cdot \gamma \cdot B \cdot N_\gamma \cdot s_\gamma \cdot d_\gamma \cdot i_\gamma

Bearing Capacity Factors
++++++++++++++++++++++++

.. math:: 

    N_c &= (N_q - 1) \cot \phi

    N_q &= \tan^2 \left(45 + \frac{\phi}{2} \right)\left(e^{\pi \tan \phi}\right)

    N_\gamma &= 1.8(N_q - 1) \tan \phi

Depth Factors
+++++++++++++

.. math:: 

    d_c &= 1 + 0.35 \left(\frac{D_f}{B}\right)

    d_q &= 1 + 0.35 \left(\frac{D_f}{B}\right)

    d_\gamma &= 1.0

Shape Factors
+++++++++++++

- if footing shape is continuous(strip)

  * :math:`\displaystyle s_c = 1`

  * :math:`\displaystyle s_q = 1`

  * :math:`\displaystyle s_\gamma = 1`

- if footing shape is rectangular 

  * :math:`\displaystyle s_c = 1 + 0.2 \left(\dfrac{B}{L}\right)`

  * :math:`\displaystyle s_q = 1 + 0.2 \left(\dfrac{B}{L}\right)`

  * :math:`\displaystyle s_\gamma = 1 - 0.4 \left(\dfrac{B}{L}\right)`

- if footing shape is square 

  * :math:`\displaystyle s_c = 1.3`

  * :math:`\displaystyle s_q = 1.2`

  * :math:`\displaystyle s_\gamma = 0.8`

- if footing shape is circular

  * :math:`\displaystyle s_c = 1.3`

  * :math:`\displaystyle s_q = 1.2`

  * :math:`\displaystyle s_\gamma = 0.6`


Inclination Factors
+++++++++++++++++++

.. math:: 

    i_c &= 1 - \left(\dfrac{\beta}{2cBL}\right)

    i_q &= 1 - 1.5 \cdot \dfrac{\beta}{V}

    i_\gamma &= \left(1 - 1.5 \cdot \dfrac{\beta}{V} \right)^2

Vesic Bearing Capacity
----------------------

.. math:: 

    q_u = c \cdot N_c \cdot s_c \cdot d_c \cdot i_c \,
    + q \cdot N_q \cdot s_q \cdot d_q \cdot i_q \, 
    + 0.5 \cdot \gamma \cdot B \cdot N_\gamma \cdot s_\gamma \cdot d_\gamma \cdot i_\gamma


Bearing Capacity Factors
++++++++++++++++++++++++

.. math:: 

    N_c &= (N_q - 1) \cdot \cot \phi

    N_q &= \tan^2 \left(45 + \frac{\phi}{2} \right) \cdot (e^{\pi \tan \phi})

    N_\gamma &= 2 \cdot (N_q + 1) \cdot \tan \phi`

Depth Factors
+++++++++++++

.. math:: 

    d_c &= 1 + 0.4 \cdot \left(\frac{D_f}{B} \right)

    d_q &= 1 + 2 \cdot \tan \phi \cdot (1 - \sin \phi)^2 \cdot \dfrac{D_f}{B}

    d_\gamma &= 1.0`

Shape Factors
+++++++++++++

- if footing shape is continuous(strip):

  * :math:`\displaystyle s_c = 1`

  * :math:`\displaystyle s_q = 1`

  * :math:`\displaystyle s_\gamma = 1`

- if footing shape is rectangular:

  * :math:`\displaystyle s_c = 1 + \dfrac{B}{L} \cdot \dfrac{N_q}{N_c}`

  * :math:`\displaystyle s_q = 1 + \dfrac{B}{L} \cdot \tan \phi`

  * :math:`\displaystyle s_\gamma = 1 - 0.4 \cdot \dfrac{B}{L}`

- if footing shape is square or circular:

  * :math:`\displaystyle s_c = 1 + \dfrac{N_q}{N_c}`

  * :math:`\displaystyle s_q = 1 + \tan \phi`

  * :math:`\displaystyle s_\gamma = 0.6`

Inclination Factors
+++++++++++++++++++

.. math:: 

    i_c = \left(1 - \frac{\beta}{90} \right)^2

    i_q = \left(1 - \frac{\beta}{90} \right)^2

    i_\gamma = \left(1 - \dfrac{\beta}{\phi} \right)^2


