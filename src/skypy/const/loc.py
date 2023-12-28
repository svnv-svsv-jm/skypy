import os

ASSETS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets"))
FILENAME_TR = "trdata_array.json"
FILENAME_WAZA = "waza_array.json"
FILENAME = "personal_array.json"
FILENAME_TR_MAP = "trdev_id.json"
FILENAME_DEVID = "devid_list.json"
INPUT_FOLDER = os.path.join(ASSETS, "json")
INPUT_FOLDER_OVERRIDE = "input"
OUTPUT_FOLDER = "output"
BIN_FOLDER = "bin"
SCHEMA_FOLDER = os.path.normpath(os.path.join(ASSETS, "schema"))
WAZA_SCHEMA = os.path.join(SCHEMA_FOLDER, "waza_array.fbs")
