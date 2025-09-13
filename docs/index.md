# Welcome to geolysis documentation

[![PyPI Latest Release](https://img.shields.io/pypi/v/geolysis?style=flat&logo=pypi)](https://pypi.org/project/geolysis/)
[![PyPI Downloads](https://static.pepy.tech/badge/geolysis)](https://pepy.tech/projects/geolysis)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/geolysis.svg?logo=python&style=flat)](https://pypi.python.org/pypi/geolysis/)
[![Unit-Tests](https://github.com/patrickboateng/geolysis/actions/workflows/geolysis-unit-tests.yml/badge.svg)](https://github.com/patrickboateng/geolysis/actions/workflows/geolysis-unit-tests.yml)
![Coveralls Status](https://img.shields.io/coverallsCoverage/github/patrickboateng/geolysis?logo=coveralls)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/17f88084c6a84a08a20f9d8da1438107)](https://app.codacy.com/gh/patrickboateng/geolysis/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![license](https://img.shields.io/pypi/l/geolysis?style=flat&logo=opensourceinitiative)](https://opensource.org/license/mit/)

`geolysis` is an open-source python package (library) for geotechnical analysis
and modeling.

!!! info "Geotechnical Software Toolkit"

    The `geolysis` python package is among three other projects, 
    `geolysis.excel`, `geolysis.gui`, and `geolysis.ai`. For me information 
    on the full geotechnical toolkit, 
    click [here](https://github.com/geolysis-dev).

## [Python API](reference/index.md)

- [allowable_bearing_capacity](reference/allowable-bearing-capacity.md)
- [ultimate_bearing_capacity](reference/ultimate-bearing-capacity.md)
- [foundation](reference/foundation.md)
- [soil_classifier](reference/soil-classifier.md)
- [spt](reference/spt.md)
- [utils](reference/utils.md)

## Imports

### Bearing Capacity

#### Allowable Bearing Capacity (ABC)

```python
from geolysis.bearing_capacity.abc import create_abc_4_cohesionless_soils
```

#### Ultimate Bearing Capacity (UBC)

```python
from geolysis.bearing_capacity.ubc import create_ubc_4_all_soil_types
```

### Foundation

```python
from geolysis.foundation import create_foundation
```

### Soil Classification

```python
from geolysis.soil_classifier import create_uscs_classifier
from geolysis.soil_classifier import create_aashto_classifier
```

### Standard Penetration Test (SPT) Analysis

```python
from geolysis.spt import DilatancyCorrection
from geolysis.spt import EnergyCorrection
from geolysis.spt import SPT
from geolysis.spt import create_overburden_pressure_correction
``` 
