from setuptools import setup, find_packages


def scm_version():
    def local_scheme(version):
        return version.format_choice("+{node}", "+{node}.dirty")
    return {
        "relative_to": __file__,
        "version_scheme": "guess-next-dev",
        "local_scheme": local_scheme,
    }


setup(
    name="torii-boards",
    use_scm_version=scm_version(),
    author="",
    author_email="",
    description="Board and connector definitions for Torii-HDL",
    #long_description="""TODO""",
    license="BSD",
    setup_requires=["wheel", "setuptools", "setuptools_scm"],
    install_requires=[
        "torii-hdl>=0.2,<0.5",
        "importlib_metadata; python_version<'3.8'",
    ],
    packages=find_packages(),
    project_urls={
        "Documentation": "",
        "Source Code": "https://github.com/shrine-maiden-heavy-industries/torii-boards",
        "Bug Tracker": "https://github.com/shrine-maiden-heavy-industries/torii-boards/issues",
    },
)
