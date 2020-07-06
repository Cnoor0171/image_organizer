PYTHON = python3.7
VENV = $(PYTHON) -m venv
PIP = $(PYTHON) -m pip
PYTEST = $(PYTHON) -m pytest
PYLINT = $(PYTHON) -m pylint
BLACK = $(PYTHON) -m black

# Setup
.PHONY: venv, install, install-dev, install-proj

venv:
	$(VENV) .venv
install: install-proj
	$(PIP) install -r pip-requirements.txt
install-dev: install-proj
	$(PIP) install -r pip-requirements-dev.txt
install-proj:
	$(PIP) install -e .

# Tests
.PHONY: tests tests-unit
tests: tests-unit
tests-unit:
	$(PYTEST) tests/unit

# Linting
.PHONY: lint, typecheck
lint: typecheck
	$(PYLINT) src tests
typecheck:
	pyright src tests

# Formatting
.PHONY: format, format-check, format-write, format-diff
format: format-check
format-check:
	$(BLACK) --check src tests
format-write:
	$(BLACK) src tests
format-diff:
	$(BLACK) --diff src tests
