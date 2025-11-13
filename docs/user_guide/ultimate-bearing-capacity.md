# Ultimate Bearing Capacity Estimation

Calculating the ultimate bearing capacity of soil using ``Vesic's``
correlation:

```python

>>> from geolysis.bearing_capacity.ubc import create_ubc_4_all_soils
>>> hansen_ubc = create_ubc_4_all_soils(friction_angle=20.0,
...                                     cohesion=20.0,
...                                     moist_unit_wgt=18.0,
...                                     depth=1.5,
...                                     width=2.0,
...                                     shape="square",
...                                     ubc_method="vesic")
>>> hansen_ubc.ultimate_bearing_capacity()
893.2

```

Other available `shape` and `ubc_type` can be found in
[Shape][geolysis.foundation.Shape] and
[UBCType][geolysis.bearing_capacity.ubc.UBCType] respectively.
