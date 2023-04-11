# `geolab `: geotechnical engineering software for students and professionals.

<p align="center">
    <a href="https://pypi.org/user/Pato546/">
        <img src="https://img.shields.io/badge/PyPi-Pato546-blue?style=flat-square&logo=pypi&logoColor=white">
    </a>
    <a href="#">
        <img src="https://img.shields.io/pypi/l/geolab?style=flat-square">
    </a>
    <a>
        <img src="https://img.shields.io/pypi/dm/geolab?style=flat-square">
    </a>
    <a>
        <img src="https://img.shields.io/github/repo-size/patrickboateng/geolab?style=flat-square">
    </a>
</p>

`geolab` implements various geotechnical methods such as soil classification (USCS, AASHTO). Also, `geolab` implements methods for estimating soil engineering properties such as bearing capacity ($q_{ult}$), void ratio ($e_o$), undrained shear strength($C_u$), internal angle of friction ($\phi$) etc.

> **&#9432;** Only Unified Soil Classification (USCS) has been implemented as of now and can also be installed as a Microsoft Excel addin.

## Installation

Windows:

```sh
pip install geolab
```

## Usage example

```py
from geolab import soil_classifier

# element in data should be arranged as follows
# liquid limit, plastic limit, plasticity index, fines, sand, gravel
data = [34.1, 21.1, 13, 47.88, 37.84, 14.28]
soil = soil_classifier.Soil(*data)
usc_clf = soil.get_unified_classification()
aashto_clf = soil.get_aashto_classification()

print(usc_clf)
print(aashto_clf)
```

```sh
 'SC'
 'A-6(3)'
```

<!-- ## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
``` -->

## Release History

-   0.1.0
    -   **rapid** development.

## Contributing

1. [Fork it](https://github.com/patrickboateng/geolab/fork)
2. Create your feature branch (`git checkout -b feature`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature`)
5. Create a new Pull Request

## Todo

-   [x] Soil Classifier
-   [ ] Estimating Soil Engineering Parameters
-   [ ] Bearing Capacity Analysis
-   [ ] Settlement Analysis
-   [ ] Modelling the behavior of Soils under loads using `FEM`
