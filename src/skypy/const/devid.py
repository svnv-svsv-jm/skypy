__all__ = ["DEV_ID"]

import typing as ty
import os
import json

from .loc import INPUT_FOLDER, FILENAME_DEVID

json_file = os.path.join(INPUT_FOLDER, FILENAME_DEVID)
with open(json_file, "r", encoding="utf-8-sig") as f:
    DEV_ID: ty.Dict[str, ty.List[ty.Dict[str, ty.Any]]] = json.load(f)
