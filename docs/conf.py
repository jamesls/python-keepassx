# -*- coding: utf-8 -*-

import guzzle_sphinx_theme

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode',
              'guzzle_sphinx_theme']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'keepassx'
copyright = u'2013, James Saryerwinnie'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.0.3'
# The full version, including alpha/beta/rc tags.
release = '0.0.3'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']


# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# Adds an HTML table visitor to apply Bootstrap table classes
html_translator_class = 'guzzle_sphinx_theme.HTMLTranslator'
html_theme_path = guzzle_sphinx_theme.html_theme_path()
html_theme = 'guzzle_sphinx_theme'

html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'keepassxdoc'

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'keepassx', u'keepassx Documentation',
     [u'James Saryerwinnie'], 1)
]


# Guzzle theme options (see theme.conf for more information)
html_theme_options = {

    # Set the name of the project to appear in the nav menu

    # Set you GA account ID to enable tracking
    "google_analytics_account": "UA-28869503-3",

    # Path to a touch icon
    "touch_icon": "",

    # Specify a base_url used to generate sitemap.xml links. If not
    # specified, then no sitemap will be built.
    "base_url": "http://keepassx.readthedocs.org/en/latest/"
}
