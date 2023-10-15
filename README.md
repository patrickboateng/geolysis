# geolysis

<p align="center">
    <a href="https://pypi.org/project/geolysis/">
        <img src="https://img.shields.io/pypi/v/geolysis?style=flat-square&logo=pypi&logoColor=white"
        alt="PyPI Latest Release">
    </a>
    <a href="">
        <img src="https://img.shields.io/pypi/l/geolysis?style=flat-square" alt="license">
    </a>
    <a href="https://pycqa.github.io/isort/">
        <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat-square"
        alt="isort">
    </a>
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square"
        alt="black">
    </a>
    <a href="https://github.com/patrickboateng/geolysis/actions/workflows/unit-tests.yml">
        <img src="https://github.com/patrickboateng/geolysis/actions/workflows/unit-tests.yml/badge.svg"
        alt="CI - Test">
    </a>
    <a href="https://github.com/patrickboateng/geolysis/actions/workflows/build.yml">
        <img src="https://github.com/patrickboateng/geolysis/actions/workflows/build.yml/badge.svg"
        alt="CI - Test">
    </a>
    <a href="">
        <img src="https://img.shields.io/github/repo-size/patrickboateng/geolysis?style=flat-square"
        alt="repo size">
    </a>
</p>

`geolysis` is an open-source software for geotechnical engineering analysis and
modeling. `geolysis` provides soil classification based on `USCS` and `AASHTO`
standards, `bearing capacity analysis`,`estimation of soil engineering
properties`, `settlement analysis`, and `finite element modeling`. The software
assists geotechnical engineers in their day-to-day work, enabling them to
efficiently perform a wide range of tasks and make informed decisions about
design and construction. `geolysis` enhances efficiency and effectiveness,
allowing engineers to design and build better projects.

## Table of Contents

- [Installation](#installation)
- [Usage Example](#usage-example)
- [Release History](#release-history)
- [Code of Conduct](#code-of-conduct)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)
- [Project Links](#project-links)

## Installation

> [!WARNING]
> Project is still under development.

```shell

pip install geolysis

```

## Usage example

Classification of soil using `AASHTO` classification system.

```python

    >>> from geolab.soil_classifier import AASHTO
    >>> aashto_classifier = AASHTO(liquid_limit=37.7,
    ...                            plasticity_index=13.9,
    ...                            fines=47.44)
    >>> aashto_classifier.classify()
    'A-6(4)'

```

See [examples](https://github.com/patrickboateng/geolysis/blob/main/docs/source/examples/)
folder for more usage examples.

## Release History

Check the [CHANGELOG](https://github.com/patrickboateng/geolysis/blob/main/CHANGELOG.md)
for release history.

## Code of Conduct

This project has a [CODE_OF_CONDUCT](https://github.com/patrickboateng/geolysis/blob/main/CODE_OF_CONDUCT.md)
that we expect all contributors to adhere to. Please read and follow it when
participating in this project.

## Contributing

See [CONTRIBUTING](https://github.com/patrickboateng/geolysis/blob/main/docs/CONTRIBUTING.md#how-to-contribute)
for more information on contributing.

## License

Distributed under the `MIT license`. See [LICENSE](https://github.com/patrickboateng/geolysis/blob/main/LICENSE.txt)
for more information. By using, distributing, or contributing to this project,
you agree to the terms and conditions of this license.

## Contact Information

- **LinkedIn**: <https://linkedin.com/in/patrickboateng/>

> [!IMPORTANT]
> For questions or comments about `geolysis`, please contact <https://linkedin.com/in/patrickboateng/>

## Project Links

- [**Documentation**](https://)
- [**PyPi**](https://)
- [**Source Code**](https://github.com/patrickboateng/geolysis/)
- [**Website**](https://)
