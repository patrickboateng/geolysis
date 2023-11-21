<div align="center">

<h1> geolysis </h1>

<h3>

[Homepage](https://github.com/patrickboateng/geolysis) | [Documentation](/docs) |
[PyPi](https://pypi.org/project/geolysis/) |
[Source Code](https://github.com/patrickboateng/geolysis/) |
[Bug Reports](https://github.com/patrickboateng/geolysis/issues) |
[Discussions](https://github.com/patrickboateng/geolysis/discussions)

</h3>

[![GitHub Repo stars](https://img.shields.io/github/stars/patrickboateng/geolysis?style=flat)](https://github.com/patrickboateng/geolysis/stargazers)
[![PyPI Latest Release](https://img.shields.io/pypi/v/geolysis?style=flat&logo=pypi&logoColor=white)](https://pypi.org/project/geolysis/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/geolysis.svg?style=flat)](https://pypi.python.org/pypi/geolysis/)
[![license](https://img.shields.io/pypi/l/geolysis?style=flat)](https://opensource.org/license/mit/)
[![GitHub last commit](https://img.shields.io/github/last-commit/patrickboateng/geolysis?logo=github&style=flat)](https://github.com/patrickboateng/geolysis/commits)
[![CI - Test](https://github.com/patrickboateng/geolysis/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/patrickboateng/geolysis/actions/workflows/unit-tests.yml)
[![CI - Test](https://github.com/patrickboateng/geolysis/actions/workflows/build.yml/badge.svg)](https://github.com/patrickboateng/geolysis/actions/workflows/build.yml)

</div>

## Table of Contents

- [What is geolysis?](#what-is-geolysis)
- [Installation](#installation)
- [Usage Example](#usage-example)
- [Release History](#release-history)
- [Code of Conduct](#code-of-conduct)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)

## What is geolysis?

`geolysis` is an open-source software for geotechnical engineering analysis and
modeling. `geolysis` provides soil classification based on `USCS` and `AASHTO`
standards, `bearing capacity analysis`,`estimation of soil engineering
properties`, `settlement analysis`, and `finite element modeling`. The software
assists geotechnical engineers in their day-to-day work, enabling them to
efficiently perform a wide range of tasks and make informed decisions about
design and construction. `geolysis` enhances efficiency and effectiveness,
allowing engineers to design and build better projects.

## Installation

> [!WARNING]
> Project is still under development.

```shell
pip install geolysis
```

## Usage example

Classification of soil using `AASHTO` classification system.

```python

    >>> from geolysis.soil_classifier import AASHTOClassificationSystem
    >>> aashto_classifier = AASHTOClassificationSystem(liquid_limit=37.7,
    ...                                                plasticity_index=13.9,
    ...                                                fines=47.44)
    >>> aashto_classifier.classify()
    'A-6(4)'

```

## Release History

Check the [changelog](https://github.com/patrickboateng/geolysis/blob/main/CHANGELOG.md)
for release history.

## Code of Conduct

This project has a [code of conduct](https://github.com/patrickboateng/geolysis/blob/main/CODE_OF_CONDUCT.md)
that we expect all contributors to adhere to. Please read and follow it when
participating in this project.

## Contributing

If you would like to contribute to this project, please read the
[contributing guidelines](https://github.com/patrickboateng/geolysis/blob/main/docs/CONTRIBUTING.md#how-to-contribute)

## License

Distributed under the [**MIT**](https://github.com/patrickboateng/geolysis/blob/main/LICENSE.txt)
license. By using, distributing, or contributing to this project, you agree to
the terms and conditions of this license.

## Contact Information

- [**LinkedIn**](https://linkedin.com/in/patrickboateng/)

> [!IMPORTANT]
> For questions or comments about `geolysis`, please ask them in the
> [discussions forum](https://github.com/patrickboateng/geolysis/discussions)
