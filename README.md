# SkyPy

## Datamining Scarlet and Violet

Inspired by [Project Sky](https://gamebanana.com/tools/11558). This is a (still ugly) Python implementation of that, so that it can run on any platform/OS.

There is no UI, just [notebooks](./notebooks/Demo.ipynb). The idea is to be able to edit stuff programmatically. Edit the notebook as you prefer.

## Installation

You need Python.

```bash
python -m pip install --upgrade pip poetry
python -m poetry install
```

Now you're good to go.

## Usage

The output `.json` will be created in the [output](./output) folder. The next time you use the notebook, that `.json` file will be loaded, instead of the clean default one. So your edits won't be lost.

I recommend to create a notebook/script with all the planned changes, and then run it, so it does not matter if you load a clean `.json` or not.

You can read and edit mon's abilities, stats, types, etc. Also moves.

Once you're done, run:

```bash
make bin
```

to create your `bin/personal_array.bin` and `bin/waza_array.bin` file.

In your dumped ROM's folder, copy `personal_array.bin` to `romfs/avalon/data/personal_array.bin` and copy `waza_array.bin` to `romfs/avalon/data/waza_array.bin`.

---

## To-do

- need to edit waza's
- need to create script for preferred edits
- need to create better demo
- need UI
