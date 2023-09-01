import sys

sys.path.insert(0, ".")

from geolab.bearing_capacity.meyerhof import meyerhoff_bearing_capacity

if __name__ == "__main__":
    m = meyerhoff_bearing_capacity([1, 2, 3, 4, 5])

    print(m.n_design)
