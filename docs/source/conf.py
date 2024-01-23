# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from importlib import metadata

sys.path.insert(0, os.path.abspath("../.."))


PACKAGE_VERSION = metadata.version("geolysis")

project = "geolysis"
copyright = f"2023, {project}"
author = "Patrick Boateng"
version = release = PACKAGE_VERSION

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
    "sphinxcontrib.bibtex",
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
    "jupyter_sphinx",
    "enum_tools.autoenum",
]

templates_path = ["_templates", "_templates/autosummary"]
exclude_patterns = []

rst_prolog = """.. include:: <isonum.txt>"""  # adds this string to the start of every .rst file


# -- References ------------------------------
# https://sphinxcontrib-bibtex.readthedocs.io/en/latest/quickstart.html

bibtex_bibfiles = ["./refs.bib", "./article.bib"]
bibtex_default_style = "unsrt"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = "pydata_sphinx_theme"
html_logo = "_static/geolysis_logo.png"
html_favicon = "_static/logo.png"
html_title = project
html_static_path = ["_static"]
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css"
]

html_theme_options = {
    "header_links_before_dropdown": 6,
    "icon_links": [
        {
            "name": "GitHub",
            "url": f"https://github.com/patrickboateng/{project}",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
    ],
}
#     "navbar_align": "left",
#     "navbar_end": ["theme-switcher", "version-switcher", "navbar-icon-links"],
#     # "switcher": {
#     #     "json_url": (
#     #         "https://scikit-image.org/docs/dev/_static/version_switcher.json"
#     #     ),
#     #     "version_match": "dev" if "dev" in release else release,
#     # },
#     # Footer
#     "footer_start": ["copyright"],
#     "footer_end": ["sphinx-version", "theme-version"],
#     # Other
#     "pygment_light_style": "default",
#     "pygment_dark_style": "github-dark",
#     # "analytics": {
#     #     "plausible_analytics_domain": "scikit-image.org",
#     #     "plausible_analytics_url": (
#     #         "https://views.scientific-python.org/js/script.js"
#     #     ),
#     # },
# }

mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
