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
copyright = f"{datetime.now().year}, {project}"
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
    "sphinxcontrib.bibtex",
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
    "autoapi.extension",
    # "jupyter_sphinx",
    # "enum_tools.autoenum",
]

templates_path = ["_templates"]
exclude_patterns = ["build"]

rst_prolog = """.. include:: <isonum.txt>"""  # adds this string to the start of every .rst file


# -- References ------------------------------
# https://sphinxcontrib-bibtex.readthedocs.io/en/latest/quickstart.html

bibtex_bibfiles = ["./citations/refs.bib", "./citations/article.bib"]
bibtex_default_style = "unsrt"

# --- API Documentation --------------------
# https://sphinx-autoapi.readthedocs.io/en/latest/tutorials.html

autoapi_dirs = ["../../geolysis"]
autoapi_root = "reference/"
autoapi_add_toctree_entry = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = "pydata_sphinx_theme"
html_logo = "_static/geolysis_logo.png"
html_favicon = "_static/logo.png"
html_title = project
html_static_path = ["_static"]
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css",
    "custom.css",
]
html_context = {"default_mode": "light"}

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

if os.environ.get("READTHEDOCS"):
    from pathlib import Path

    PROJECT_ROOT = Path(__file__).parent.parent
    PACKAGE_ROOT = PROJECT_ROOT / project

    def run_apidoc():
        from sphinx.ext import apidoc

        apidoc.main(
            [
                "--force",
                "implicit-namespaces",
                "--module-first",
                "--separate",
                "-o",
                str(PROJECT_ROOT / "docs" / "reference"),
                str(PACKAGE_ROOT),
            ]
        )

    def setup(app):
        app.connect("builder-inited", run_apidoc)
