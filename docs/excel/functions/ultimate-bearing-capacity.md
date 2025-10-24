# GEOLYSIS.ULTIMATE_BEARING_CAPACITY

## Description
Returns the ultimate bearing capacity of the soil for shallow foundations (kN/m^2 or kPa).

## Syntax
```
GEOLYSIS.ULTIMATE_BEARING_CAPACITY(friction_angle, cohesion, moist_unit_wgt, depth, width, [length], [factor_of_safety], [saturated_unit_wgt], [ground_water_level], [eccentricity], [load_angle], [apply_local_shear], [shape], [ubc_type], [allowable_bearing_capacity])
```

## Parameters
| Name                       | Type    | Required?   | Description                                                                                                                        |
|:---------------------------|:--------|:------------|:-----------------------------------------------------------------------------------------------------------------------------------|
| friction_angle             | number  | Yes         | Internal angle of friction for general shear failure (degrees). friction_angle >= 0.                                               |
| cohesion                   | number  | Yes         | Cohesion of the soil (kN/m^2). cohesion >= 0.                                                                                      |
| moist_unit_wgt             | number  | Yes         | Unit weight of the soil (kN/m^3). moist_unit_wgt > 0.                                                                              |
| depth                      | number  | Yes         | Depth of the foundation (m).                                                                                                       |
| width                      | number  | Yes         | Width of the foundation footing (m). width > 0.0                                                                                   |
| length                     | number  | No          | Length of the foundation footing (m). length > 0.0                                                                                 |
| factor_of_safety           | number  | No          | Factor of safety. If omitted factor_of_safety = 3.                                                                                 |
| saturated_unit_wgt         | number  | No          | Saturated unit weight of soil (kN/m^3). If omitted, saturated_unit_wgt = 20.5,                                                     |
| ground_water_level         | number  | No          | Depth of the ground water level (m). ground_water_level >= 0.                                                                      |
| eccentricity               | number  | No          | Eccentricity of applied load (m). eccentricity >= 0, If omitted, eccentricity = 0.0.                                               |
| load_angle                 | number  | No          | Inclination of applied load with the vertical (degrees). If omitted, load_angle = 0.0.                                             |
| apply_local_shear          | boolean | No          | Indicates whether to apply local shear. If omitted, apply_local_shear = false.                                                     |
| shape                      | string  | No          | Shape of the foundation footing. If omitted, shape = "square". Available options are "square", "rectangle", "circle", and "strip". |
| ubc_type                   | string  | No          | Type of bearing capacity calculation. If omitted, ubc_type = "vesic". Available options are "terzaghi", and "vesic".               |
| allowable_bearing_capacity | boolean | No          | Indicates whether to return the allowable bearing capacity of the soil or not.                                                     |

