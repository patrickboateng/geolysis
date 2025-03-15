<div align="center">
<img src="https://raw.githubusercontent.com/patrickboateng/geolysis/dev/docs/source/_static/branding/geolysislogo.svg" 
alt="geolysislogo" width="75%" />
</div><br>

<div align="center">

[![PyPI Latest Release](https://img.shields.io/pypi/v/geolysis?style=flat&logo=pypi)](https://pypi.org/project/geolysis/)
[![PyPI Downloads](https://static.pepy.tech/badge/geolysis)](https://pepy.tech/projects/geolysis)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/geolysis.svg?logo=python&style=flat)](https://pypi.python.org/pypi/geolysis/)
[![license](https://img.shields.io/pypi/l/geolysis?style=flat&logo=opensourceinitiative)](https://opensource.org/license/mit/)

![Coveralls Status](https://img.shields.io/coverallsCoverage/github/patrickboateng/geolysis?logo=coveralls)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/17f88084c6a84a08a20f9d8da1438107)](https://app.codacy.com/gh/patrickboateng/geolysis/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Unit-Tests](https://github.com/patrickboateng/geolysis/actions/workflows/geolysis-unit-tests.yml/badge.svg)](https://github.com/patrickboateng/geolysis/actions/workflows/unit-tests.yml)
[![Documentation Status](https://readthedocs.org/projects/geolysis/badge/?version=latest)](https://geolysis.readthedocs.io/en/latest/?badge=latest)

</div>

`geolysis` is an open-source library for geotechnical analysis and modeling.
It offers tools for soil classification, Standard Penetration Test (SPT)
analysis, and bearing capacity estimation, among others.

The `geolysis` library is among four main projects: `geolysis.gui`,
`geolysis.excel`, and `geolysis.ai`. The geolysis library powers all of these
projects.

**_The `geolysis` projects are currently under developement and not yet
publicly available_**.

**_Active development of `geolysis` occurs on the `dev` branch. For more
information on the latest features of `geolysis`, switch to the
`dev` branch_**.

Here are brief descriptions of these projects:

<table>
  <tr>
    <td>
    <strong>geolysis.gui</strong>
    </td>
    <td>A graphical user interface that allows users to interact with the
     geolysis library. Through this interface, users can view generated reports
     and visualizations, such as Particle Size Distribution (PSD) curves,
     Atterberg Limits plots, and Compaction curves, among others.
     Additionally, it enables users to conduct foundation analysis and
     design, among other functionalities.
    </td>
  </tr>
  <tr>
    <td>
    <strong>geolysis.excel</strong>
    </td>
    <td>An add-in for Microsoft Excel that performs simple geotechnical
     analysis. It offers some features similar to <code>geolysis.gui</code>
     within Microsoft Excel.
    </td>
  </tr>
  <tr>
    <td>
    <strong>geolysis.ai</strong>
    </td>
    <td>Offers machine learning models that are trained using geotechnical data.
    </td>
  </tr>
</table>

## Project Structure

    .
    ├── .github        # GitHub Actions
    ├── docs           # Documentation files
    ├── geolysis       # Source files
    ├── tests          # Automated tests
    └── README.md

## Table of Contents

- [Installation](#installation)
- [Usage Example](#usage-example)
- [Features](#features)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

```shell
$ pip install geolysis
```

## Usage Example

```python

>>> from geolysis.soil_classifier import create_soil_classifier
>>> uscs_clf = create_soil_classifier(liquid_limit=34.1,
...                                   plastic_limit=21.1,
...                                   fines=47.88,
...                                   sand=37.84,
...                                   clf_type="USCS")
>>> clf = uscs_clf.classify()
>>> clf
SoilClf(symbol='SC', description='Clayey sands')
>>> clf.symbol
'SC'
>>> clf.description
'Clayey sands'

```

```python

>>> from geolysis.soil_classifier import create_soil_classifier
>>> aashto_clf = create_soil_classifier(liquid_limit=34.1,
...                                     plastic_limit=21.1,
...                                     fines=47.88,
...                                     sand=37.84,  # Sand is optional for AASHTO classification
...                                     clf_type="AASHTO")
>>> clf = aashto_clf.classify()
>>> clf
SoilClf(symbol='A-6(4)', description='Clayey soils')
>>> clf.symbol
'A-6(4)'
>>> clf.description
'Clayey soils'

```

Check out more examples
[here](https://docs.geolysis.io/en/latest/user_guide/getting_started.html#quick-start)

## Features

<table>
    <tr>
        <td><strong>Soil Classification</strong></td>
        <td>AASHTO Classification System</td>
    </tr>
    <tr>
        <td></td>
        <td>Unified Soil Classification System</td>
    </tr>
    <tr>
        <td><strong>Standard Penetration Test (SPT) Analysis</strong></td>
        <td>SPT Energy Correction</td>
    </tr>
    <tr>
        <td></td>
        <td>SPT Overburden Pressure Correction</td>
    </tr>
    <tr>
        <td></td>
        <td>Dilatancy Correction</td>
    </tr>
    <tr>
        <td></td>
        <td>SPT N-Design Calculation</td>
    </tr>
    <tr>
        <td><strong>Bearing Capacity Estimation</strong></td>
        <td>Allowable Bearing Capacity Estimation</td>
    </tr>
    <tr>
        <td></td>
        <td>Ultimate Bearing Capacity Estimation</td>
    </tr>
</table>

## Documentation

Full documentation is available [here](https://docs.geolysis.io/en/latest/)

## Contributing

Contribution guidelines can be
found [here](https://docs.geolysis.io/en/latest/dev_guide/index.html)

## License

This project is licensed under the MIT License - see the
[LICENSE](https://github.com/patrickboateng/geolysis/blob/main/LICENSE.txt)
file for more details.

## Contact

For questions or feedback, please contact us at
[boatengpato.pb@gmail.com](mailto:boatengpato.pb@gmail.com)
