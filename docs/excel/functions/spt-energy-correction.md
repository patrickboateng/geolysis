# GEOLYSIS.SPT_ENERGY_CORRECTION

## Description
Returns the SPT N-value corrected for field procedures.

## Syntax
```
GEOLYSIS.SPT_ENERGY_CORRECTION(recorded_spt_n_value, [energy_percentage], [borehole_diameter], [rod_length], [hammer_type], [sampler_type])
```

## Parameters
| Name                 | Type   | Required?   | Description                                                                                                                                           |
|:---------------------|:-------|:------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
| recorded_spt_n_value | number | Yes         | Recorded SPT N value. Valid values are between (0 < recorded_spt_n_value <= 100)                                                                      |
| energy_percentage    | number | No          | Percentage of energy reaching the tip of the sampler. Valid values are between (0.0 < energy_percentage <= 1.0). If omitted, energy_percentage = 0.6. |
| borehole_diameter    | number | No          | Borehole diameter (mm). Valid values are between (65.0 <= borehole_diameter <= 200.0) If omitted, borehole_diameter = 65.0.                           |
| rod_length           | number | No          | Length of spt rod (m). Valid values are (rod_length > 0.0). If omitted, rod_length = 3.0.                                                             |
| hammer_type          | string | No          | Hammer type. If omitted, hammer_type = "donut_1". Available options are "automatic", "donut_1", "donut_2", "safety", "drop" and "pin"                 |
| sampler_type         | string | No          | Sampler type. If omitted, sampler_type = "standard". Available options are "standard" and "non_standard".                                             |

