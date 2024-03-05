# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from datetime import date, datetime

sys.path.insert(0, os.path.abspath("../.."))

import geolysis

PACKAGE_VERSION = geolysis.__version__
today = datetime.now()

project = "geolysis"
copyright = f"2023 - {today.year}, {project}"
author = "Patrick Boateng"
version = release = PACKAGE_VERSION

_today = today.strftime("%d-%b-%Y")

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
    # Third Party
    "sphinx_copybutton",
    "sphinx_design",
    # "sphinx_tabs.tabs",
    "sphinxcontrib.bibtex",
    "myst_parser",
    # "jupyter_sphinx",
    # "enum_tools.autoenum",
]

templates_path = ["_templates"]
exclude_patterns = ["build"]

rst_prolog = """.. include:: <isonum.txt>"""  # adds this string to the start of every .rst file

# -- References ------------------------------
# https://sphinxcontrib-bibtex.readthedocs.io/en/latest/quickstart.html

bibtex_bibfiles = ["./citations/book.bib", "./citations/article.bib"]
bibtex_default_style = "unsrt"

# --- Sphinx Tabs --------------------
# https://sphinx-tabs.readthedocs.io/en/latest/

sphinx_tabs_disable_css_loading = True
sphinx_tabs_disable_tab_closing = True

#
#
copybutton_prompt_text = (
    r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
)
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_logo = "_static/geolysis_logo.png"
html_favicon = "_static/logo.png"
html_title = project
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css",
    "custom.css",
]
html_context = {"default_mode": "dark"}

html_theme_options = {
    "header_links_before_dropdown": 6,
    # "icon_links": [
    #     {
    #         "name": "GitHub",
    #         "url": f"https://github.com/patrickboateng/{project}",
    #         "icon": "fa-brands fa-github",
    #         "type": "fontawesome",
    #     },
    # ],
    "github_url": f"https://github.com/patrickboateng/{project}",
    "navbar_align": "content",
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "navbar_persistent": [],
    "secondary_sidebar_items": ["page-toc"],
    "show_prev_next": False,
    "article_footer_items": ["prev-next"],
    "footer_start": ["copyright"],
    "footer_center": ["sphinx-version"],
    "footer_end": ["theme-version"],
}

html_sidebars = {"**": ["search-field", "sidebar-nav-bs"]}

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


# def skip_submodules(app, what, name, obj, skip, options):
#     if what.startswith("_"):
#         skip = True
#     return skip


# def setup(sphinx):
#     sphinx.connect("autoapi-skip-member", skip_submodules)
