[code_of_conduct_url]: https://github.com/patrickboateng/geolysis/blob/main/CODE_OF_CONDUCT.md/
[contributing_url]: https://github.com/patrickboateng/geolysis/blob/main/docs/CONTRIBUTING.md#how-to-contribute
[license_url]: https://github.com/patrickboateng/geolysis/blob/main/LICENSE.txt

# geolysis

<div align="center">

[![PyPI Latest Release](https://img.shields.io/pypi/v/geolysis?style=flat&logo=pypi)](https://pypi.org/project/geolysis/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/geolysis.svg?logo=python&style=flat)](https://pypi.python.org/pypi/geolysis/)
[![license](https://img.shields.io/pypi/l/geolysis?style=flat&logo=opensourceinitiative)](https://opensource.org/license/mit/)

![Coveralls Status](https://img.shields.io/coverallsCoverage/github/patrickboateng/geolysis?logo=coveralls)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/17f88084c6a84a08a20f9d8da1438107)](https://app.codacy.com/gh/patrickboateng/geolysis/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Unit-Tests](https://github.com/patrickboateng/geolysis/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/patrickboateng/geolysis/actions/workflows/unit-tests.yml)
[![Pkg Build](https://github.com/patrickboateng/geolysis/actions/workflows/pkg_build.yml/badge.svg)](https://github.com/patrickboateng/geolysis/actions/workflows/pkg_build.yml)
[![Documentation Status](https://readthedocs.org/projects/geolysis/badge/?version=latest)](https://geolysis.readthedocs.io/en/latest/?badge=latest)

</div>

#

> [!NOTE]
> Active development of `geolysis` occurs on the `dev` branch. For more
> information for the lastest features of `geolysis`, switch to the
> `dev` branch.

`geolysis` is your one-stop shop for all your geotechnical engineering
solutions, ranging from site investigation and laboratory test analysis
to advanced geotechnical designs.

`geolysis` is divided into four (4) main parts:

1. `geolyis.core (Python)`

   `geolysis.core` is an open-source Python package that provides features
   for analyzing geotechnical results obtained from field and laboratory
   tests. `geolysis.core` is designed specifically to assist developers
   in building applications that can solve complex geotechnical
   problems.

   Whether you're working on soil mechanics, rock mechanics, or any other
   geotechnical field, `geolysis.core` provides a powerful set of tools
   that can help you design and develop robust solutions. With an
   intuitive API and a wide range of features, this software is an
   essential tool for anyone who needs to work with geotechnical data on
   a regular basis. Whether you're a seasoned geotechnical engineer or a
   new developer just getting started in the field, `geolysis.core` is
   the ideal solution for all your software development needs.

   Some of the features implemented so far include soil classification,
   standard penetration test analysis (such as SPT N-design and SPT
   N-value corrections), and calculating the allowable bearing capacity of
   soils from Standard Penetration Test N-values. There are more features
   underway, which include settlement analysis, ultimate bearing capacity
   analysis, etc.

   `geolysis.core` is the foundation application on which other parts of the
   application will depend. Developers can also use `geolysis.core` to power
   their applications.

1. `geolysis.ui (Qt, PySide6)`

   `geolysis.ui` is a Graphical User Interface (GUI) which will enable
   users to graphically interact with `geolysis`. User will be able to
   input data and view generated plots, such as `PSD` curves,
   `Atterberg Limits` plots, `Compaction` curves, etc within the application.

1. `geolysis.excel (Javascript & Others)`

   `geolysis.excel` provides a Microsoft Excel add-in for simple geotechnical
   analysis. _More on this later._

1. `geolysis.ai (Python, Pytorch & Others)`

   `geolysis.ai` explores the use of Artificial Intelligence (**AI**) in
   enhancing productivity in Geotechnical Engineering.

Lastly `geolysis.docs` is the documentation project for `geolysis`.

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

`geolysis` is a software solution that aims to support geotechnical
engineers in their daily work by providing a set of tools that makes
them perform their tasks in a more efficient and effective manner.
Moreover, the platform is designed to educate civil engineering
students, especially those who specialize in geotechnical engineering,
by exposing them to industry-relevant tools and techniques that will
help them become industry-ready professionals as soon as they graduate.
With `geolysis`, users will be better equipped to handle geotechnical
challenges, make informed decisions, and improve their overall
productivity.

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
>>> aashto_cls.classify()
'A-2-4(0)'
>>> aashto_cls.description()
'Silty or clayey gravel and sand'

```

USCS Classification

```python

>>> from geolysis.core.soil_classifier import USCS, AtterbergLimits, PSD, SizeDistribution
>>> al = AtterbergLimits(liquid_limit=34.1, plastic_limit=21.1)
>>> psd = PSD(fines=47.88, sand=37.84)
>>> uscs_cls = USCS(atterberg_limits=al, psd=psd)
>>> uscs_cls.classify()
'SC'
>>> uscs_cls.description()
'Clayey sands'

>>> al = AtterbergLimits(liquid_limit=30.8, plastic_limit=20.7)
>>> size_dist = SizeDistribution(d_10=0.07, d_30=0.3, d_60=0.8)
>>> psd = PSD(fines=10.29, sand=81.89, size_dist=size_dist)
>>> uscs_cls = USCS(atterberg_limits=al, psd=psd)
>>> uscs_cls.classify()
'SW-SC'
>>> uscs_cls.description()
'Well graded sand with clay'

```

<!-- See the [Quick start section] of the docs for more examples. -->

## Release History

Check out the [release notes](https://geolysis.rtfd.io/en/latest/release_notes/index.html)
for features.

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
Once `geolysis.core` hits `1.0.0`, it will slow down considerably.

## Contact Information

- [**LinkedIn**](https://linkedin.com/in/patrickboateng/)

> [!IMPORTANT]
> For questions or comments about `geolysis`, please ask them in the
> [discussions forum](https://github.com/patrickboateng/geolysis/discussions)
