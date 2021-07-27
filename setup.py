import os
import io
from setuptools import setup, find_packages


# Helpers


def read(*paths):
    """Read a text file."""
    basedir = os.path.dirname(__file__)
    fullpath = os.path.join(basedir, *paths)
    contents = io.open(fullpath, encoding="utf-8").read().strip()
    return contents


# Prepare


PACKAGE = "livemark"
NAME = PACKAGE.replace("_", "-")
TESTS_REQUIRE = [
    "mypy",
    "black",
    "pylama",
    "pytest",
    "ipython",
    "pytest-cov",
    "pytest-vcr",
    "pytest-only",
]
EXTRAS_REQUIRE = {
    "dev": TESTS_REQUIRE,
}
INSTALL_REQUIRES = [
    "marko>=1.0",
    "pyyaml>=5.3",
    "jinja2>=3.0",
    "pyquery>=1.4",
    "deepmerge>=0.3",
    "gitpython>=3.1",
    "jsonschema>=2.5",
    "typer[all]>=0.3",
    "livereload>=2.6",
    "giturlparse>=0.10",
    "frictionless[excel,json]==4.*",
]
README = read("README.md")
VERSION = read(PACKAGE, "assets", "VERSION")
PACKAGES = find_packages(exclude=["tests"])
ENTRY_POINTS = {"console_scripts": ["livemark = livemark.__main__:program"]}


# Run


setup(
    name=NAME,
    version=VERSION,
    packages=PACKAGES,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require=EXTRAS_REQUIRE,
    entry_points=ENTRY_POINTS,
    zip_safe=False,
    long_description=README,
    long_description_content_type="text/markdown",
    description="Livemark is a static site generator that extends Markdown with interactive charts, tables, scripts, and more.",
    author="Evgeny Karev",
    author_email="eskarev@gmail.com",
    url="https://github.com/frictionlessdata/livemark",
    license="MIT",
    keywords=[
        "livemark",
        "markdown",
        "documentation",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
