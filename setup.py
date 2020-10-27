# Setup module for hakilo package.
# Cleve (Klivo) Lendon, 2020-10

import setuptools

with open("README.md", "r") as fin:
    long_description = fin.read()

setuptools.setup(
    name = "hakilo",
    version = "1.0.0",
    author = "Cleve (Klivo) Lendon",
    author_email = "indriko@yahoo.com",
    description = "A tool for splitting a text into sentences.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/Indrikoterio/hakilo-python",
    packages = setuptools.find_packages(),
    package_data = {'hakilo': []},
    include_package_data = True,
    py_modules = ['hakilo'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.5',
)
