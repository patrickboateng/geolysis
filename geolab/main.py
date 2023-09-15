import sys

sys.path.insert(0, ".")

from geolab.bearing_capacity import FootingSize, FoundationSize
from geolab.bearing_capacity.ultimate import terzaghi_bearing_capacity
from geolab.utils import arctan, cos, isclose, log10, sin

if __name__ == "__main__":
    # spt = spt_corrections().n_design([1, 2, 4, 5])
    # print(spt)
    # print(cos(115))
    # print(arctan(45))
    f_size = FootingSize(1.715, 1.715)
    fs = FoundationSize(f_size, 1.2)
    t = terzaghi_bearing_capacity(10.7, 18.76, 18.5, fs)

    print(t.ultimate_4_square_footing())
    print(t.nc, t.nq, t.ngamma)
