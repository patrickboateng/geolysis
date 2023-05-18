# `geolab`

> `geolab` is an open-source software for geotechnical engineering analysis and modelling.

[![pypi](https://img.shields.io/badge/PyPi-Pato546-blue?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/user/Pato546/)
![license](https://img.shields.io/pypi/l/geolab?style=flat-square)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat-square&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![code style](https://img.shields.io/badge/code%20formatter-docformatter-fedcba.svg?style=flat-square)](https://github.com/PyCQA/docformatter)
[![style guide](https://img.shields.io/badge/%20style-google-3666d6.svg?style=flat-square)](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings)
![repo size](https://img.shields.io/github/repo-size/patrickboateng/geolab?style=flat-square&labelColor=ef8336)
![downloads](https://img.shields.io/pypi/dm/geolab?style=flat-square)

`geolab` is an open-source software for geotechnical engineering that offers a suite of powerful tools and features for soil analysis and modeling. It provides soil classification based on both USCS and AASHTO standards, bearing capacity analysis, estimation of soil engineering properties, settlement analysis, and finite element modeling. The software assists geotechnical engineers in their day-to-day work, enabling them to perform a wide range of tasks with ease and make informed decisions about design and construction. `geolab` enhances efficiency and effectiveness, allowing engineers to design and build better projects with confidence.

The key features of `geolab` are stated below:

- Provides soil classification based on `USCS` and `AASHTO` standards.
- Bearing capacity analysis can be performed in both from results obtained from laboratory or field tests.
- Estimates important soil engineering properties, aiding in decision-making.
- Settlement analysis tools predict and model soil settlements under various loads and conditions.
- Supports finite element modelling of soil behaviour under different conditions.

## Table of Contents

- [Installation](#installation)
- [Usage Example](#usage-example)
- [Release History](#release-history)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)
- [Links](#links)
- [Todo](#todo)

## Installation

> **&#9432;** This install does not work yet.

```sh
pip install geolab
```

## Usage example

```py
>>> from geolab.soil_classifier import aashto, uscs
>>> uscs(liquid_limit=34.1, plastic_limit=21.1, plasticity_index=13, fines=47.88, sand=37.84, gravels=14.28)
'SC'
>>> aashto(liquid_limit=34.1, plastic_limit=21.1, plasticity_index=13, fines=47.88)
'A-6(3)'

```

<!-- ## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
``` -->

## Release History

- 0.1.0
  - **rapid** development.

## Contributing

1. [Fork it](https://github.com/patrickboateng/geolab/fork)
2. Create your feature branch (`git checkout -b feature`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature`)
5. Create a new Pull Request

## License

Distributed under the `MIT license`. See [`LICENSE`](./LICENSE.txt) for more information.

## Contact Information

Patrick Boateng - <boatengpato.pb@gmail.com>, [LinkedIn](https://linkedin.com/in/patrickboateng/)

For questions or comments about `geolab`, please contact <boatengpato.pb@gmail.com>

## Links

- Documentation: <>
- PyPi: <>
- Source Code: <https://github.com/patrickboateng/geolab/>
- Issue Tracker: <>
- Website: <>

## Todo

- [x] Soil Classifier
- [x] Bearing Capacity Analysis
- [x] Estimating Soil Engineering Parameters
- [ ] Settlement Analysis
- [ ] Modelling the behavior of Soils under loads using `FEM`
