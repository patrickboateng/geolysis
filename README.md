[code_of_conduct_url]: https://github.com/patrickboateng/geolysis/blob/main/CODE_OF_CONDUCT.md/
[contributing_url]: https://github.com/patrickboateng/geolysis/blob/main/docs/CONTRIBUTING.md#how-to-contribute
[changelog_url]: https://github.com/patrickboateng/geolysis/blob/main/CHANGELOG.md
[license_url]: https://github.com/patrickboateng/geolysis/blob/main/LICENSE.txt

# geolysis

<div align="center">

[![GitHub Repo stars](https://img.shields.io/github/stars/patrickboateng/geolysis?style=flat)](https://github.com/patrickboateng/geolysis/stargazers)
[![PyPI Latest Release](https://img.shields.io/pypi/v/geolysis?style=flat&logo=pypi)](https://pypi.org/project/geolysis/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/geolysis.svg?logo=python&style=flat)](https://pypi.python.org/pypi/geolysis/)
[![GitHub last commit](https://img.shields.io/github/last-commit/patrickboateng/geolysis?logo=github&style=flat)](https://github.com/patrickboateng/geolysis/commits)
[![license](https://img.shields.io/pypi/l/geolysis?style=flat)](https://opensource.org/license/mit/)

#

![Coveralls branch](https://img.shields.io/coverallsCoverage/github/patrickboateng/geolysis)
[![CI-Unit-Test](https://github.com/patrickboateng/geolysis/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/patrickboateng/geolysis/actions/workflows/unit-tests.yml)
[![CI-Build-Test](https://github.com/patrickboateng/geolysis/actions/workflows/build.yml/badge.svg)](https://github.com/patrickboateng/geolysis/actions/workflows/build.yml)

</div>

## Project Links

<!-- - [Homepage](https://github.com/patrickboateng/geolysis) -->

<!-- - [Documentation](/docs) -->

- [PyPi](https://pypi.org/project/geolysis/)
- [Bug Reports](https://github.com/patrickboateng/geolysis/issues)
- [Discussions](https://github.com/patrickboateng/geolysis/discussions)

> [!IMPORTANT]
> Project documentation is underway

## Table of Contents

- [What is geolysis?](#what-is-geolysis)
- [Installation](#installation)
- [Usage Example](#example)
- [Release History](#release-history)
- [Code of Conduct](#code-of-conduct)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)

## What is geolysis?

`geolysis` is an open-source software for geotechnical analysis and modeling.
It provides features such as soil classifications
(based on the `USCS` and `AASHTO` classification standards), estimating soil
bearing capacity using SPT N-value, and estimating of soil engineering parameters
such as Soil Unit Weight (moist, saturated, and submerged), Compression index,
soil internal angle of friction, and undrained shear strength of soil.

**Features to include in upcoming versions:**

- Settlement analysis
- Finite element modeling
- Graphical User Interface (GUI)

The motivation behind `geolysis` is to provide free software to assist geotechnical
engineers in their day-to-day work and to expose civil engineering students
(especially geotechnical students) to tools that can make them industry-ready
geotechnical engineers right from college.

## Installation

```shell
pip install geolysis
```

## Example

### Classification of soil using `AASHTO` classification system

```python
>>> from geolysis.soil_classifier import AASHTO, AASHTOClassification
>>> aashto_clf = AASHTOClassification(liquid_limit=37.7,
...                                   plasticity_index=13.9,
...                                   fines=47.44)
>>> aashto_clf.classify()
'A-6(4)'
>>> aashto_clf = AASHTO(liquid_limit=30.2, plasticity_index=6.3, fines=11.18)
>>> aashto_clf.classify()
'A-2-4(0)'

```

> [!NOTE] > `AASHTOClassification` and `AASHTO` can be used interchangeably
> In other words `AASHTO` is an alias for `AASHTOClassification`

### Classification of soil using `USCS` classification system

```python
>>> from geolysis.soil_classifier import (
...    USCS,
...    UnifiedSoilClassification,
...    AtterbergLimits,
...    PSD,
...    ParticleSizes,
...    )
>>> al = AtterbergLimits(liquid_limit=35.83, plastic_limit=25.16)
>>> psd = PSD(fines=68.94, sand=28.88, gravel=2.18)
>>> uscs_clf = USCS(atterberg_limits=al, psd=psd)
>>> uscs_clf.classify()
'ML'

>>> al = AtterbergLimits(liquid_limit=30.8, plastic_limit=20.7)
>>> particle_sizes = ParticleSizes(d_10=0.07, d_30=0.3, d_60=0.8)
>>> psd = PSD(fines=10.29, sand=81.89, gravel=7.83, particle_sizes=particle_sizes)
>>> uscs_clf = USCS(atterberg_limits=al, psd=psd)
>>> uscs_clf.classify()
'SW-SC'

```

> [!NOTE] > `UnifiedSoilClassification` and `USCS` can be used interchangeably
> In other words `USCS` is an alias for `UnifiedSoilClassification`

## Release History

Check the [changelog][changelog_url]
for release history.

## Code of Conduct

This project has a [code of conduct][code_of_conduct_url] that we
expect all contributors to adhere to. Please read and follow it
when participating in this project.

## Contributing

If you would like to contribute to this project, please read the
[contributing guidelines][contributing_url]

## License

Distributed under the [**MIT**][license_url] license. By using,
distributing, or contributing to this project, you agree to the
terms and conditions of this license.

## Contact Information

- [**LinkedIn**](https://linkedin.com/in/patrickboateng/)

> [!IMPORTANT]
> For questions or comments about `geolysis`, please ask them in the
> [discussions forum](https://github.com/patrickboateng/geolysis/discussions)
