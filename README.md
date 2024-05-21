[code_of_conduct_url]: https://github.com/patrickboateng/geolysis/blob/main/CODE_OF_CONDUCT.md/
[contributing_url]: https://github.com/patrickboateng/geolysis/blob/main/docs/CONTRIBUTING.md#how-to-contribute
[changelog_url]: https://github.com/patrickboateng/geolysis/blob/main/CHANGELOG.md
[license_url]: https://github.com/patrickboateng/geolysis/blob/main/LICENSE.txt

# geolysis

<div align="center">

[![PyPI Latest Release](https://img.shields.io/pypi/v/geolysis?style=flat&logo=pypi)](https://pypi.org/project/geolysis/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/geolysis.svg?logo=python&style=flat)](https://pypi.python.org/pypi/geolysis/)
[![license](https://img.shields.io/pypi/l/geolysis?style=flat&logo=opensourceinitiative)](https://opensource.org/license/mit/)

![Coveralls Status](https://img.shields.io/coverallsCoverage/github/patrickboateng/geolysis?logo=coveralls)
[![Unit-Tests](https://github.com/patrickboateng/geolysis/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/patrickboateng/geolysis/actions/workflows/unit-tests.yml)
[![Pkg Build](https://github.com/patrickboateng/geolysis/actions/workflows/pkg_build.yml/badge.svg)](https://github.com/patrickboateng/geolysis/actions/workflows/pkg_build.yml)
[![Documentation Status](https://readthedocs.org/projects/geolysis/badge/?version=latest)](https://geolysis.readthedocs.io/en/latest/?badge=latest)

</div>

#

`geolysis.core` is an open-source Python package that provides features
for analyzing geotechnical results obtained from laboratory and field
tests. Some of the features implemented include soil classification,
standard penetration test analysis (such as SPT $N_{design}$ and SPT
N-value corrections), and calculating the allowable bearing capacity of
soils from Standard Penetration Test N-values. There are more features
underway, which include settlement analysis, ultimate bearing capacity
analysis, etc.

`geolysis.core` is the foundation application on which other parts of the
application will depend. Developers can also use `geolysis.core` to power
their applications.

Check out the [release notes](https://geolysis.rtfd.io/release_notes/index.html)
for features.

## Project Links

- [Documentation](https://geolysis.readthedocs.org/en/latest)
- [Repo](https://github.com/patrickboateng/geolysis)
- [PyPi](https://pypi.org/project/geolysis/)
- [Bug Reports](https://github.com/patrickboateng/geolysis/issues)
- [Discussions](https://github.com/patrickboateng/geolysis/discussions)

<!-- > [!IMPORTANT]
> Project documentation is underway -->

## Table of Contents

- [Motivation](#motivation)
- [Installation](#installation)
- [Getting Started](#getting-started)
  - [Soil Classification Example](#soil-classification-example)
- [Release History](#release-history)
- [Code of Conduct](#code-of-conduct)
- [Contributing](#contributing)
- [License](#license)
- [Governance of this project](#governance-of-this-project)
- [Contact Information](#contact-information)

## Motivation

`geolysis.core` is a free software package designed specifically to
assist developers in building applications that can solve complex
geotechnical problems. Whether you're working on soil mechanics,
rock mechanics, or any other geotechnical field, `geolysis.core`
provides a powerful set of tools that can help you design and
develop robust solutions. With an intuitive API and a wide range
of features, this software is an essential tool for anyone who
needs to work with geotechnical data on a regular basis. Whether
you're a seasoned geotechnical engineer or a new developer just
getting started in the field, `geolysis.core` is the ideal solution
for all your software development needs.

## Installation

```shell
pip install geolysis
```

## Getting Started

### Soil Classification Example

AASHTO classification

```python

>>> from geolysis.core.soil_classifier import AASHTO
>>> aashto_cls = AASHTO(liquid_limit=30.2, plasticity_index=6.3, fines=11.18)
>>> aashto_cls.soil_class
'A-2-4(0)'
>>> aashto_cls.soil_desc
'Silty or clayey gravel and sand'

```

USCS Classification

```python

>>> from geolysis.core.soil_classifier import USCS
>>> uscs_cls = USCS(liquid_limit=34.1, plastic_limit=21.1,
...                 fines=47.88, sand=37.84, gravel=14.8)
>>> uscs_cls.soil_class
'SC'
>>> uscs_cls.soil_desc
'Clayey sands'
>>> uscs_cls = USCS(liquid_limit=30.8, plastic_limit=20.7, fines=10.29,
...                 sand=81.89, gravel=7.83, d_10=0.07, d_30=0.3, d_60=0.8)
>>> uscs_cls.soil_class
'SW-SC'
>>> uscs_cls.soil_desc
'Well graded sand with clay'

```

<!-- See the [Quick start section] of the docs for more examples. -->

## Release History

Check the [changelog][changelog_url] for release history.

## Code of Conduct

This project has a [code of conduct][code_of_conduct_url] that
we expect all contributors to adhere to. Please read and follow
it when participating in this project.

## Contributing

If you would like to contribute to this project, please read
the [contributing guidelines][contributing_url]

## License

Distributed under the [**MIT**][license_url] license. By using,
distributing, or contributing to this project, you agree to the
terms and conditions of this license.

## Governance of this project

`geolysis.core` is still developing relatively rapidly, so please
be patient if things change or features iterate and change quickly.
Once `geolysis.core` hits 1.0, it will slow down considerably.

## Contact Information

- [**LinkedIn**](https://linkedin.com/in/patrickboateng/)

> [!IMPORTANT]
> For questions or comments about `geolysis.core`, please ask them in the
> [discussions forum](https://github.com/patrickboateng/geolysis/discussions)
