# Makefile for easy development workflows.
# See docs/development.md for docs.
# Note GitHub Actions call uv directly, not this Makefile.

.DEFAULT_GOAL := default

.PHONY: default install lint test upgrade build clean
.PHONY: download build-fonts build-text validate-fonts fonts specimen
.PHONY: images demo html-specimen site regression-generate regression-verify
.PHONY: dev-tools qa release release-finalize

default: install lint test

install:
	uv sync --all-extras

# Install native build tools (typst, fontforge; vhs optional). Idempotent.
dev-tools:
	bash scripts/setup-dev-tools.sh

# Post-generation quality checks (monospace invariants, metrics, style linking).
qa: validate-fonts

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
	uv run planetaire build text --formats ttf
	uv run planetaire build text --split --italics

validate-fonts:
	uv run planetaire validate fonts/output/*.ttf

fonts: download build-fonts build-text validate-fonts

images: build-fonts
	uv run planetaire build images

specimen: build-fonts
	uv run planetaire build specimen


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

# Release, in two steps with a review gate (see docs/fonts-build-and-release.md):
#   make release VERSION=0.1.4            # build, stamp PDF, re-pin README -> review the diff
#   make release-finalize VERSION=0.1.4   # commit + tag the reviewed changes (does not push)
release:
	@test -n "$(VERSION)" || { echo "usage: make release VERSION=X.Y.Z"; exit 1; }
	uv run python scripts/release.py prepare $(VERSION)

release-finalize:
	@test -n "$(VERSION)" || { echo "usage: make release-finalize VERSION=X.Y.Z"; exit 1; }
	uv run python scripts/release.py finalize $(VERSION)
