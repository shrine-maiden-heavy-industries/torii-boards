# SPDX-License-Identifier: BSD-3-Clause

import shutil
from pathlib        import Path
from setuptools_scm import (
	get_version, ScmVersion
)

import nox

ROOT_DIR  = Path(__file__).parent

BUILD_DIR = (ROOT_DIR  / 'build')
DOCS_DIR  = (ROOT_DIR  / 'docs')
DIST_DIR  = (BUILD_DIR / 'dist')


# Default sessions to run
nox.options.sessions = (
	'test',
	'flake8',
	'mypy'
)

def torii_boards_version() -> str:
	def scheme(version: ScmVersion) -> str:
		if version.tag and not version.distance:
			return version.format_with('')
		else:
			return version.format_choice('+{node}', '+{node}.dirty')

	return get_version(
		root           = str(ROOT_DIR),
		version_scheme = 'guess-next-dev',
		local_scheme   = scheme,
		relative_to    = __file__
	)

@nox.session(reuse_venv = True)
def test(session: nox.Session) -> None:
	session.install(
		'git+https://github.com/shrine-maiden-heavy-industries/torii-hdl.git#egg=torii'
	)
	session.install('.')
	session.run(
		'python', '-m', 'unittest', 'discover',
		'-s', '.'
	)

@nox.session
def docs(session: nox.Session) -> None:
	out_dir = (BUILD_DIR / 'docs')
	shutil.rmtree(out_dir, ignore_errors = True)
	session.install('-r', str(DOCS_DIR / 'requirements.txt'))
	session.install(
		'git+https://github.com/shrine-maiden-heavy-industries/torii-hdl.git#egg=torii'
	)
	session.install('.')
	session.run('sphinx-build', '-b', 'html', str(DOCS_DIR), str(out_dir))

@nox.session
def mypy(session: nox.Session) -> None:
	out_dir = (BUILD_DIR / 'mypy')
	session.install('mypy')
	session.install('lxml')
	session.install(
		'git+https://github.com/shrine-maiden-heavy-industries/torii-hdl.git#egg=torii'
	)
	session.install('.')
	session.run(
		'mypy', '--non-interactive', '--install-types',
		'-p', 'torii_boards', '--html-report', str(out_dir.resolve())
	)

@nox.session
def flake8(session: nox.Session) -> None:
	session.install('flake8')
	session.run('flake8', './torii_boards')

@nox.session
def build_dists(session: nox.Session) -> None:
	session.install('build')
	session.run('python', '-m', 'build',
		'-o', str(DIST_DIR)
	)

@nox.session
def upload_dist(session: nox.Session) -> None:
	session.install('twine')
	build_dists(session)
	session.log('Uploading to PyPi')
	session.run('python', '-m', 'twine',
		'upload', f'{DIST_DIR}/*'
	)
