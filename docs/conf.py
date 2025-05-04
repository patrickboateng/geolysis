# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(".."))

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
    # Custom Extensions
    "_ext.pyver",
    # Third Party Libraries
    "sphinx_design",
    "myst_parser",
    "enum_tools.autoenum",
    "nbsphinx",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
]

# Custom Extension Config
python_docs_url = "https://docs.python.org/3/whatsnew"

source_suffix = [".rst", ".md", "ipynb"]

templates_path = ["_templates"]
exclude_patterns = ["build"]

# Sphinx AutoDoc Ext
autodoc_default_options = {"exclude-members": "__init__",
                           "class-doc-from": "both",
                           "undoc-members": False}
autodoc_member_order = "bysource"

# Sphinx Autosummary Ext
autosummary_generate = False
autosummary_ignore_module_all = True

# adds this string to the start of every .rst file
rst_prolog = """.. include:: <isonum.txt>"""

# Myst
myst_heading_anchors = 6

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
logo_path = "_static/branding/"
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
html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": f"https://github.com/patrickboateng/{project}",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
        {
            "name": "PyPI",
            "url": f"https://pypi.org/project/{project}",
            "icon": "fa-custom fa-pypi",
            "type": "fontawesome",
        },
    ],
    "secondary_sidebar_items": ["page-toc", "edit-this-page"],
    "footer_start": ["copyright"],
    "footer_center": ["sphinx-version"],
    "footer_end": ["theme-version"],
}

mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
