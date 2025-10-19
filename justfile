# For docs, see: https://github.com/casey/just?tab=readme-ov-file

set shell := ["bash", "-c"]
set dotenv-load

default:
	@just --list

# ----------------
# default settings
# ----------------
# python
PROJECT_NAME := "skypy"
PYTHON_EXEC := "uv run"
PYTHONVERSION := "3.12"
ENVNAME := "venv"
COV_FAIL_UNDER := "100"
EXAMPLE_DIR := "./examples"
# VARIABLES
APP_LOC := `shell pip show customtkinter | grep Location | awk '{print $$NF}'`
OUTPUT := "output"
SCHEMADIR := "src/skypy/assets/schema"
BINDIR := "bin"
APPNAME := "MoveEditor"
EXT := "bfbs"
MODDIR := BINDIR + "/__mod__"


# --------------------------------
# Installation
# --------------------------------
install:
	uv sync

lock:
	uv lock


# -----------
# Testing
# -----------
format:
	{{PYTHON_EXEC}} ruff check . # Lint only

mypy:
	{{PYTHON_EXEC}} mypy --cache-fine-grained src
	{{PYTHON_EXEC}} mypy --cache-fine-grained tests

pyright:
	{{PYTHON_EXEC}} pyright --project pyproject.toml src
	{{PYTHON_EXEC}} pyright --project pyproject.toml tests

pylint:
	{{PYTHON_EXEC}} pylint src

unit-test:
	{{PYTHON_EXEC}} pytest -m "not integtest" -x --pylint --testmon --junitxml=pytest-results.xml --cov=src/ --cov-fail-under {{COV_FAIL_UNDER}}

integ-test:
	{{PYTHON_EXEC}} pytest -m "integtest" --pylint --testmon --junitxml=pytest-results.xml --cov=src/

nbmake:
	{{PYTHON_EXEC}} pytest -x --testmon --nbmake --overwrite {{EXAMPLE_DIR}}

test: format pylint pyright unit-test nbmake

tests: test


# --------------------------------
# Run
# --------------------------------
run cmd="apply":
	{{PYTHON_EXEC}} {{PROJECT_NAME}} {{cmd}}

ui:
	{{PYTHON_EXEC}} {{PROJECT_NAME}}


# --------------------------------
# Create binary files (the MODS)
# --------------------------------
bin:
	rm {{BINDIR}}/*.bin || echo "no bins"
	flatc -b {{SCHEMADIR}}/personal_array.fbs {{OUTPUT}}/personal_array.json || echo "ERROR for personal_array"
	flatc -b {{SCHEMADIR}}/waza_array.fbs {{OUTPUT}}/waza_array.json || echo "ERROR for waza_array"
	flatc -b {{SCHEMADIR}}/trdata_array.bfbs {{OUTPUT}}/trdata_array.json || echo "ERROR for trdata_array"
	mv *.bin {{BINDIR}}/.

mod:
	just bin
	mkdir -p {{MODDIR}}/romfs/avalon/data
	mv {{BINDIR}}/personal_array.bin {{MODDIR}}/romfs/avalon/data/.
	mv {{BINDIR}}/waza_array.bin {{MODDIR}}/romfs/avalon/data/.
	mkdir -p {{MODDIR}}/romfs/world/data/trainer/trdata
	mv {{BINDIR}}/trdata_array.bin {{MODDIR}}/romfs/world/data/trainer/trdata/.
	cp info.toml {{MODDIR}}/.
	cp -r sandbox/arc {{MODDIR}}/romfs/.


# --------------------------------
# Decode binary files to JSON
# --------------------------------
json-decode filename ext:
	rm {{filename}}.json || echo ""
	flatc --json --strict-json --raw-binary {{SCHEMADIR}}/{{filename}}.{{ext}} -- {{BINDIR}}/{{filename}}.bin
	mv {{filename}}.json {{OUTPUT}}/. || echo ""

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
	flatc --json --strict-json --raw-binary -- {{BINDIR}}/data.trpfd


# --------------------------------
# App
# --------------------------------
# Use --add-data="$(LOC):customtkinter/" or not
app LOC = APP_LOC:
	pyinstaller --noconfirm --onedir --windowed \
	--icon "icon.ico" \
	--name {{APPNAME}} \
	--add-data="$(LOC):customtkinter/" \
	--add-data "pyproject.toml:." \
	--add-data "src/skypy/assets:skypy/assets" \
	src/skypy/__main__.py

test-app:
	./dist/{{APPNAME}}/{{APPNAME}}