# Makefile for easy development workflows.
# See docs/development.md for docs.
# Note GitHub Actions call uv directly, not this Makefile.

.DEFAULT_GOAL := default

.PHONY: default install lint test upgrade build clean
.PHONY: download build-fonts build-text validate-fonts fonts showcase specimen
.PHONY: hero demo html-specimen site regression-generate regression-verify

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

build-text: download
	uv run planetaire build text

validate-fonts:
	uv run planetaire validate fonts/output/*.ttf

fonts: download build-fonts build-text validate-fonts

showcase: build-fonts
	uv run python scripts/generate_showcase.py

specimen: build-fonts
	uv run planetaire build specimen

hero: build-fonts
	uv run planetaire build hero

# Requires the `vhs` binary and the Planetaire Mono font installed system-wide.
demo: build-fonts
	vhs docs/specimen/terminal-demo.tape

html-specimen: build-text
	uv run planetaire build html-specimen

site: build-text html-specimen
	uv run planetaire build site

regression-generate: build-fonts
	uv run planetaire regression generate

regression-verify: build-fonts
	uv run planetaire regression verify
