__all__ = ["BaseSchema"]

import typing as ty
from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Base class to have cool methods."""

    def model_dump(self, **kwargs: ty.Any) -> dict[str, ty.Any]:
        """Override original `model_dump()` to replace all `"__"` characters with `"."`."""
        original_dict = super().model_dump(**kwargs)  # Get the default serialization
        transformed_dict = {key.replace("__", "."): value for key, value in original_dict.items()}
        return transformed_dict

    def to_dict(self) -> dict[str, ty.Any]:
        """Alias for `model_dump()`."""
        return self.model_dump()
