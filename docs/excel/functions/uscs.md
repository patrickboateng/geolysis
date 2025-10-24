# GEOLYSIS.USCS

## Description
Returns the USCS classification of the soil.

## Syntax
```
GEOLYSIS.USCS(liquid_limit, plastic_limit, fines, sand, [d_10], [d_30], [d_60], [organic], [description])
```

## Parameters
| Name          | Type    | Required?   | Description                                                                                         |
|:--------------|:--------|:------------|:----------------------------------------------------------------------------------------------------|
| liquid_limit  | number  | Yes         | Liquid limit of the soil (%). liquid_limit >= 0 and liquid_limit > plastic_limit                    |
| plastic_limit | number  | Yes         | Plastic limit of the soil (%). plastic_limit >= 0.                                                  |
| fines         | number  | Yes         | Percentage of fines in the soil. fines >= 0.                                                        |
| sand          | number  | Yes         | Percentage of sand in the soil. sand >= 0.                                                          |
| d_10          | number  | No          | Diameter at which 10% of soil is finer.                                                             |
| d_30          | number  | No          | Diameter at which 30% of soil is finer.                                                             |
| d_60          | number  | No          | Diameter at which 60% of soil is finer.                                                             |
| organic       | boolean | No          | Indicates whether the soil is organic. If omitted, organic = false.                                 |
| description   | boolean | No          | Indicates whether to return the description of the classification. If omitted, description = false. |

