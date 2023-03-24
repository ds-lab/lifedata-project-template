import os
import subprocess
import sys
from typing import List

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

# We make the root of the repository the documentation root. That way we are
# free to include files located in the respective module directories.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "sphinx"))

# List all subfolders of {{cookiecutter.project_name}}
project_name = "{{cookiecutter.project_name}}"
dirs = [
    dI
    for dI in os.listdir(
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), project_name
        )
    )
    if os.path.isdir(
        os.path.join(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                project_name,
            ),
            dI,
        )
    )
]
# Append all folders of {{cookiecutter.project_name}}  to sys path
for dir in dirs:
    sys.path.append(
        os.path.join(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                project_name,
            ),
            dir,
        )
    )
sys.path.append(
    os.path.join(
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), project_name
        )
    )
)


# -- Project information -----------------------------------------------------

project = "{{cookiecutter.project_name}}"
copyright = "your_copyright"
author = "author"

# The full version, including alpha/beta/rc tags

version = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("ascii")
release = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("ascii")

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "m2r2",
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "nbsphinx",
    "sphinx.ext.graphviz",
    "sphinxcontrib.plantuml",
]

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": True,
}

always_document_param_types = True

# Add any paths that contain templates here, relative to this directory.
# This is not used yet. If you need to add a template, create the directory
# and uncomment the following line.
# "_templates"
templates_path: List[str] = []

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_title = "{{cookiecutter.project_name}}"
html_theme = "sphinx_typlog_theme"

html_theme_options = {
    "logo_name": "{{cookiecutter.project_name}}",
}

html_sidebars = {
    "**": [
        "logo.html",
        "globaltoc.html",
        "searchbox.html",
    ]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = [
    # This is not used yet. If you need to add a template, create the directory
    # and uncomment the following line.
    "_static"
]

html_css_files = [
    "custom.css",
]
