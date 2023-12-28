help:
	@cat Makefile

.EXPORT_ALL_VARIABLES:

# create an .env file to override the default settings
-include .env
export $(shell sed 's/=.*//' .env)


.PHONY: build docs bin json

# VARIABLES
OUTPUT=output
SCHEMADIR=src/skypy/assets/schema
BINDIR=bin
APPNAME=MoveEditor


install:
	pip install --upgrade pip
	pip install --upgrade poetry
	poetry install


# --------------------------------
# Run main script
# --------------------------------
run:
	python main.py


# --------------------------------
# Create binary files (the MODS)
# --------------------------------
bin:
	rm $(BINDIR)/*.bin || echo "no bins"
	flatc -b $(SCHEMADIR)/personal_array.fbs $(OUTPUT)/personal_array.json || echo "ERROR for personal_array"
	flatc -b $(SCHEMADIR)/waza_array.fbs $(OUTPUT)/waza_array.json || echo "ERROR for waza_array"
	flatc -b $(SCHEMADIR)/trdata_array.bfbs $(OUTPUT)/trdata_array.json || echo "ERROR for trdata_array"
	mv *.bin $(BINDIR)/.

mod: MODDIR=$(BINDIR)/__mod__
mod: bin
	mkdir -p $(MODDIR)/romfs/avalon/data
	mv $(BINDIR)/personal_array.bin $(MODDIR)/romfs/avalon/data/.
	mv $(BINDIR)/waza_array.bin $(MODDIR)/romfs/avalon/data/.
	mkdir -p $(MODDIR)/romfs/world/data/trainer/trdata
	mv $(BINDIR)/trdata_array.bin $(MODDIR)/romfs/world/data/trainer/trdata/.
	cp info.toml $(MODDIR)/.
	cp -r sandbox/arc $(MODDIR)/romfs/.


# --------------------------------
# Decode binary files to JSON
# --------------------------------
json-decode: EXT=bfbs
json-decode:
	rm $(FILENAME).json || echo ""
	flatc --json --strict-json --raw-binary $(SCHEMADIR)/$(FILENAME).$(EXT) -- $(BINDIR)/$(FILENAME).bin
	mv $(FILENAME).json $(OUTPUT)/. || echo ""

json-personal: FILENAME=personal_array
json-personal: EXT=fbs
json-personal: json-decode

json-trainer: FILENAME=trdata_array
json-trainer: json-decode

json-waza: FILENAME=waza_array
json-waza: EXT=fbs
json-waza: json-decode

json: json-personal json-trainer json-waza


# --------------------------------
# Deserialize data.trpfd
# --------------------------------
trpfd:
	flatc --json --strict-json --raw-binary -- $(BINDIR)/data.trpfd


# --------------------------------
# App
# --------------------------------
# Use --add-data="$(LOC):customtkinter/" or not
app: LOC=$(shell pip show customtkinter | grep Location | awk '{print $$NF}')
app:
	pyinstaller --noconfirm --onedir --windowed \
	--icon "icon.ico" \
	--name $(APPNAME) \
	--add-data="$(LOC):customtkinter/" \
	--add-data "pyproject.toml:." \
	--add-data "src/skypy/assets:skypy/assets" \
	app.py

test-app:
	./dist/$(APPNAME)/$(APPNAME)