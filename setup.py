#!/usr/bin/env python3

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='gsfpy',
      version='0.1',
      description='Python Generic Sensor Format package',
      long_description=long_description,
      author='United Kingdom Hydrographic Office - Data Engineering',
      author_email='datascienceandengineering@ukho.gov.uk',
      url='https://github.com/UKHO/gsfpy',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'License :: Other/Proprietary License',     # FIXME - update when open sourced
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering :: ',
            'Topic :: Scientific/Engineering :: GIS',
            'Topic :: Scientific/Engineering :: Information Analysis'
           ],
      packages=find_packages(),
      install_requires=[],
      package_data={
        'libgsf3_06.so': ['libgsf3_06/libgsf3_06.so'],
      },
      include_package_data=True
      )
