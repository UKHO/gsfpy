.PHONY: clean clean-test clean-pyc clean-build docs help lint checktypes checkstyle sast checklicenses test test-all coverage release
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
	@poetry run python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

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

lint: checktypes checkstyle sast checklicenses ## run all checks

checktypes: .venv ## check types with mypy
	poetry run mypy --ignore-missing-imports gsfpy tests

checkstyle: .venv ## check style with flake8 and black
	poetry run flake8 gsfpy tests
	poetry run isort --check-only --profile black gsfpy tests
	poetry run black --check --diff gsfpy tests

fixstyle: .venv ## fix black and isort style violations
	poetry run isort --profile black gsfpy tests
	poetry run black gsfpy tests

sast: .venv ## run static application security testing
	poetry run bandit -r gsfpy

checklicenses: .venv requirements.txt ## check dependencies meet licence rules
	poetry run liccheck -s liccheck.ini

test: .venv ## run tests quickly with the default Python
	poetry run pytest tests/test_libgsf_load_valid.py --verbose --capture=no
	poetry run pytest tests/test_libgsf_load_invalid.py --verbose --capture=no
	poetry run pytest tests/test_libgsf_load_default.py --verbose --capture=no
	poetry run pytest --ignore-glob=tests/test_libgsf_load_*.py --verbose --capture=no

test-all: .venv ## run tests on every Python version with tox
	poetry run tox

coverage: ## check code coverage quickly with the default Python
	poetry run coverage run --source gsfpy -m pytest
	poetry run coverage report -m
	poetry run coverage html
	poetry run $(BROWSER) htmlcov/index.html

release: dist ## package and upload a release
	poetry publish

dist: clean ## builds source and wheel package
	poetry build

requirements.txt: poetry.lock
	poetry export --format requirements.txt --output requirements.txt
	@touch requirements.txt # when there are no dependencies

.venv: poetry.lock
	poetry config virtualenvs.in-project true
	poetry install
	@touch -c .venv

poetry.lock: pyproject.toml
	poetry update
	@touch -c poetry.lock
