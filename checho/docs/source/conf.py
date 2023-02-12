# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import django
sys.path.insert(0, os.path.abspath('../../../'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'barberia.settings'
django.setup()

project = 'barberia'
copyright = '2022, Juan Urrutia -  Cristian Arboleda'
author = 'Juan Urrutia -  Cristian Arboleda'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
        'sphinx.ext.intersphinx',
        'sphinx.ext.todo',
        'sphinx.ext.mathjax',
        'sphinx.ext.napoleon',
        'sphinx.ext.autosummary', # solamente si se la quiere usar
        'sphinx.ext.viewcode']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'nature'
html_static_path = ['_static']
html_sidebars = { '**': ['globaltoc.html', 'relations.html',
        'sourcelink.html', 'searchbox.html'], }