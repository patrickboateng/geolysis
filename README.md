# geolab

`geolab` is an open-source software for geotechnical engineering analysis and modelling.

<p align="center">
    <a href="https://pypi.org/user/Pato546/">
        <img src="https://img.shields.io/badge/PyPi-Pato546-blue?style=flat-square&logo=pypi&logoColor=white" alt="pypi">
    </a>
    <a href="">
        <img src="https://img.shields.io/pypi/l/geolab?style=flat-square" alt="license">
    </a>
    <a href="https://pycqa.github.io/isort/">
        <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat-square&labelColor=ef8336" alt="isort">
    </a>
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">
    </a>
    <a href="">
        <img src="https://img.shields.io/github/repo-size/patrickboateng/geolab?style=flat-square&labelColor=ef8336" alt="repo size">
    </a>
</p>

`geolab` offers a suite of powerful tools and features for soil analysis and
modeling. It provides soil classification based on both USCS and AASHTO
standards, bearing capacity analysis, estimation of soil engineering properties,
settlement analysis, and finite element modeling. The software assists
geotechnical engineers in their day-to-day work, enabling them to perform a wide
range of tasks with ease and make informed decisions about design and
construction. `geolab` enhances efficiency and effectiveness, allowing engineers
to design and build better projects with confidence.

## Features

- Provides soil classification based on `USCS` and `AASHTO` standards.
- Bearing capacity analysis can be performed, both from results obtained from
  **laboratory** or **field**.
- Estimates important soil engineering properties.
- Settlement analysis tools to predict and model soil settlements under various
  loads and conditions.
- Supports finite element modeling of soil behaviour under different conditions.

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
> This install does not work yet. Project is still under **rapid** development

```shell

pip install geolab

```

## Usage example

```python

>>> from geolab.soil_classifier import AASHTO, USCS
>>> aashto_classifier = AASHTO(liquid_limit=37.7, plasticity_index=13.9, fines=47.44)
>>> aashto_classifier.classify()
'A-6(4)'

# single classification
>>> uscs_classifier = USCS(liquid_limit=34.1, plastic_limit=21.1, plasticity_index=13,
...                        fines=47.88, sand=37.84, gravel=14.28)
>>> uscs_classifier.classify()
'SC'

# dual classification
>>> uscs_classifier = USCS(liquid_limit=30.8, plastic_limit=20.7, plasticity_index=10.1,
...                       fines=10.29, sand=81.89, gravel=7.83, d10=0.07, d30=0.3, d60=0.8)
>>> uscs_classifier.classify()
'SW-SC'

```

## Release History

Check the [CHANGELOG](./CHANGELOG.md) for release history.

## Code of Conduct

This project has a [CODE_OF_CONDUCT](./CODE_OF_CONDUCT.md) that we expect all
contributors to adhere to. Please read and follow it when participating in this
project.

## Contributing

See [CONTRIBUTING](docs/CONTRIBUTING.md#how-to-contribute) for more information
on contributing.

## License

Distributed under the `MIT license`. See [LICENSE](./LICENSE.txt) for more
information. By using, distributing, or contributing to this project, you agree
to the terms and conditions of this license.

## Contact Information

- **Email**: <boatengpato.pb@gmail.com>,
- **LinkedIn**: <https://linkedin.com/in/patrickboateng/>

> [!IMPORTANT]
> For questions or comments about `geolab`, please contact <boatengpato.pb@gmail.com>

## Project Links

- [**Documentation**](https://)
- [**PyPi**](https://)
- [**Source Code**](https://github.com/patrickboateng/geolab/)
- [**Website**](https://)
