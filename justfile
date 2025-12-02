# For docs, see: https://github.com/casey/just?tab=readme-ov-file

set shell := ["bash", "-c"]
set dotenv-load := true

default:
    @just --list

# ----------------
# default settings
# ----------------
# Python

PROJECT_NAME := "skypy"
PYTHON_EXEC := "uv run"
PYTHONVERSION := "3.13"
VENV := ".venv"
COV_FAIL_UNDER := "100"
EXAMPLE_DIR := "./examples"
PYTHON_PATH := "/opt/homebrew/bin"

# Testing

DIRS2CHECK := "src tests"

# VARIABLES

APP_LOC := `uv pip show customtkinter | grep Location | cut -d' ' -f2`
OUTPUT := "output"
SCHEMADIR := "src/skypy/assets/schema"
BINDIR := "bin"
EXT := "bfbs"
MODDIR := BINDIR + "/__mod__"

# ----------------------
# Initialization
# ----------------------

# Show this help message
help:
    @just --list

# Source .env variables
load-env:
    set -a; source ".env"; set +a;

# Show variables
env:
    @env

# Initialize project directories
init:
    mkdir -p logs

# Python install
venv venv=VENV python=PYTHONVERSION:
    rm -rf {{ venv }} || echo "ok"
    uv python install {{ python }}
    uv venv {{ venv }} --python={{ PYTHON_PATH }}/python{{ python }}
    source "{{ venv }}/bin/activate"

# Pre-commit
pre-commit-install:
    uv tool install pre-commit
    uv tool run pre-commit install

# Install project dependencies
install: pre-commit-install
    uv sync

# Lock project dependencies
lock:
    uv lock

# Prepare CI/CD
prepare venv=VENV python=PYTHONVERSION:
    just venv "{{ venv }}" "{{ python }}"
    just install

# Build distribution
build:
    @echo "--- Building with uv ---"
    rm -r dist || echo "ok"
    uv build --all -o dist
    @echo "--- Done ---"

# -----------
# Testing
# -----------

# Mypy
mypy dir=DIRS2CHECK:
    {{ PYTHON_EXEC }} mypy --cache-fine-grained {{ dir }}

# Ruff is a linter and formatter
ruff dir=DIRS2CHECK:
    {{ PYTHON_EXEC }} ruff check --fix {{ dir }}
    {{ PYTHON_EXEC }} ruff format {{ dir }}

unit-test:
    {{ PYTHON_EXEC }} pytest -x --cov=src/ --cov-fail-under {{ COV_FAIL_UNDER }}

nbmake:
    {{ PYTHON_EXEC }} pytest -x --nbmake --overwrite {{ EXAMPLE_DIR }}

test: ruff mypy unit-test

tests: test

# Test we can build the wheel and then install it in a new, isolated environment
test-build: build
    @echo "--- Testing build with uv using Python ---"
    ls dist
    uv run scripts/pre-commits.py test-build --libs-dir "libs" --dist-dir "dist"
    @echo "--- Done ---"

# -----------
# git
# -----------

# Locally delete branches that have been merged
git-clean:
    bash scripts/git-clean.sh

# git-squash n:
# 	git reset --soft HEAD~{{n}} && git commit -m \"$(git log -1 --pretty=%B)\"

# Run pre-commits manually
pre-commit: pre-commit-install
    uv tool run pre-commit run --all-files

# --------------------------------
# Run
# --------------------------------

# Run the app
trainer-editor:
    {{ PYTHON_EXEC }} python -m skypy

# --------------------------------
# Files
# --------------------------------

# Create binary from JSON
encode-binary-from-json:
    mkdir -p bin
    rm bin/*.bin || echo "no bins"
    flatc -b sandbox/trdata_array.bfbs sandbox/trdata_array.json
    mv *.bin bin/.

# Decode binary files to JSON
decode-binary-to-json:
    flatc --json --strict-json --raw-binary sandbox/trdata_array.bfbs -- sandbox/trdata_array.bin
    mv trdata_array.json assets/za/Raw/trdata_array.json

# --------------------------------
# App
# --------------------------------

# Use --add-data="$(LOC):customtkinter/" or not
build-app name="ZA-Trainer-Editor" loc=APP_LOC:
    uv run pyinstaller --noconfirm --onedir --windowed \
    --icon "icon.ico" \
    --name {{ name }} \
    --add-data="{{ loc }}:customtkinter/" \
    --add-data "pyproject.toml:." \
    --add-data "src/skypy/assets:skypy/assets" \
    src/skypy/__main__.py
