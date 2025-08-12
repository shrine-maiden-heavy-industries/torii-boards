# SPDX-License-Identifier: BSD-2-Clause
from datetime     import date
from pathlib      import Path

from torii        import __version__ as torii_version
from torii_boards import __version__ as boards_version

ROOT_DIR = (Path(__file__).parent).parent

project = 'Torii-HDL Boards'
version = boards_version
release = version.split('+')[0]
copyright = f'{date.today().year}, Shrine Maiden Heavy Industries'
language  = 'en'
docver    = version

extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.extlinks',
	'sphinx.ext.githubpages',
	'sphinx.ext.intersphinx',
	'sphinx.ext.napoleon',
	'sphinx.ext.todo',
	'myst_parser',
	'sphinx_autodoc_typehints',
	'sphinx_codeautolink',
	'sphinx_copybutton',
	'sphinx_inline_tabs',
	'sphinx_multiversion',
	'sphinxext.opengraph',
]

source_suffix = {
	'.rst': 'restructuredtext',
	'.md': 'markdown',
}

extlinks = {
	'issue': ('https://github.com/shrine-maiden-heavy-industries/torii-boards/issues/%s', 'torii-boards/%s'),
	'pypi':  ('https://pypi.org/project/%s/', '%s'),
}

pygments_style              = 'default'
pygments_dark_style         = 'monokai'
autodoc_member_order        = 'bysource'
autodoc_docstring_signature = False
todo_include_todos          = True

intersphinx_mapping = {
	'python': ('https://docs.python.org/3', None),
	'torii': (f'https://torii.shmdn.link/v{torii_version}', None)
}

napoleon_google_docstring              = False
napoleon_numpy_docstring               = True
napoleon_use_ivar                      = True
napoleon_use_admonition_for_notes      = True
napoleon_use_admonition_for_examples   = True
napoleon_use_admonition_for_references = True
napoleon_custom_sections  = [
	('Attributes', 'params_style'),
	'Platform overrides'
]

myst_heading_anchors = 3

always_use_bars_union = True
typehints_defaults = 'braces-after'
typehints_use_signature = True
typehints_use_signature_return = True

templates_path = [
	'_templates',
]

html_baseurl     = 'https://torii-boards.shmdn.link/'
html_theme       = 'furo'
html_copy_source = False

html_theme_options = {
	'announcement': 'This documentation is a work in progress, and you can help us <a href="https://github.com/shrine-maiden-heavy-industries/torii-boards/blob/main/CONTRIBUTING.md">improve it!</a>', # noqa: E501
	'light_css_variables': {
		'color-brand-primary': '#2672a8',
		'color-brand-content': '#2672a8',
		'color-announcement-background': '#ffab87',
		'color-announcement-text': '#494453',
	},
	'dark_css_variables': {
		'color-brand-primary': '#85C2FE',
		'color-brand-content': '#85C2FE',
		'color-announcement-background': '#ffab87',
		'color-announcement-text': '#494453',
	},
	'source_repository': 'https://github.com/shrine-maiden-heavy-industries/torii-boards/',
	'source_branch': 'main',
	'source_directory': 'docs/',
}

html_static_path = [
	'_static'
]

html_sidebars = {
	"**": [
		"sidebar/brand.html",
		"sidebar/search.html",
		"sidebar/scroll-start.html",
		"sidebar/navigation.html",
		"sidebar/version_selector.html",
		"sidebar/scroll-end.html",
	]
}

html_css_files = [
	'css/styles.css'
]

# TODO(aki): OpenGraph metadata stuff
ogp_site_url = html_baseurl
ogp_social_cards = {}
ogp_image = None
ogp_image_alt = None
ogp_custom_meta_tags = list[str]()
ogp_enable_meta_description = True

linkcheck_retries = 2
linkcheck_workers = 1 # At the cost of speed try to prevent rate-limiting
linkcheck_ignore  = [
	'https://www.intel.com/content/www/us/en/products/details/fpga/development-tools/quartus-prime.html',
	'https://www.xilinx.com/products/design-tools/ise-design-suite.html',
	'https://www.xilinx.com/products/design-tools/vivado.html',
	# Digilent is being a big meanie
	'https://digilent.com/reference/programmable-logic/genesys-2/start',
	'https://digilent.com/reference/programmable-logic/atlys/start',
	# SSL Timeout from GitHub actions
	'https://aur.archlinux.org',
]
linkcheck_anchors_ignore_for_url = [
	r'^https://web\.libera\.chat/',
]

# Sphinx-Multiversion stuff
# TODO(aki): Revert to `^v(?!0)\d+\.\d+\.\d+$` when `v1.0.0` drops, we need to gen the v0.8.0 stable for now
smv_tag_whitelist    = r'^v\d+\.(?![1-7])\d+\.\d+$' # Ignore all `v0.[1-7].x` versions
smv_branch_whitelist = r'^main$'                    # Only look at `main`
smv_remote_whitelist = r'^origin$'
smv_released_pattern = r'^refs/tags/v.+$'           # Only consider tags to be full releases
smv_outputdir_format = '{ref.name}'
