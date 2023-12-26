# SkyPy

## Datamining Scarlet and Violet

Inspired by [Project Sky](https://gamebanana.com/tools/11558). This is a (still ugly) Python implementation of that, so that it can run on any platform/OS.

## Installation

You need Python.

```bash
python -m pip install --upgrade pip poetry
python -m poetry install
```

Now you're good to go.

## Usage

There is no UI, just [notebooks](./notebooks/Demo.ipynb). The idea is to be able to edit stuff programmatically. Edit the notebook as you prefer.

The output `.json` will be created in the [output](./output) folder. The next time you use the notebook, that `.json` file will be loaded, instead of the clean default one. So your edits won't be lost.

I recommend to create a notebook/script with all the planned changes, and then run it, so it does not matter if you load a clean `.json` or not.

You can read and edit mon's abilities, stats, types, etc. Also moves.

### Create .bin files

> You may want to skip this section

Once you're done, run:

```bash
make bin
```

to create your `bin/personal_array.bin` and `bin/waza_array.bin` file.

In your dumped ROM's folder, copy `personal_array.bin` to `romfs/avalon/data/personal_array.bin` and copy `waza_array.bin` to `romfs/avalon/data/waza_array.bin`.

### Create mod

Run:

```bash
make mod
```

This will create your mod here `bin/__mod__`. Copy this folder to your emulator. You will probably also need the `__mod__/romfs/arc/data.trpfd` file. Please get one by dumping a real copy of the game or by using [Trinity](https://github.com/Inidar1/Switch-Pokemon-Modding-Tutorials/wiki).

#### Acquire data.trpfd File

To get this file, download any up-to-date mod that includes it. See [here](https://github.com/pkZukan/gftool).

Download the mod, extract the zip, then copy the `data.trpfd` file from the `arc/` folder to any location you choose.

Alternatively, dump the full game with an emulator (right click --> extract data) and move the resulting `arc/`, `audio/`, `demo/`, and `event/` folders into the folder called `romfs`.

---

## To-do

- need to create better demo
- need UI: [example](https://www.youtube.com/watch?v=ELkaEpN29PU)
