__all__ = ["TRDEV_ID"]

import typing as ty
import os
import json

from .loc import INPUT_FOLDER, FILENAME_TRDEVID

json_file = os.path.join(INPUT_FOLDER, FILENAME_TRDEVID)
with open(json_file, "r", encoding="utf-8-sig") as f:
    TRDEV_ID: ty.Dict[str, ty.List[ty.Dict[str, ty.Any]]] = json.load(f)
