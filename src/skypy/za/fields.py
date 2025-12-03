__all__ = ["FieldFrame", "CheckboxFrame", "PkmnFrame", "WazaFrame"]


import typing as ty

import customtkinter as ctk
import pydantic

CFG = pydantic.ConfigDict(
    extra="forbid",
    arbitrary_types_allowed=True,
    populate_by_name=True,
    validate_assignment=True,
    validate_default=True,
)


class FieldFrame(pydantic.BaseModel):
    """Field frame."""

    model_config = CFG

    field_frame: ctk.CTkFrame
    label: ctk.CTkLabel
    entry: ctk.CTkEntry | ctk.CTkLabel
    var: ctk.StringVar


class CheckboxFrame(pydantic.BaseModel):
    """Checkbox frame."""

    model_config = CFG

    var: ctk.IntVar
    checkbox: ctk.CTkCheckBox


class DropdownFrame(pydantic.BaseModel):
    """Dropdown frame."""

    model_config = CFG

    field_frame: ctk.CTkFrame
    label: ctk.CTkLabel
    option_menu: ctk.CTkOptionMenu


class WazaFrame(pydantic.BaseModel):
    """Waza frame."""

    model_config = CFG

    frame: ctk.CTkFrame
    name_label: ctk.CTkLabel
    option_menu: ctk.CTkOptionMenu
    plus_checkbox: ctk.CTkCheckBox

    @pydantic.model_validator(mode="after")
    def pack(self) -> ty.Self:
        """Post init."""
        self.frame.pack(fill="x", pady=5, padx=10)
        self.name_label.pack(anchor="w", padx=10, pady=5)
        self.option_menu.pack(fill="x", pady=2, padx=10)
        self.plus_checkbox.pack(fill="x", pady=2, padx=10)
        return self


class PkmnFrame(pydantic.BaseModel):
    """Pokemon frame."""

    model_config = CFG

    frame: ctk.CTkFrame
    title: ctk.CTkLabel
    dev_id_field: DropdownFrame
    item_field: DropdownFrame
    level_field: FieldFrame
    form_id_field: FieldFrame
    sex_field: DropdownFrame
    ball_id_field: DropdownFrame
    scale_value_field: FieldFrame
    waza_label: ctk.CTkLabel
    waza_frames: list[WazaFrame]

    @pydantic.model_validator(mode="after")
    def pack(self) -> ty.Self:
        """Post init."""
        self.frame.pack(fill="x", pady=5, padx=10)
        self.title.pack(anchor="w", padx=10, pady=5)
        self.dev_id_field.field_frame.pack(fill="x", pady=2, padx=10)
        self.item_field.field_frame.pack(fill="x", pady=2, padx=10)
        self.level_field.field_frame.pack(fill="x", pady=2, padx=10)
        self.form_id_field.field_frame.pack(fill="x", pady=2, padx=10)
        self.sex_field.field_frame.pack(fill="x", pady=2, padx=10)
        self.ball_id_field.field_frame.pack(fill="x", pady=2, padx=10)
        self.scale_value_field.field_frame.pack(fill="x", pady=2, padx=10)
        self.waza_label.pack(anchor="w", padx=10, pady=5)
        for waza_frame in self.waza_frames:
            waza_frame.frame.pack(fill="x", pady=2, padx=10)
            waza_frame.name_label.pack(anchor="w", padx=10, pady=5)
            waza_frame.option_menu.pack(fill="x", pady=2, padx=10)
            waza_frame.plus_checkbox.pack(fill="x", pady=2, padx=10)
        return self
