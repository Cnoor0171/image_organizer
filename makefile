VENV ?= .venv
PYTHON_VERSION=3.8
PYTHON = $(if $(shell [ ! -d $(VENV) ] && echo found),python$(PYTHON_VERSION),. ${VENV}/bin/activate && python$(PYTHON_VERSION))
PYRIGHT = $(if $(shell [ ! -d $(VENV) ] && echo found),pyright,. ${VENV}/bin/activate && pyright)
PIP = $(PYTHON) -m pip
PYLINT = $(PYTHON) -m pylint
BLACK = $(PYTHON) -m black
MYPY = $(PYTHON) -m mypy
COVERAGE = $(PYTHON) -m coverage

UNIT_TEST_COV_THRESH = 50
SYS_TEST_COV_THRESH = 50

.PHONY: default
default: coverage

###################################
### Setup
###################################
.PHONY: venv install install-dev
venv:
	$(PYTHON) -m venv .venv
install:
	$(PIP) install -U setuptools wheel
	$(PIP) install .
install-dev:
	$(PIP) install -U setuptools wheel
	$(PIP) install -e .[dev,rest_api]

###################################
### Run
###################################
.PHONE: run
run:
	$(PYTHON) main.py

###################################
### Tests
###################################
.PHONY: tests tests-unit tests-system clean-coverage
tests: coverage
clean-coverage:
	$(COVERAGE) erase
tests-unit:
	$(COVERAGE) run --append --source=src --context=unit -m pytest tests/unit
tests-system:
	$(COVERAGE) run --append --source=src --context=system -m pytest tests/system
coverage: tests-unit tests-system
	$(COVERAGE) html --fail-under=$(UNIT_TEST_COV_THRESH) --context=unit -d htmlcov-unit
	$(COVERAGE) html --fail-under=$(SYS_TEST_COV_THRESH) --context=system -d htmlcov-system

###################################
### Linting
###################################
.PHONY: lint typecheck format format-check format-write format-diff
lint: format-check typecheck
	$(PYLINT) --rcfile=pylintrc src
	$(PYLINT) --rcfile=pylintrc.tests tests
typecheck:
	$(MYPY)
	$(PYRIGHT) src tests
format: format-check
format-check:
	$(BLACK) --check src tests
format-write:
	$(BLACK) src tests
format-diff:
	$(BLACK) --diff src tests

###################################
### Checks
###################################
.PHONY: pre-commit
pre-commit: lint tests
