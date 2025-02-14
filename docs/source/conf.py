# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath("../.."))

import geolysis

PACKAGE_VERSION = geolysis.__version__

project = "geolysis"
copyright = f"{datetime.today().year}, {project}"
author = "Patrick Boateng"
version = release = PACKAGE_VERSION

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autodoc.typehints",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
    "sphinx.ext.graphviz",
    "sphinx.ext.inheritance_diagram",
    # Third Party Libraries
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
    "notfound.extension",
    "enum_tools.autoenum",
]

templates_path = ["_templates"]
exclude_patterns = ["build"]

# Sphinx AutoDoc
# autodoc_member_order = "bysource"
autoclass_content = "both"

# adds this string to the start of every .rst file
rst_prolog = """.. include:: <isonum.txt>"""

# # Sphinx Copybutton
# copybutton_prompt_text = (
#     r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: |C:\\> "
# )
# copybutton_prompt_is_regexp = True

# Myst
myst_heading_anchors = 6

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
logo_path = "./_static/branding/"
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_logo = logo_path + "geolysislogoicon.svg" 
html_favicon = logo_path + "geolysislogoicon.svg" 
html_title = project
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css",
    "custom.css",
]
html_js_files = ["pypi-icon.js"]

mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
