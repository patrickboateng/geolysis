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
