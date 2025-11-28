__all__ = [
    "BaseSchema",
    "_ByAliasInitializer",
    "_ByAliasSerializer",
    "get_values_from_serialization_alias",
]

import typing as ty

import pydantic


def get_values_from_serialization_alias(
    base_model: type[pydantic.BaseModel],
    values: dict[str, ty.Any],
) -> dict[str, ty.Any]:
    """This function is used to let a user initialize a data model (`pydantic.BaseModel`) with values from the serialization alias, which are generally only used when dumping the data model to a `dict`, not when initializing the data model from a `dict`.

    Args:
        base_model (type[pydantic.BaseModel]):
            The data model.
            This is needed to get the name and serialization alias from the data model for each field.

        values (dict[str, Any]):
            The `dict` object that contains the values the user provided to create an object of the given `base_model` class.
            Any field in this `dict` object that is named after one of the serialization aliases will be renamed with the original name of the field.
            This function will update this `dict` object (in-place!).

    Returns:
        dict[str, Any]: The `dict` object with the renamed values (serialization aliases replaced with the original names).
    """
    for name, field_info in base_model.model_fields.items():
        serialization_alias = field_info.serialization_alias
        if serialization_alias is not None and serialization_alias in values:
            values[name] = values[serialization_alias]
            del values[serialization_alias]
    return values


class BaseSchema(pydantic.BaseModel):
    """Base class to have cool methods."""

    def model_dump(self, **kwargs: ty.Any) -> dict[str, ty.Any]:
        """Override original `model_dump()` to replace all `"__"` characters with `"."`."""
        original_dict = super().model_dump(**kwargs)  # Get the default serialization
        transformed_dict = {
            key.replace("__", "."): value for key, value in original_dict.items()
        }
        return transformed_dict

    def to_dict(self) -> dict[str, ty.Any]:
        """Alias for `model_dump()`."""
        return self.model_dump()


class _ByAliasInitializer(pydantic.BaseModel):
    """Allows initializing by alias for nested objects."""

    @pydantic.model_validator(mode="before")
    @classmethod
    def _model_validator(cls, values: dict[str, ty.Any]) -> dict[str, ty.Any]:
        """Validate."""
        values = get_values_from_serialization_alias(cls, values)
        return values


class _ByAliasSerializer(pydantic.BaseModel):
    """Allows serializing by alias for nested objects."""

    def model_dump(self, *, by_alias: bool = False, **kwargs: ty.Any) -> dict:  # type: ignore
        # Call the original model_dump from the superclass
        data = super().model_dump(by_alias=by_alias, **kwargs)
        if not by_alias:
            return data  # No need to recurse

        for field, value in data.items():
            if isinstance(value, pydantic.BaseModel):
                # This case should not be possible because the above `super().model_dump` is supposed to already cast this to `dict`
                data[field] = value.model_dump(
                    by_alias=True, **kwargs
                )  # pragma: no cover
            elif isinstance(value, list):
                data[field] = [
                    (
                        v.model_dump(by_alias=True, **kwargs)
                        if isinstance(v, pydantic.BaseModel)
                        else v
                    )
                    for v in value
                ]
            elif isinstance(value, dict):
                data[field] = {
                    k: (
                        v.model_dump(by_alias=True, **kwargs)
                        if isinstance(v, pydantic.BaseModel)
                        else v
                    )
                    for k, v in value.items()
                }
        return data
