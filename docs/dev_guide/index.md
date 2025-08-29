# Developer Documentation

This page provides an overview of how the project is organized for both the
source code and documentation.

## Layout of Project's Source Code

The `geolysis` folder contains all the source code for the project, and it is
the root (main package namespace) of the project.

- `bearing_capacity` package (folder) contains the code for bearing
  capacity analysis.
- `foundation.py` module (file) contains classes for representing a foundation.
- `soil_classifier.py` module (file) contains classes for soil classification.
- `spt.py` module (file) contains classes for Standard Penetration Test Analysis.
- `utils` package (folder) contains useful objects (functions, decorators, etc.) 
  that are used across the project.

## Layout of Project's Documentation

The `docs` folder contains all the documentation files for the project.

- `api` folder contains the API (code) reference for `geolysis`.
- `assets` folder contain images used for the docs website (e.g. logo).
- `dev_guide` folder contains information for contributors.
- `release_notes` folder contains all the release notes for `geolysis`.
- `index.md` is the landing page for the documentation.
- `usage.md` file contains information for users.

All (or most) of the other files found in the root of the `geolysis` and
`docs` folders are metadata/configuration files.

