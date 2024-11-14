[code_of_conduct_url]: https://github.com/patrickboateng/geolysis/blob/main/CODE_OF_CONDUCT.md/
[contributing_url]: https://github.com/patrickboateng/geolysis/blob/main/docs/CONTRIBUTING.md#how-to-contribute
[license_url]: https://github.com/patrickboateng/geolysis/blob/main/LICENSE.txt

# Core

<div align="center">

[![PyPI Latest Release](https://img.shields.io/pypi/v/geolysis?style=flat&logo=pypi)](https://pypi.org/project/geolysis/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/geolysis.svg?logo=python&style=flat)](https://pypi.python.org/pypi/geolysis/)
[![license](https://img.shields.io/pypi/l/geolysis?style=flat&logo=opensourceinitiative)](https://opensource.org/license/mit/)
![Coveralls Status](https://img.shields.io/coverallsCoverage/github/patrickboateng/geolysis?logo=coveralls)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/17f88084c6a84a08a20f9d8da1438107)](https://app.codacy.com/gh/patrickboateng/geolysis/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Unit-Tests](https://github.com/patrickboateng/geolysis/actions/workflows/geolysis-core-unit-tests.yml/badge.svg)](https://github.com/patrickboateng/geolysis/actions/workflows/geolysis-core-unit-tests.yml)
[![Documentation Status](https://readthedocs.org/projects/geolysis/badge/?version=latest)](https://geolysis.readthedocs.io/en/latest/?badge=latest)

</div>

> [!IMPORTANT]
> Project documentation is underway

## Project Links

- [Documentation](https://geolysis.readthedocs.org/en/latest)
- [Repo](https://github.com/patrickboateng/geolysis)
- [PyPi](https://pypi.org/project/geolysis/)
- [Bug Reports](https://github.com/patrickboateng/geolysis/issues)
- [Discussions](https://github.com/patrickboateng/geolysis/discussions)

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
  - [Soil Classification Example](#soil-classification-example)
- [Release History](#release-history)
- [Code of Conduct](#code-of-conduct)
- [Contributing](#contributing)
- [License](#license)
- [Governance of this project](#governance-of-this-project)
- [Contact Information](#contact-information)

## Installation

```shell
pip install geolysis
```

## Getting Started

### Soil Classification Example

AASHTO classification

```python

>>> from geolysis.core.soil_classifier import ClfType, create_soil_classifier
>>> aashto_clf = create_soil_classifier(
...     liquid_limit=30.2,
...     plastic_limit=23.9,
...     fines=11.18,
...     clf_type=ClfType.AASHTO,
... )
>>> aashto_clf.classify()
'A-2-4(0)'
>>> aashto_clf.description()
'Silty or clayey gravel and sand'

```

USCS Classification

```python

>>> from geolysis.core.soil_classifier import ClfType, create_soil_classifier
>>> uscs_clf = create_soil_classifier(
...     liquid_limit=34.1,
...     plastic_limit=21.1,
...     fines=47.88,
...     sand=37.84,
...     clf_type=ClfType.USCS,
... )
>>>
>>> uscs_clf.classify()
'SC'
>>> uscs_clf.description()
'Clayey sands'

>>> uscs_clf = create_soil_classifier(
...     liquid_limit=30.8,
...     plastic_limit=20.7,
...     fines=10.29,
...     sand=81.89,
...     d_10=0.07,
...     d_30=0.3,
...     d_60=0.8,
...     clf_type=ClfType.USCS,
... )
>>> uscs_clf.classify()
'SW-SC'
>>> uscs_clf.description()
'Well graded sand with clay'

```

## Release History

Check out the [release notes](https://geolysis.rtfd.io/en/latest/release_notes/index.html)
for features.

## Code of Conduct

This project has a [code of conduct][code_of_conduct_url] that we expect all
contributors to adhere to. Please read and follow it when participating in this
project.

## Contributing

If you would like to contribute to this project, please read the
[contributing guidelines][contributing_url]

## License

Distributed under the [**MIT**][license_url] license. By using, distributing, or
contributing to this project, you agree to the terms and conditions of this
license.

## Governance of this project

`geolysis.core` is still developing relatively rapidly, so please be patient if
things change or features iterate and change quickly.

Once `geolysis.core` hits `1.0.0`, it will slow down considerably.

## Contact Information

- [**LinkedIn**](https://linkedin.com/in/patrickboateng/)

> [!IMPORTANT]
> For questions or comments about `geolysis`, please ask them in the
> [discussions forum](https://github.com/patrickboateng/geolysis/discussions)
