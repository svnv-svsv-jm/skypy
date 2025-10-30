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

# Testing

DIRS2CHECK := "src tests"

# VARIABLES

APP_LOC := `shell pip show customtkinter | grep Location | awk '{print $$NF}'`
OUTPUT := "output"
SCHEMADIR := "src/skypy/assets/schema"
BINDIR := "bin"
APPNAME := "MoveEditor"
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
    uv python install {{ python }}
    uv venv {{ venv }} --python={{ python }}
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
    {{ PYTHON_EXEC }} pytest -m "not integtest" -x --testmon --cov=src/ --cov-fail-under {{ COV_FAIL_UNDER }}

integ-test:
    {{ PYTHON_EXEC }} pytest -m "integtest" --testmon --cov=src/

nbmake:
    {{ PYTHON_EXEC }} pytest -x --testmon --nbmake --overwrite {{ EXAMPLE_DIR }}

test: ruff mypy unit-test nbmake

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
run cmd="apply":
    {{ PYTHON_EXEC }} {{ PROJECT_NAME }} {{ cmd }}

ui:
    {{ PYTHON_EXEC }} {{ PROJECT_NAME }}

# --------------------------------
# Create binary files (the MODS)

# --------------------------------
bin:
    rm {{ BINDIR }}/*.bin || echo "no bins"
    flatc -b {{ SCHEMADIR }}/personal_array.fbs {{ OUTPUT }}/personal_array.json || echo "ERROR for personal_array"
    flatc -b {{ SCHEMADIR }}/waza_array.fbs {{ OUTPUT }}/waza_array.json || echo "ERROR for waza_array"
    flatc -b {{ SCHEMADIR }}/trdata_array.bfbs {{ OUTPUT }}/trdata_array.json || echo "ERROR for trdata_array"
    mv *.bin {{ BINDIR }}/.

mod:
    just bin
    mkdir -p {{ MODDIR }}/romfs/avalon/data
    mv {{ BINDIR }}/personal_array.bin {{ MODDIR }}/romfs/avalon/data/.
    mv {{ BINDIR }}/waza_array.bin {{ MODDIR }}/romfs/avalon/data/.
    mkdir -p {{ MODDIR }}/romfs/world/data/trainer/trdata
    mv {{ BINDIR }}/trdata_array.bin {{ MODDIR }}/romfs/world/data/trainer/trdata/.
    cp info.toml {{ MODDIR }}/.
    cp -r sandbox/arc {{ MODDIR }}/romfs/.

# --------------------------------
# Decode binary files to JSON

# --------------------------------
json-decode filename ext:
    rm {{ filename }}.json || echo ""
    flatc --json --strict-json --raw-binary {{ SCHEMADIR }}/{{ filename }}.{{ ext }} -- {{ BINDIR }}/{{ filename }}.bin
    mv {{ filename }}.json {{ OUTPUT }}/. || echo ""

json-personal:
    just json-decode personal_array fbs

json-trainer:
    json-decode trdata_array bfbs

json-waza:
    json-decode waza_array fbs

json: json-personal json-trainer json-waza

# --------------------------------
# Deserialize data.trpfd

# --------------------------------
trpfd:
    flatc --json --strict-json --raw-binary -- {{ BINDIR }}/data.trpfd

# --------------------------------
# App
# --------------------------------

# Use --add-data="$(LOC):customtkinter/" or not
app LOC=APP_LOC:
    pyinstaller --noconfirm --onedir --windowed \
    --icon "icon.ico" \
    --name {{ APPNAME }} \
    --add-data="$(LOC):customtkinter/" \
    --add-data "pyproject.toml:." \
    --add-data "src/skypy/assets:skypy/assets" \
    src/skypy/__main__.py

test-app:
    ./dist/{{ APPNAME }}/{{ APPNAME }}
