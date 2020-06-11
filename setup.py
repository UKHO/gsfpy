#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md") as history_file:
    history = history_file.read()

setup(
    author="UK Hydrographic Office",
    author_email="datascienceandengineering@ukho.gov.uk",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="""
    Python wrapper for the C implementation of the Generic Sensor Format library.
    """,
    install_requires=[],
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="gsfpy",
    name="gsfpy",
    packages=find_packages(include=["gsfpy", "gsfpy.*"]),
    package_data={"libgsf03-08.so": ["libgsf/libgsf03-08.so"]},
    setup_requires=["pytest-runner"],
    test_suite="tests",
    tests_require=["pytest>=3"],
    url="https://github.com/UKHO/gsfpy",
    version="1.4.0",
    zip_safe=False,
)
