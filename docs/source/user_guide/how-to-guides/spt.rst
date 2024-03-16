***************************
How to analyze SPT N-values
***************************

Importing objects
=================

.. code:: python

    from geolysis.spt import weighted_avg_spt_n_val, avg_uncorrected_spt_n_val, SPTCorrections

Weighted Average SPT N-value
============================

Due to uncertainty in field procedure in standard penetration test and also
to consider all the N-value in the influence zone of a foundation, a method
was suggested to calculate the design N-value which should be used in
calculating the allowable bearing capacity of shallow foundation rather than
using a particular N-value. All the N-value from the influence zone is taken
under consideration by giving the highest weightage to the closest N-value
from the base.

The determination of :math:`N_{design}` is given by:

.. math::

    N_{design} = \dfrac{\sum_{i=1}^{n} \frac{N_i}{i^2}}{\sum_{i=1}^{n} \frac{1}{i^2}}

- influence zone = :math:`D_f + 2B` or to a depth up to which soil
  types are approximately the same.
- B = width of footing
- :math:`n` = number of layers in the influence zone.
- :math:`N_i` = corrected N-value at ith layer from the footing base.

The **Weighted Average SPT N-value** is the same as the SPT :math:`N_{design}`

SPT :math:`N_{design}` can be computed as follows: ::

    >>> corrected_spt_vals = [7.0, 15.0, 18.0]
    >>> weighted_avg_spt_n_val(corrected_spt_vals)
    9.0

Average SPT N-value
===================

This is simply the mean of all uncorrected SPT N-values within the 
foundation influence zone i.e. :math:`D_f \rightarrow D_f + 2B`.
Only water table correction suggested. 

Average SPT N-value can be computed as follows: ::

    >>> uncorrected_spt_vals = [8.0, 10.0, 14.0] # Note: water table correction may be applied
    >>> avg_uncorrected_spt_n_val(uncorrected_spt_vals)
    11.0

Energy correction
=================

On the basis of field observations, it appears reasonable to standardize the field
SPT N-value as a function of the input driving energy and its dissipation around
the sampler around the surrounding soil. The variations in testing procedures may
be at least partially compensated by converting the measured N-value to :math:`N_{60}`.

.. math::

    N_{60} = \dfrac{E_H \cdot C_B \cdot C_S \cdot C_R \cdot N}{0.6}

Where:

.. list-table:: 
    :header-rows: 0

    * - :math:`N_{60}`
      - Corrected SPT N-value for field procedures

    * - :math:`E_H`
      - Hammer efficiency

    * - :math:`C_B`
      - Borehole diameter correction

    * - :math:`C_S`
      - Sampler correction

    * - :math:`C_R`
      - Rod length correction

    * - N
      - Recorded SPT N-value in field

The values of :math:`E_H`, :math:`C_B`, :math:`C_S`, and :math:`C_R` can be found in
the table below.

.. table:: Correction table for field procedure of SPT N-value

    +--------------------+------------------------------+--------------------------------+
    | SPT Hammer Efficiencies                                                            |
    +====================+==============================+================================+
    | **Hammer Type**    | **Hammer Release Mechanism** | **Efficiency**, :math:`E_H`    |
    +--------------------+------------------------------+--------------------------------+
    | Automatic          | Trip                         | 0.70                           |
    +--------------------+------------------------------+--------------------------------+
    | Donut              | Hand dropped                 | 0.60                           |
    +--------------------+------------------------------+--------------------------------+
    | Donut              | Cathead+2 turns              | 0.50                           |
    +--------------------+------------------------------+--------------------------------+
    | Safety             | Cathead+2 turns              | 0.55 - 0.60                    |
    +--------------------+------------------------------+--------------------------------+
    | Drop/Pin           | Hand dropped                 | 0.45                           |
    +--------------------+------------------------------+--------------------------------+
    | Borehole, Sampler and Rod Correction                                               |
    +--------------------+------------------------------+--------------------------------+
    | **Factor**         | **Equipment Variables**      | **Correction Factor**          |
    +--------------------+------------------------------+--------------------------------+
    | Borehole Dia       | 65 - 115 mm (2.5-4.5 in)     | 1.00                           |
    | Factor,            |                              |                                |
    | :math:`C_B`        |                              |                                |
    +--------------------+------------------------------+--------------------------------+
    |                    | 150 mm (6 in)                | 1.05                           |
    +--------------------+------------------------------+--------------------------------+
    |                    | 200 mm (8 in)                | 1.15                           |
    +--------------------+------------------------------+--------------------------------+
    | Sampler            | Standard sampler             | 1.00                           |
    | Correction,        |                              |                                |
    | :math:`C_S`        |                              |                                |
    +--------------------+------------------------------+--------------------------------+
    |                    | Sampler without liner        | 1.20                           |
    |                    | (not recommended)            |                                |
    +--------------------+------------------------------+--------------------------------+
    | Rod Length         | 3 - 4 m (10-13 ft)           | 0.75                           |
    | Correction,        |                              |                                |
    | :math:`C_R`        |                              |                                |
    +--------------------+------------------------------+--------------------------------+
    |                    | 4 - 6 m (13-20 ft)           | 0.85                           |
    +--------------------+------------------------------+--------------------------------+
    |                    | 6 - 10 m (20-30 ft)          | 0.95                           |
    +--------------------+------------------------------+--------------------------------+
    |                    | >10 m (>30 ft)               | 1.00                           |
    +--------------------+------------------------------+--------------------------------+

