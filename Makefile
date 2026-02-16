# Makefile for easy development workflows.
# See docs/development.md for docs.
# Note GitHub Actions call uv directly, not this Makefile.

.DEFAULT_GOAL := default

.PHONY: default install lint test upgrade build clean
.PHONY: download build-fonts validate-fonts fonts showcase specimen
.PHONY: regression-generate regression-verify

default: install lint test

install:
	uv sync --all-extras

lint:
	uv run python devtools/lint.py

test:
	uv run pytest

upgrade:
	uv sync --upgrade --all-extras --dev

build:
	uv build

clean:
	-rm -rf dist/
	-rm -rf *.egg-info/
	-rm -rf .pytest_cache/
	-rm -rf .mypy_cache/
	-rm -rf .venv/
	-find . -type d -name "__pycache__" -exec rm -rf {} +

# Font build targets

download:
	uv run planetaire build download

build-fonts: download
	uv run planetaire build planetaire-mono

validate-fonts:
	uv run planetaire validate fonts/output/*.ttf

fonts: download build-fonts validate-fonts

showcase: build-fonts
	python scripts/generate_showcase.py

specimen: build-fonts
	typst compile docs/specimen/planetaire-mono-specimen.typ docs/specimen/planetaire-mono-specimen.pdf

regression-generate: build-fonts
	uv run planetaire regression generate

regression-verify: build-fonts
	uv run planetaire regression verify
