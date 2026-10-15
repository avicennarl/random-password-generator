.PHONY: help install test lint fmt check clean

PYTHON := python3
VENV := .venv
ACTIVATE := . $(VENV)/bin/activate

help:
	@echo "targets: install, test, lint, fmt, check, clean"

$(VENV):
	$(PYTHON) -m venv $(VENV)
	. $(ACTIVATE) && pip install -e ".[dev]"

install: $(VENV)

test: $(VENV)
	. $(ACTIVATE) && pytest

lint: $(VENV)
	. $(ACTIVATE) && ruff check .

fmt: $(VENV)
	. $(ACTIVATE) && ruff format .

check: lint test

clean:
	rm -rf build dist *.egg-info __pycache__ .pytest_cache .ruff_cache
	find . -name "*.pyc" -o -name "*.pyo" -type f -delete
