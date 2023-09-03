import pytest

from geolab import ERROR_TOLERANCE

# from geolab.bearing_capacity.terzaghi import TerzaghiBearingCapacity

# from geolab.bearing_capacity.hansen import HansenBCF
# from geolab.bearing_capacity.vesic import VesicBCF


T_bearing_capacity_factors = [
    (1, {"nq": 1.10, "nc": 6.00}),
    (15, {"nq": 4.45, "nc": 12.86}),
    (25, {"nq": 12.72, "nc": 25.13}),
    (27, {"nq": 15.9, "nc": 29.24}),
    (18.76, {"nq": 6.54, "nc": 16.21}),
]

H_bearing_capacity_factors = [
    (5, {"nq": 1.57, "nc": 6.49, "ngamma": 0.09}),
    (10, {"nq": 2.47, "nc": 8.35, "ngamma": 0.47}),
    (15, {"nq": 3.94, "nc": 10.98, "ngamma": 1.42}),
    (20, {"nq": 6.40, "nc": 14.83, "ngamma": 3.54}),
]

V_bearing_capacity_factors = [
    (5, {"nq": 1.57, "nc": 6.49, "ngamma": 0.45}),
    (10, {"nq": 2.47, "nc": 8.35, "ngamma": 1.22}),
    (15, {"nq": 3.94, "nc": 10.98, "ngamma": 2.65}),
    (20, {"nq": 6.40, "nc": 14.83, "ngamma": 5.39}),
]
