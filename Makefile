.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: checkstyle sast checklicenses ## run all checks

checkstyle: ## check style with flake8 and black
	flake8 gsfpy tests setup.py
	isort --check-only --recursive gsfpy tests setup.py
	black --check --diff gsfpy tests setup.py

fixstyle: ## fix black and isort style violations
	isort --recursive gsfpy tests setup.py
	black gsfpy tests setup.py

sast: ## run static application security testing
	bandit -r gsfpy

checklicenses: requirements.txt ## check dependencies meet licence rules
	liccheck -s liccheck.ini -r requirements.txt

test: requirements.txt ## run tests quickly with the default Python
	pytest --verbose --capture=no

test-all: requirements.txt ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source gsfpy -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean requirements.txt ## install the package to the active Python's site-packages
	python setup.py install

requirements.txt: setup.py ## create/update the requirements.txt file using pip-tools
	pip install -r requirements-dev.txt
	pip-compile
	pip install -r requirements.txt
