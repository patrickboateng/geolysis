## Installation

`geolysis` supports Python 3.11 - 3.12. We also recommend using a
[virtual environment](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments)
in order to isolate your project dependencies from other projects and the 
system.

`geolysis` can be installed via [pip](https://pypi.org/project/geolysis) as 
follows for the supported operating systems.

```shell
pip install geolysis # "pip3 install geolysis" for unix systems
```

## Version Check

To see whether ``geolysis`` is already installed or to check if an install has
worked, run the following in a Python shell:

```python

import geolysis as gl
print(gl.__version__) 

```
    
or from the command line:

```shell

python -c "import geolysis; print(geolysis.__version__)" # python3 for unix systems

```
    
You'll see the version number if ``geolysis`` is installed and an error message
otherwise.

## Quick Start

### Prerequisites

You need to know [Python](https://docs.python.org/3/tutorial/) and a little
bit of soil mechanics in order to understand the following examples.

### Learning Objective

After reading, you should be able to:

- Perform basic soil analysis such as **soil classification**, **bearing
  capacity analysis**, and **standard penetration test analysis**.

### Soil Classification

#### AASHTO classification 

```python

>>> from geolysis.soil_classifier import create_aashto_classifier
>>> aashto_clf = create_aashto_classifier(liquid_limit=30.2,
...                                       plastic_limit=23.9,
...                                       fines=11.18, )
>>> clf = aashto_clf.classify()
>>> clf.symbol
'A-2-4(0)'
>>> clf.symbol_no_group_idx
'A-2-4'
>>> clf.group_index
'0'
>>> clf.description
'Silty or clayey gravel and sand'

```

#### USCS classification

Classification with soil grading

```python

>>> from geolysis.soil_classifier import create_uscs_classifier
>>> uscs_clf = create_uscs_classifier(liquid_limit=30.8,
...                                   plastic_limit=20.7,
...                                   fines=10.29,
...                                   sand=81.89,
...                                   d_10=0.07,
...                                   d_30=0.3,
...                                   d_60=0.8, )
>>> clf = uscs_clf.classify()
>>> clf.symbol
'SW-SC'
>>> clf.description
'Well graded sand with clay'

```

Classification without soil grading

```python

>>> uscs_clf = create_uscs_classifier(liquid_limit=34.1,
...                                   plastic_limit=21.1,
...                                   fines=47.88,
...                                   sand=37.84, )
>>> clf = uscs_clf.classify()
>>> clf.symbol
'SC'
>>> clf.description
'Clayey sands'

```


### Ultimate Bearing Capacity Estimation

Calculating the ultimate bearing capacity of soil using ``Hansen's``
correlation:

```python

>>> from geolysis.bearing_capacity.ubc import create_ubc_4_all_soil_types
>>> hansen_ubc = create_ubc_4_all_soil_types(friction_angle=20.0,
...                                          cohesion=20.0,
...                                          moist_unit_wgt=18.0,
...                                          depth=1.5,
...                                          width=2.0,
...                                          shape="square",
...                                          ubc_type="hansen")
>>> hansen_ubc.bearing_capacity()
798.41

```


Other available `shape` and `ubc_type` can be found in 
[Shape][geolysis.foundation.Shape] and 
[UBCType][geolysis.bearing_capacity.ubc.UBCType] respectively.

### Allowable Bearing Capacity Estimation

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
>>> bowles_abc.bearing_capacity()
341.11

```

Other available `shape`, `foundation_type`, and `abc_type` can be found
in [Shape][geolysis.foundation.Shape], 
[FoundationType][geolysis.foundation.FoundationType], and
[ABCType][geolysis.bearing_capacity.abc.ABCType] respectively.

### Standard Penetration Tests Analysis

#### SPT N-Design

```python

>>> from geolysis.spt import SPT
>>> spt = SPT(corrected_spt_n_values=[7.0, 15.0, 18.0], method="avg")
>>> spt.n_design()
13.3
>>> spt.method = "min"
>>> spt.n_design()
7.0
>>> spt.method = "wgt"
>>> spt.n_design()
9.4

```

#### Energy Correction

```python

>>> from geolysis.spt import EnergyCorrection
>>> energy_corr = EnergyCorrection(recorded_spt_n_value=30,
...                                energy_percentage=0.6,
...                                borehole_diameter=65.0,
...                                rod_length=3.0)
>>> energy_corr.standardized_spt_n_value()
22.5

```

#### Overburden Pressure Correction

```python

>>> from geolysis.spt import create_overburden_pressure_correction
>>> opc_corr = create_overburden_pressure_correction(std_spt_n_value=23,
...                                                  eop=100, 
...                                                  opc_type="gibbs")
>>> opc_corr.corrected_spt_n_value()
23.7

```

Other available `opc_type` can be found in [OPCType][geolysis.spt.OPCType].

#### Dilatancy Correction

```python

>>> from geolysis.spt import DilatancyCorrection
>>> dil_corr = DilatancyCorrection(corr_spt_n_value=17.7)
>>> dil_corr.corrected_spt_n_value()
16.4

```
