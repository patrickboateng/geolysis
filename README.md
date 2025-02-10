<h1 align="center">
<img src="https://raw.githubusercontent.com/patrickboateng/geolysis/dev/docs/source/_static/branding/geolysislogo.svg" 
alt="geolysislogo" width="75%" />
</h1><br>

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
    <td style="vertical-align: top; text-align: left;">
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
    <td style="vertical-align: top; text-align: left;">
    <strong>geolysis.excel</strong>
    </td>
    <td>An add-in for Microsoft Excel that performs simple geotechnical
     analysis. It offers some features similar to <code>geolysis.gui</code>
     within Microsoft Excel.
    </td>
  </tr>
  <tr>
    <td style="vertical-align: top; text-align: left;">
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

**_Note: Work on the latest update is still in progress, so the usage example below
will not function if installed._**

```shell
   pip install geolysis
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
   SoilClf(soil_symbol='SC', soil_description='Clayey sands')
   >>> clf.soil_symbol
   'SC'
   >>> clf.soil_description
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
   SoilClf(soil_symbol='A-6(4)', soil_description='Clayey soils')
   >>> clf.soil_symbol
   'A-6(4)'
   >>> clf.soil_description
   'Clayey soils'

```

## Features

<table>
  <tr>
    <td rowspan="2" style="vertical-align: top; text-align: left;">
    <strong>Soil Classification</strong>
    </td>
    <td>AASHTO Classification System</td>
  </tr>
  <tr>
    <td>Unified Soil Classification System</td>
  </tr>
  <tr>
    <td rowspan="4" style="vertical-align: top; text-align: left;">
    <strong>Standard Penetration Test (SPT) Analysis</strong>
    </td>
    <td>SPT Energy Correction</td>
  </tr>
  <tr>
    <td>SPT Overburden Pressure Correction</td>
  </tr>
  <tr>
    <td>Dilatancy Correction</td>
  </tr>
  <tr>
    <td>SPT N-Design Calculation</td>
  </tr>
  <tr>
    <td rowspan="2" style="vertical-align: top; text-align: left;">
    <strong>Bearing Capacity Estimation</strong>
    </td>
    <td>Allowable Bearing Capacity Estimation</td>
  </tr>
  <tr>
    <td>Ultimate Bearing Capacity Estimation</td>
  </tr>
</table>

## Documentation

Full documentation is available [here](https://www.geolysis.readthedocs.io)

**_Note: Work on the latest documentation is still ongoing._**

## Contributing

## License

This project is licensed under the MIT License - see the
[LICENSE](https://github.com/patrickboateng/geolysis/blob/main/LICENSE.txt)
file for more details.

## Contact

For questions or feedback, please contact us at
[boatengpato.pb@gmail.com](mailto:boatengpato.pb@gmail.com)
