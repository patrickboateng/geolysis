# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "geolab"
copyright = "2023, Patrick Boateng"
author = "Patrick Boateng"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.doctest", "sphinxcontrib.bibtex"]

templates_path = ["_templates"]
exclude_patterns = []

# -- References ------------------------------
# https://sphinxcontrib-bibtex.readthedocs.io/en/latest/quickstart.html
bibtex_bibfiles = ["refs.bib"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
