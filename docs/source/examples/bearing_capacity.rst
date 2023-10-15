Ultimate Bearing Capacity example:

Terzaghi Bearing Capacity example:

.. doctest::

    >>> from geolab.bearing_capacity import FoundationSize
    >>> from geolab.bearing_capacity.ultimate import TerzaghiBearingCapacity
    >>> tbc = TerzaghiBearingCapacity(cohesion=16,
    ...                               soil_friction_angle=27,
    ...                               soil_unit_weight=18.5,
    ...                               foundation_size=FoundationSize(1.068, 1.068, 1.2))
    >>> tbc.nc
    29.24
    >>> tbc.nq
    15.9
    >>> tbc.ngamma
    11.6
    >>> tbc.ultimate_4_square_footing()
    1052.85
