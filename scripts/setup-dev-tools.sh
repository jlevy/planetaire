#!/usr/bin/env bash
#
# Install the native (non-Python) tools the font pipeline needs:
#
#   typst      - renders the specimen PDF and the README images       (required)
#   fontforge  - emboldens the Medium / ExtraBold weight masters       (required)
#   vhs        - records the terminal-demo.gif                         (optional)
#
# Python deps (fontTools, etc.) are managed by uv via pyproject.toml and are
# NOT handled here -- run `uv sync --all-extras` for those.
#
# Versions are pinned and (where a stable checksum is available) verified.
# The script is idempotent: tools already present at the pinned version are
# skipped. Binaries are installed into BIN_DIR (default: ~/.local/bin).
#
# Usage:
#   scripts/setup-dev-tools.sh            # typst + fontforge
#   scripts/setup-dev-tools.sh --with-vhs # also install vhs (+ ffmpeg/ttyd)
#
set -euo pipefail

TYPST_VERSION="0.13.1"
TYPST_SHA256="7d214bfeffc2e585dc422d1a09d2b144969421281e8c7f5d784b65fc69b5673f"
VHS_VERSION="0.11.0"

BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"
mkdir -p "$BIN_DIR"

note() { printf '\033[1m==>\033[0m %s\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

os="$(uname -s)"
arch="$(uname -m)"

# --- typst -------------------------------------------------------------------
install_typst() {
  if have typst && typst --version | grep -q "$TYPST_VERSION"; then
    note "typst $TYPST_VERSION already installed ($(command -v typst))"
    return
  fi
  case "$os/$arch" in
    Linux/x86_64)  target="x86_64-unknown-linux-musl" ;;
    Linux/aarch64) target="aarch64-unknown-linux-musl" ;;
    Darwin/arm64)  target="aarch64-apple-darwin" ;;
    Darwin/x86_64) target="x86_64-apple-darwin" ;;
    *) echo "Unsupported platform for typst: $os/$arch" >&2; return 1 ;;
  esac
  local url="https://github.com/typst/typst/releases/download/v${TYPST_VERSION}/typst-${target}.tar.xz"
  note "Installing typst $TYPST_VERSION from $url"
  local tmp; tmp="$(mktemp -d)"
  curl -sfL "$url" -o "$tmp/typst.tar.xz"
  if [ "$target" = "x86_64-unknown-linux-musl" ]; then
    echo "$TYPST_SHA256  $tmp/typst.tar.xz" | sha256sum -c - \
      || { echo "typst checksum mismatch" >&2; return 1; }
  fi
  tar -xJf "$tmp/typst.tar.xz" -C "$tmp"
  install -m 0755 "$tmp/typst-${target}/typst" "$BIN_DIR/typst"
  rm -rf "$tmp"
  note "typst -> $("$BIN_DIR/typst" --version)"
}

# --- fontforge ---------------------------------------------------------------
install_fontforge() {
  if have fontforge; then
    note "fontforge already installed ($(command -v fontforge))"
    return
  fi
  case "$os" in
    Linux)
      if have apt-get; then
        note "Installing fontforge via apt"
        (sudo apt-get update -y && sudo apt-get install -y fontforge) 2>/dev/null \
          || (apt-get update -y && apt-get install -y fontforge)
      elif have dnf; then sudo dnf install -y fontforge
      elif have pacman; then sudo pacman -S --noconfirm fontforge
      else echo "Install fontforge manually (no apt/dnf/pacman found)" >&2; return 1; fi ;;
    Darwin)
      have brew && brew install fontforge || { echo "Install Homebrew, then: brew install fontforge" >&2; return 1; } ;;
    *) echo "Unsupported platform for fontforge: $os" >&2; return 1 ;;
  esac
  note "fontforge -> $(fontforge --version 2>&1 | head -1)"
}

# --- vhs (optional) ----------------------------------------------------------
install_vhs() {
  if have vhs && vhs --version | grep -q "$VHS_VERSION"; then
    note "vhs $VHS_VERSION already installed"; return
  fi
  [ "$os" = "Linux" ] && [ "$arch" = "x86_64" ] || { echo "vhs auto-install only wired for Linux/x86_64; see https://github.com/charmbracelet/vhs" >&2; return 1; }
  # vhs needs ffmpeg and ttyd at runtime.
  if have apt-get; then (sudo apt-get install -y ffmpeg ttyd 2>/dev/null || apt-get install -y ffmpeg ttyd) || true; fi
  local base="https://github.com/charmbracelet/vhs/releases/download/v${VHS_VERSION}"
  local tmp; tmp="$(mktemp -d)"
  note "Installing vhs $VHS_VERSION"
  curl -sfL "$base/vhs_${VHS_VERSION}_Linux_x86_64.tar.gz" -o "$tmp/vhs.tgz"
  curl -sfL "$base/checksums.txt" -o "$tmp/checksums.txt"
  (cd "$tmp" && grep "vhs_${VHS_VERSION}_Linux_x86_64.tar.gz" checksums.txt | sha256sum -c -) \
    || { echo "vhs checksum mismatch" >&2; return 1; }
  tar -xzf "$tmp/vhs.tgz" -C "$tmp"
  install -m 0755 "$(find "$tmp" -name vhs -type f | head -1)" "$BIN_DIR/vhs"
  rm -rf "$tmp"
  note "vhs -> $("$BIN_DIR/vhs" --version)"
}

install_typst
install_fontforge
if [ "${1:-}" = "--with-vhs" ]; then install_vhs; fi

note "Done. Ensure $BIN_DIR is on your PATH."
note "Python deps: run 'uv sync --all-extras'."
