# geolab

`geolab` is an open-source software for geotechnical engineering analysis and modelling.

[![pypi](https://img.shields.io/badge/PyPi-Pato546-blue?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/user/Pato546/)
![license](https://img.shields.io/pypi/l/geolab?style=flat-square)
[![isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat-square&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![docformatter](https://img.shields.io/badge/code%20formatter-docformatter-fedcba.svg?style=flat-square)](https://github.com/PyCQA/docformatter)
![repo size](https://img.shields.io/github/repo-size/patrickboateng/geolab?style=flat-square&labelColor=ef8336)

<!-- [![style guide](https://img.shields.io/badge/%20style-google-3666d6.svg?style=flat-square)](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings) -->

<!-- ![downloads](https://img.shields.io/pypi/dm/geolab?style=flat-square) -->

`geolab` is an open-source software for geotechnical engineering that offers a suite of
powerful tools and features for soil analysis and modeling. It provides soil classification based
on both USCS and AASHTO standards, bearing capacity analysis, estimation of soil engineering properties,
settlement analysis, and finite element modeling. The software assists geotechnical engineers in their
day-to-day work, enabling them to perform a wide range of tasks with ease and make informed decisions
about design and construction. `geolab` enhances efficiency and effectiveness, allowing engineers to
design and build better projects with confidence.

## Features

- Provides soil classification based on `USCS` and `AASHTO` standards.
- Bearing capacity analysis can be performed, both from results obtained from **laboratory** or **field**.
- Estimates important soil engineering properties.
- Settlement analysis tools to predict and model soil settlements under various loads and conditions.
- Supports finite element modelling of soil behaviour under different conditions.

.. contents::
.. ## Table of Contents

.. - [Installation](#installation)
.. - [Usage Example](#usage-example)
.. - [Release History](#release-history)
.. - [Contributing](#contributing)
.. - [License](#license)
.. - [Contact Information](#contact-information)
.. - [Links](#links)
.. - [Todo](#todo)

## Installation

.. note::

This install does not work yet. Project is still under **rapid** development.

.. code::

pip install geolab

## Usage example

```python

# >>> from geolab.soil_classifier import unified_soil_classification, aashto_soil_classification
# >>> unified_soil_classification(liquid_limit=34.1, plastic_limit=21.1, plasticity_index=13, fines=47.88, sand=37.84, gravels=14.28)
# >>> 'SC'
# >>> aashto(liquid_limit=34.1, plastic_limit=21.1, plasticity_index=13, fines=47.88)
# >>> 'A-6(3)' -->

```

## Release History

- 0.1.0
  - **rapid** development.

## Contributing

1. [Fork it](https://github.com/patrickboateng/geolab/fork)
1. Create your feature branch (`git checkout -b feature`)
1. Commit your changes (`git commit -am 'Add some fooBar'`)
1. Push to the branch (`git push origin feature`)
1. Create a new Pull Request

## License

Distributed under the `MIT license`. See `LICENSE <./LICENSE.txt>`\_ for more information.

## Contact Information

- Email: <boatengpato.pb@gmail.com>,
- LinkedIn: <https://linkedin.com/in/patrickboateng/>

_For questions or comments about `geolab`, please contact <boatengpato.pb@gmail.com>_

## Links

- [Documentation](https://)
- [PyPi](https://)
- [Source Code](https://github.com/patrickboateng/geolab/)
- [Issue Tracker](https://)
- [Website](https://)

## Todo

- [x] Soil Classifier
- [x] Bearing Capacity Analysis
- [x] Estimating Soil Engineering Parameters
- [ ] Settlement Analysis
- [ ] Modelling the behavior of Soils under loads using `FEM`
