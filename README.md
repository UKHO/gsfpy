# gsfpy
Python wrapper for the C implementation of the Generic Sensor Format library.

## Install as pip package into external project
    SSH: pip install git+ssh://git@github.com/UKHO/gsfpy.git@master
    HTTPS: pip install git+https://github.com/UKHO/gsfpy.git@master

## Development environment
Set up the gsfpy project in a local development environment as follows:

    git clone git@github.com:UKHO/gsfpy.git
    virtualenv gsfpy/ (--always-copy)
    cd gsfpy/
    source bin/activate
    python3 -m pip install -e .

## Run tests
Set up the development environment as above, then:

    python3 -m pip install pytest
    python3 -m pytest -s --verbose ./tests/

## Generic Sensor Format Documentation
Generic Sensor Format specification: see https://github.com/schwehr/generic-sensor-format/blob/master/doc/GSF_lib_03-06.pdf

Generic Sensor Format C library v3.06 specification: see https://github.com/schwehr/generic-sensor-format/blob/master/doc/GSF_spec_03-06.pdf

## Acknowledgements
C implementation of the GSF library provided by [Leidos](https://www.leidos.com/products/ocean-marine) under the LGPL license v2.1.

libgsf3_06.so was built from the Leidos C code using Make scripts based on those from [schwehr/generic-sensor-format](https://github.com/schwehr/generic-sensor-format/)