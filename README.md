<h1 align="center">
<img src="https://raw.githubusercontent.com/patrickboateng/geolysis/dev/branding/geolysislogo.svg" 
alt="geolysislogo" width="85%" />
</h1><br>

geolysis is an open-source library for geotechnical analysis and modeling. It
offers tools for soil classification, Standard Penetration Test (SPT) analysis,
and bearing capacity estimation, among others.

The geolysis library is among four main projects: `geolysis.gui`,
`geolysis.excel`, and `geolysis.ai`. The geolysis library powers all of these
projects.

**_The `geolysis` projects are currently under developement and not yet
publicly available_**.

**_Active development of `geolysis` occurs on the `dev` branch. For more
information on the latest features of `geolysis`, switch to the
`dev` branch_**.

Here are brief descriptions of these projects:

- `geolysis.gui` is a graphical user interface that allows users to interact
  with the geolysis library. Through this interface, users can view generated
  reports and visualizations, such as Particle Size Distribution (PSD) curves,
  Atterberg Limits plots, and Compaction curves, among others. Additionally,
  it enables users to conduct foundation analysis and design, among other
  functionalities.

- `geolysis.excel` is an add-in for Microsoft Excel that performs simple
  geotechnical analysis. It offers some features similar to `geolysis.gui`
  within Microsoft Excel.

- `geolysis.ai` offers machine learning models that are trained using
  geotechnical data.

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

- **Soil Classification**

  - AASHTO Classification System
  - Unified Soil Classification System

- **Standard Penetration Test (SPT) Analysis**

  - SPT Energy Correction
  - SPT Overburden Pressure Correction
  - Dilatancy Correction
  - SPT N-Design Calculation

- **Bearing Capacity Estimation**

  - Allowable Bearing Capacity Estimation
  - Ultimate Bearing Capacity Estimation

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
