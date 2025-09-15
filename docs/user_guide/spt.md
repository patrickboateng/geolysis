# Standard Penetration Tests Analysis

## SPT N-Design

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

## Energy Correction

```python

>>> from geolysis.spt import EnergyCorrection
>>> energy_corr = EnergyCorrection(recorded_spt_n_value=30,
...                                energy_percentage=0.6,
...                                borehole_diameter=65.0,
...                                rod_length=3.0)
>>> energy_corr.standardized_spt_n_value()
22.5

```

## Overburden Pressure Correction

```python

>>> from geolysis.spt import create_overburden_pressure_correction
>>> opc_corr = create_overburden_pressure_correction(std_spt_n_value=23,
...                                                  eop=100, 
...                                                  opc_type="gibbs")
>>> opc_corr.corrected_spt_n_value()
23.7

```

Other available `opc_type` can be found in [OPCType][geolysis.spt.OPCType].

## Dilatancy Correction

```python

>>> from geolysis.spt import DilatancyCorrection
>>> dil_corr = DilatancyCorrection(corr_spt_n_value=17.7)
>>> dil_corr.corrected_spt_n_value()
16.4

```
