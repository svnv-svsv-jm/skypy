help:
	@cat Makefile

.EXPORT_ALL_VARIABLES:

# create an .env file to override the default settings
-include .env
export $(shell sed 's/=.*//' .env)


.PHONY: build docs bin json

# VARIABLES
OUTPUT=output
BINDIR=bin
BASENAME=personal_array


bin:
	flatc -b $(OUTPUT)/$(BASENAME).fbs $(OUTPUT)/$(BASENAME).json
	mv $(BASENAME).bin bin/.

json:
	rm $(BASENAME).json || echo ""
	flatc --json --strict-json --raw-binary $(OUTPUT)/$(BASENAME).fbs $(OUTPUT)/$(BASENAME).json -- $(BINDIR)/$(BASENAME).bin
	mv $(BASENAME).json $(BINDIR)/.

decode-bin:
	FILE=bin/data.trpfd
	flatc --json --strict-json --raw-binary -- bin/data.trpfd