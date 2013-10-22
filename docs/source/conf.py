# -*- coding: utf-8 -*-

import os
import sys

# always use relative module (current path would be docs' source dir)
pardir = os.path.pardir
abspath = lambda *p: os.path.abspath(os.path.join(*p))
sys.path.insert(0, abspath(pardir, pardir))

# required by Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'zeusci.testsettings'

zeusci = __import__('zeusci')


# -- General configuration -----------------------------------------------------

extensions = []
templates_path = ['.templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'zeus-ci'
copyright = u'2013, Lukasz Balcerzak'

# The short X.Y version.
version = zeusci.get_version(full=False)
# The full version, including alpha/beta/rc tags.
release = zeusci.get_version(full=True)

exclude_patterns = []
pygments_style = 'sphinx'

# -- Options for HTML output ---------------------------------------------------

html_theme = 'default'
html_static_path = ['.static']
htmlhelp_basename = 'zeus-cidoc'

# -- Options for LaTeX output --------------------------------------------------

latex_elements = {}
latex_documents = [
  ('index', 'zeus-ci.tex', u'zeus-ci Documentation',
   u'Lukasz Balcerzak', 'manual'),
]

# -- Options for manual page output --------------------------------------------

man_pages = [
    ('index', 'zeus-ci', u'zeus-ci Documentation',
     [u'Lukasz Balcerzak'], 1)
]

# -- Options for Texinfo output ------------------------------------------------

texinfo_documents = [
  ('index', 'zeus-ci', u'zeus-ci Documentation',
   u'Lukasz Balcerzak', 'zeus-ci', 'One line description of project.',
   'Miscellaneous'),
]

