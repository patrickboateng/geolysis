# GEOLYSIS.SPT_OVERBURDEN_PRESSURE_CORRECTION

## Description
Returns the SPT N-value corrected for overburden pressure.

## Syntax
```
GEOLYSIS.SPT_OVERBURDEN_PRESSURE_CORRECTION(std_spt_n_value, eop, [opc_type])
```

## Parameters
| Name            | Type   | Required?   | Description                                                                                                                                    |
|:----------------|:-------|:------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
| std_spt_n_value | number | Yes         | Standardized SPT N value. Valid values are between (0.0 < std_spt_n_value <= 100.0)                                                            |
| eop             | number | Yes         | Effective overburden pressure (kN/m^2).                                                                                                        |
| opc_type        | string | No          | Overburden pressure correction type. If omitted, opc_type = "gibbs". Available options are "gibbs", "bazaraa", "peck", "liao", and "skempton". |

