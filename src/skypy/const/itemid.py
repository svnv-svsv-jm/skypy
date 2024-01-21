__all__ = ["ITEMID"]

import typing as ty
import os
import json

from .loc import INPUT_FOLDER, FILENAEM_ITEMID

json_file = os.path.join(INPUT_FOLDER, FILENAEM_ITEMID)
with open(json_file, "r", encoding="utf-8-sig") as f:
    ITEMID: ty.Dict[str, ty.List[ty.Dict[str, ty.Any]]] = json.load(f)
