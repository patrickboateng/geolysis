# GEOLYSIS.AASHTO

## Description
Returns the AASHTO classification of the soil.

## Syntax
```
GEOLYSIS.AASHTO(liquid_limit, plastic_limit, fines, [only_group_idx], [add_group_idx], [description])
```

## Parameters
| Name           | Type    | Required?   | Description                                                                                                                                                                                                 |
|:---------------|:--------|:------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| liquid_limit   | number  | Yes         | Liquid limit of the soil (%). liquid_limit >= 0 and liquid_limit > plastic_limit                                                                                                                            |
| plastic_limit  | number  | Yes         | Plastic limit of the soil (%). plastic_limit >= 0.                                                                                                                                                          |
| fines          | number  | Yes         | Percentage of fines in the soil. fines >= 0.                                                                                                                                                                |
| only_group_idx | boolean | No          | Indicates whether only the group index should be returned. It takes precedence over add_group_idx and description. If omitted, only_group_idx = false.                                                      |
| add_group_idx  | boolean | No          | Indicates whether the group index should be added to the classification. If omitted, add_group_idx = true.                                                                                                  |
| description    | boolean | No          | Indicates whether to return the description of the classification. If omitted, description = false. NB: If only_group_idx=true,then description won't be returned, intead the group index will be returned. |

