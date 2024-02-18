__all__ = ["BaseSchema"]

import typing as ty
from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Base class to have cool methods."""

    def to_dict(self) -> ty.Dict[str, ty.Any]:
        """Return a dict representation. We need to replace `"_"` with `"."`, and to flatten the dictionary, too."""
        out = {}
        for key, val in self.__dict__.items():
            if isinstance(val, BaseSchema):
                for key_, val_ in val.to_dict().items():
                    k = f"{key}.{key_}"
                    out[k] = val_
            else:
                k = key.replace("___", ".")
                out[k] = val
        return out
