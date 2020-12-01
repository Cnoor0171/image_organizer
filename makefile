VENV ?= .venv
PYTHON = $(if $(shell [ ! -d $(VENV) ] && echo found),python3.7,. ${VENV}/bin/activate && python3.7)
PIP = $(PYTHON) -m pip
PYTEST = $(PYTHON) -m pytest
PYLINT = $(PYTHON) -m pylint
BLACK = $(PYTHON) -m black
PYRIGHT = pyright

default:
	echo "${PYLINT}"

###################################
### Setup
###################################
.PHONY: venv install install-dev
venv:
	$(PYTHON) -m venv .venv
install:
	$(PIP) install .
install-dev:
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
.PHONY: tests tests-unit
tests: tests-unit
tests-unit:
	$(PYTEST) tests/unit

###################################
### Linting
###################################
.PHONY: lint typecheck format format-check format-write format-diff
lint: format-check typecheck
	$(PYLINT) --rcfile=pylintrc src
	$(PYLINT) --rcfile=pylintrc.tests tests
typecheck:
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
