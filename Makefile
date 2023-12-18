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


bin:
	flatc -b $(SCHEMADIR)/personal_array.fbs $(OUTPUT)/personal_array.json
	flatc -b $(SCHEMADIR)/waza_array.fbs $(OUTPUT)/waza_array.json
	mv *.bin bin/.

json:
	rm personal_array.json || echo ""
	rm waza_array.json || echo ""
	flatc --json --strict-json --raw-binary $(SCHEMADIR)/personal_array.fbs $(OUTPUT)/personal_array.json -- $(BINDIR)/personal_array.bin
	flatc --json --strict-json --raw-binary $(SCHEMADIR)/personal_array.fbs $(OUTPUT)/personal_array.json -- $(BINDIR)/personal_array.bin
	mv personal_array.json $(BINDIR)/.
	mv waza_array.json $(BINDIR)/.

decode-bin:
	flatc --json --strict-json --raw-binary -- bin/data.trpfd