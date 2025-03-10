# SPDX-License-Identifier: BSD-2-Clause
import datetime
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath('.'))

from torii_boards import __version__ as boards_version

ROOT_DIR = (Path(__file__).parent).parent


project = 'Torii-HDL Boards'
version = boards_version
release = version.split('+')[0]
copyright = f'{datetime.date.today().year}, Shrine Maiden Heavy Industries'
language  = 'en'
docver    = version

extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.doctest',
	'sphinx.ext.githubpages',
	'sphinx.ext.intersphinx',
	'sphinx.ext.napoleon',
	'sphinx.ext.todo',
	'sphinxcontrib.platformpicker',
	'myst_parser',
	'sphinx_rtd_theme',
]

with open(".gitignore") as f:
	exclude_patterns = [line.strip() for line in f.readlines()]

source_suffix = {
	'.rst': 'restructuredtext',
	'.md': 'markdown',
}

pygments_style         = 'monokai'
autodoc_member_order   = 'bysource'
graphviz_output_format = 'svg'
todo_include_todos     = True

intersphinx_mapping = {
	'python': ('https://docs.python.org/3', None),
	'torii': ('https://torii.shmdn.link/', None)
}


napoleon_google_docstring = False
napoleon_numpy_docstring  = True
napoleon_use_ivar         = True
napoleon_custom_sections  = [
	'Platform overrides'
]

myst_heading_anchors = 3

templates_path = [
	'_templates',
]


html_context = {
	'display_lower_left': False,
	'current_language'  : language,
	'current_version'   : version,
	'version'           : version,
	'display_github'    : True,
	'github_user'       : 'shrine-maiden-heavy-industries',
	'github_repo'       : 'torii-boards',
	'github_version'    : 'main/docs/',
	'versions'          : [
		('latest', '/latest')
	]
}

html_baseurl     = 'https://torii-boards.shmdn.link/'
html_theme       = 'sphinx_rtd_theme'
html_copy_source = False

html_theme_options = {
	'collapse_navigation' : False,
	'style_external_links': True,
}

html_static_path = [
	'_static'
]

html_css_files = [
	'css/styles.css'
]

html_style = 'css/styles.css'

linkcheck_ignore = [
	'https://www.intel.com/content/www/us/en/products/details/fpga/development-tools/quartus-prime.html',
	'https://www.xilinx.com/products/design-tools/ise-design-suite.html',
	'https://www.xilinx.com/products/design-tools/vivado.html',
	# Digilent is being a big meanie
	'https://digilent.com/reference/programmable-logic/genesys-2/start',
	'https://digilent.com/reference/programmable-logic/atlys/start',
]
