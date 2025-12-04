__all__ = ["FieldFrame", "CheckboxFrame", "PkmnFrame", "WazaFrame", "TrainerFrame"]


import typing as ty

import customtkinter as ctk
import pydantic

from skypy.schemas import ZATrainerData

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
    waza_variable: ctk.StringVar
    option_menu: ctk.CTkOptionMenu
    plus_checkbox: ctk.CTkCheckBox

    @pydantic.model_validator(mode="after")
    def pack(self) -> ty.Self:
        """Post init."""
        self.frame.pack(fill="x", pady=2, padx=30)
        self.name_label.pack(side="left", padx=5)
        self.option_menu.pack(side="left", fill="x", expand=True, padx=5)
        self.plus_checkbox.pack(side="left", padx=5)
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
        # Validations
        assert len(self.waza_frames) == 4

        # Final edits
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


class TrainerFrame(pydantic.BaseModel):
    """Trainer frame."""

    model_config = CFG

    basic_information_label: ctk.CTkLabel
    trainer_id_field: FieldFrame
    money_rate_field: FieldFrame
    flags_label: ctk.CTkLabel
    meg_evolution_checkbox: CheckboxFrame
    last_hand_checkbox: CheckboxFrame
    ai_label: ctk.CTkLabel
    ai_basic_checkbox: CheckboxFrame
    ai_high_checkbox: CheckboxFrame
    ai_expert_checkbox: CheckboxFrame
    ai_double_checkbox: CheckboxFrame
    ai_raid_checkbox: CheckboxFrame
    ai_weak_checkbox: CheckboxFrame
    ai_item_checkbox: CheckboxFrame
    ai_change_checkbox: CheckboxFrame
    view_settings_label: ctk.CTkLabel
    view_horizontal_angle_field: FieldFrame
    view_vertical_angle_field: FieldFrame
    view_range_field: FieldFrame
    hearing_range_field: FieldFrame
    pokemon_label: ctk.CTkLabel
    pokemon_fields: list[PkmnFrame]

    @pydantic.model_validator(mode="after")
    def pack(self) -> ty.Self:
        """Post init."""
        # Validations
        assert len(self.pokemon_fields) == 6

        # Final edits
        self.basic_information_label.pack(pady=(10, 5), anchor="w")
        self.flags_label.pack(pady=(20, 5), anchor="w")
        self.ai_label.pack(pady=(20, 5), anchor="w")
        self.view_settings_label.pack(pady=(20, 5), anchor="w")
        self.pokemon_label.pack(pady=(20, 5), anchor="w")
        return self

    def update_trainer_data(self, trainer: ZATrainerData) -> None:
        """Update the trainer data."""
        self.trainer_id_field.entry.set(trainer.tr_id)
        self.money_rate_field.entry.set(str(trainer.money_rate))
        self.meg_evolution_checkbox.checkbox.set(trainer.meg_evolution)
        self.last_hand_checkbox.checkbox.set(trainer.last_hand)
        self.ai_basic_checkbox.checkbox.set(trainer.ai_basic)
        self.ai_high_checkbox.checkbox.set(trainer.ai_high)
        self.ai_expert_checkbox.checkbox.set(trainer.ai_expert)
        self.ai_double_checkbox.checkbox.set(trainer.ai_double)
        self.ai_raid_checkbox.checkbox.set(trainer.ai_raid)
