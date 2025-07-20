import os
import sys

sys.path.insert(0, os.path.abspath('..'))

project = 'wove'

extensions = [
    'myst_parser',
]

html_theme = 'furo'

exclude_patterns = ['_build']

html_static_path = ['_static']
