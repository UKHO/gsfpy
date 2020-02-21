#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = []

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest>=3"]

setup(
    author="UK Hydrographic Office",
    author_email="datascienceandengineering@ukho.gov.uk",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",  # TODO - review BEFORE open sourcing
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="""
    Python wrapper for the C implementation of the Generic Sensor Format library.
    """,
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="gsfpy",
    name="gsfpy",
    packages=find_packages(include=["gsfpy", "gsfpy.*"]),
    package_data={"libgsf3_06.so": ["libgsf3_06/libgsf3_06.so"]},
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/UKHO/gsfpy",
    version="1.1.0",
    zip_safe=False,
)