Energy correction can be computed as follows: ::

    >>> SPTCorrections.energy_correction(recorded_spt_val=15.0, 
    ...                                  hammer_efficiency=0.6,
    ...                                  borehole_diameter_correction=1,
    ...                                  sampler_correction=1,
    ...                                  rod_length_correction=0.85
    ... )
    12.75

Overburden Pressure Correction
==============================

In cohesionless soils, penetration resistance is affected by overburden pressure.
Soils with the same density but different confining pressures have varying
penetration numbers, with higher confining pressures leading to higher penetration
numbers. As depth increases, confining pressure rises, causing underestimation of
penetration numbers at shallow depths and overestimation at deeper depths. The need
for corrections in Standard Penetration Test (SPT) values was acknowledged only in
1957 by Gibbs & Holtz, meaning data published before this, like Terzaghi's, are
based on uncorrected values.

The general formula for overburden pressure correction is:

.. math::

    (N_1)_{60} = C_N \cdot N_{60} \le 2 \cdot N_{60}

Where:

- :math:`C_N` = Overburden Pressure Correction Factor

.. list-table::
    :header-rows: 1

    * - Available OPC
      - Year Published

    * - Gibbs & Holtz
      - 1957

    * - Bazaraa & Peck
      - 1969

    * - Peck et al
      - 1974

    * - Liao & Whitman
      - 1986

    * - Skempton
      - 1986

Overburden pressure corrections can be computed as follows: ::

    >>> SPTCorrections.gibbs_holtz_opc_1957(spt_n_60=15, eop=100)
    15.44
    >>> SPTCorrections.peck_et_al_opc_1974(spt_n_60=15, eop=100)
    15.03
    >>> SPTCorrections.liao_whitman_opc_1986(spt_n_60=15, eop=100)
    15.0
    >>> SPTCorrections.skempton_opc_1986(spt_n_60=15, eop=100)
    14.68
    >>> SPTCorrections.bazaraa_peck_opc_1969(spt_n_60=15, eop=100)
    13.99

Dilatancy Correction
====================

**Dilatancy Correction** is a correction for silty fine sands and fine sands 
below the water table that develop pore pressure which is not easily dissipated. 
The pore pressure increases the resistance of the soil hence the standard 
penetration number (N). Correction of silty fine sands recommended by 
``Terzaghi and Peck (1948)`` if :math:`N_{60}` exceeds 15.

Dilatancy correction can be computed as follows: ::

    >>> SPTCorrections.terzaghi_peck_dc_1948(corrected_spt_val=20)
    17.5

For convenience you can use the ``map`` method on ``SPTCorrections`` to compute
the overburden pressure and dilatancy correction. ::

    >>> opc_func = SPTCorrections.gibbs_holtz_opc_1957
    >>> standardized_spt_vals = [7.5, 15.0, 22.5, 30.0, 37.5]
    >>> opcs = SPTCorrections.map(opc_func=opc_func, 
    ...                           standardized_spt_vals=standardized_spt_vals,
    ...                           eop=100)
    >>> # Note: SPTCorrections.map returns a map object
    >>> list(opcs)
    [7.72, 15.44, 23.16, 30.88, 38.6]

Using ``map`` with dilatancy correction ::

    >>> opc_func = SPTCorrections.skempton_opc_1986
    >>> dc_func = SPTCorrections.terzaghi_peck_dc_1948
    >>> standardized_spt_vals = [7.5, 15.0, 22.5, 30.0, 37.5]
    >>> corr = SPTCorrections.map(opc_func=opc_func,
    ...                           dc_func=dc_func,
    ...                           standardized_spt_vals=standardized_spt_vals,
    ...                           eop=100)
    [7.34, 14.68, 18.51, 22.18, 25.84]

