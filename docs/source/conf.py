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
    "numpydoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.graphviz",
    "sphinx.ext.inheritance_diagram",
    # Third Party Libraries
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
    "autoapi.extension",
    "notfound.extension",
    # "enum_tools.autoenum",
]

templates_path = ["_templates"]
exclude_patterns = ["build"]


# Sphinx AutoDoc
autodoc_member_order = "bysource"

# adds this string to the start of every .rst file
rst_prolog = """.. include:: <isonum.txt>"""


# Sphinx AutoAPI
autoapi_dirs = ["../../geolysis/core"]
autoapi_root = "reference"
autoapi_add_toctree_entry = False
autoapi_template_dir = "_templates/_autoapi_templates"
autoapi_options = [
    "members",
    "undoc-members",
    # "private-members",
    # "show-inheritance",
    # "show-module-summary",
    # "special-members",
    # "imported-members",
]
# autoapi_generate_api_docs = False

# Sphinx Copybutton
copybutton_prompt_text = (
    r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: |C:\\> "
)
copybutton_prompt_is_regexp = True

# Myst
myst_heading_anchors = 6

# NumPyDoc
numpydoc_attributes_as_param_list = False
# numpydoc_show_class_members = False
numpydoc_class_members_toctree = False
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# logo_path = "_static/logo.png"
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
# html_logo = logo_path
# html_favicon = logo_path
html_title = project
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css",
    "custom.css",
]
html_js_files = ["pypi-icon.js"]
html_context = {"default_mode": "light"}

# Define the json_url for our version switcher
json_url = "https://geolysis.readthedocs.io/en/latest/_static/switcher.json"
switcher_version = os.environ.get("READTHEDOCS_VERSION")

# latest == main
switcher_version = "dev" if switcher_version == "latest" else f"v{version}"

html_theme_options = {
    "header_links_before_dropdown": 4,
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
    # "navbar_start": ["navbar-logo"],
    "navbar_align": "content",
    "navbar_end": [
        "search-button",
        "version-switcher",
        "theme-switcher",
        "navbar-icon-links",
    ],
    "navbar_persistent": [],
    "secondary_sidebar_items": ["page-toc", "edit-this-page", "sourcelink"],
    "show_prev_next": False,
    "show_version_warning_banner": True,
    "article_footer_items": ["prev-next"],
    "footer_start": ["copyright"],
    "footer_center": ["sphinx-version"],
    "footer_end": ["theme-version"],
    "switcher": {"json_url": json_url, "version_match": switcher_version},
}

# Primary sidebar items
html_sidebars = {"**": ["sidebar-nav-bs"]}

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
