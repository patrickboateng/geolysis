# GEOLYSIS.ALLOWABLE_BEARING_CAPACITY

## Description
Returns the allowable bearing capacity of the soil for shallow foundations (kN/m^2 or kPa).

## Syntax
```
GEOLYSIS.ALLOWABLE_BEARING_CAPACITY(corrected_spt_n_value, tol_settlement, depth, width, [length], [eccentricity], [ground_water_level], [shape], [foundation_type], [abc_type])
```

## Parameters
| Name                  | Type   | Required?   | Description                                                                                                                        |
|:----------------------|:-------|:------------|:-----------------------------------------------------------------------------------------------------------------------------------|
| corrected_spt_n_value | number | Yes         | Corrected SPT N values. Valid values for each corrected_spt_n_value should be between (0 < corrected_spt_n_value <= 100)           |
| tol_settlement        | number | Yes         | Tolerable settlement of foundation (mm). (0 <= tol_settlement <= 25.4)                                                             |
| depth                 | number | Yes         | Depth of the foundation (m). depth > 0.0                                                                                           |
| width                 | number | Yes         | Width of the foundation footing (m). width > 0.0                                                                                   |
| length                | number | No          | Length of the foundation footing (m). length > 0.                                                                                  |
| eccentricity          | number | No          | Eccentricity of applied load (m). eccentricity >= 0. If omitted, eccentricity = 0.0.                                               |
| ground_water_level    | number | No          | Depth of the ground water level (m). ground_water_level >= 0.0                                                                     |
| shape                 | string | No          | Shape of the foundation footing. If omitted, shape = "square". Available options are "square", "rectangle", "circle", and "strip". |
| foundation_type       | string | No          | Type of foundation. If omitted, foundation_type = "pad". Available options are "pad" and "mat".                                    |
| abc_type              | string | No          | Type of bearing capacity calculation. If omitted, abc_type = "bowles". Available options are "bowles", "meyerhof", and "terzaghi". |

