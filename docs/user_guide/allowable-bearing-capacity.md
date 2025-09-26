# Allowable Bearing Capacity Estimation

Calculating the allowable bearing capacity of soil for pad foundations using
``Bowles`` correlations:

```python

>>> from geolysis.bearing_capacity.abc import create_abc_4_cohesionless_soils
>>> bowles_abc = create_abc_4_cohesionless_soils(corrected_spt_n_value=17.0,
...                                              tol_settlement=20.0,
...                                              depth=1.5,
...                                              width=1.2,
...                                              shape="square",
...                                              foundation_type="pad",
...                                              abc_type="bowles")
>>> bowles_abc.allowable_bearing_capacity()
341.1

```

Other available `shape`, `foundation_type`, and `abc_type` can be found
in [Shape][geolysis.foundation.Shape],
[FoundationType][geolysis.foundation.FoundationType], and
[ABCType][geolysis.bearing_capacity.abc.ABCType] respectively.
