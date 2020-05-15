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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "Andrea Esposito's Bachelor's Degree Thesis"
copyright = '2020, Andrea Esposito'
author = 'Andrea Esposito'
version = 'latest'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'breathe',
    'sphinx_js',
    'sphinx_rtd_theme',
    'sphinxcontrib.httpdomain'
]

# Setup the breathe extension
breathe_projects = {
    "emotions-tool": "./doxygen/emotions"
}
breathe_default_project = "emotions-tool"

# Setup the sphinx_js extension
root_for_relative_js_paths = '..'
js_source_path = [
    '../server/src/',
    '../extension/src/',
]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_logo = '_static/logo.svg'

html_theme_options = {
    #     'canonical_url': '',
    #     'analytics_id': 'UA-XXXXXXX-1',  #  Provided by Google in your dashboard
    'logo_only': True,
    'display_version': True,
    #     'prev_next_buttons_location': 'bottom',
    #     'style_external_links': False,
    #     'vcs_pageview_mode': '',
    #     'style_nav_header_background': 'white',
    #     # Toc options
    #     'collapse_navigation': True,
    #     'sticky_navigation': True,
    #     'navigation_depth': 4,
    #     'includehidden': True,
    #     'titles_only': False
}

# List of tuples:
# (source file, target name, title, author, document class [howto/manual], False).
latex_documents = [
    ('documentation', 'documentation.tex', "Technical Documentation",
     'Andrea Esposito', 'manual', False),
]
latex_use_modindex = True
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'preamble': r'''
        \usepackage{hyperref}
        \setcounter{tocdepth}{3}
        \addto\captionsenglish{\renewcommand{\contentsname}{Table of contents}}
    ''',
    'figure_align': 'htbp',
}
