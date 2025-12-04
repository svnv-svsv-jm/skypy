__all__ = ["FieldFrame", "CheckboxFrame", "PkmnFrame", "WazaFrame", "TrainerFrame"]


import typing as ty

import customtkinter as ctk
import pydantic

from skypy.schemas import ZAPokemonData, ZATrainerData, ZAWazaData

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
    plus_var: ctk.BooleanVar
    plus_checkbox: ctk.CTkCheckBox
    waza_ref: ZAWazaData

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
    pokemon_ref: ZAPokemonData

    @pydantic.model_validator(mode="after")
    def validate(self) -> ty.Self:
        """Post init."""
        assert len(self.waza_frames) == 4
        return self

    def update_pokemon_data(self, pokemon: ZAPokemonData) -> None:
        """Update the pokemon data."""
        # Update the mutable reference so closures see the new Pokemon
        self.pokemon_ref = pokemon

        self.dev_id_field.option_menu.set(pokemon.dev_id_english)
        self.item_field.option_menu.set(pokemon.item_english)
        self.level_field.var.set(str(pokemon.level))
        self.form_id_field.var.set(str(pokemon.form_id))
        self.sex_field.option_menu.set(str(pokemon.sex))
        self.ball_id_field.option_menu.set(pokemon.ball_id_english)
        self.scale_value_field.var.set(str(pokemon.scale_value))
        for waza_frame, waza in zip(
            self.waza_frames,
            (
                pokemon.waza_1,
                pokemon.waza_2,
                pokemon.waza_3,
                pokemon.waza_4,
            ),
        ):
            waza_frame.waza_ref = waza
            waza_frame.option_menu.set(waza.waza_id_english)
            waza_frame.plus_var.set(waza.is_plus_waza)


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
    trainer_ref: ZATrainerData

    @pydantic.model_validator(mode="after")
    def validate(self) -> ty.Self:
        """Post init."""
        # Validations
        assert len(self.pokemon_fields) == 6
        return self

    def update_trainer_data(self, trainer: ZATrainerData) -> None:
        """Update the trainer data."""
        # Update the trainer reference so setters use the new trainer
        self.trainer_ref = trainer

        self.trainer_id_field.var.set(trainer.tr_id)
        self.money_rate_field.var.set(str(trainer.money_rate))
        self.meg_evolution_checkbox.var.set(trainer.meg_evolution)
        self.last_hand_checkbox.var.set(trainer.last_hand)
        self.ai_basic_checkbox.var.set(trainer.ai_basic)
        self.ai_high_checkbox.var.set(trainer.ai_high)
        self.ai_expert_checkbox.var.set(trainer.ai_expert)
        self.ai_double_checkbox.var.set(trainer.ai_double)
        self.ai_raid_checkbox.var.set(trainer.ai_raid)
        self.ai_weak_checkbox.var.set(trainer.ai_weak)
        self.ai_item_checkbox.var.set(trainer.ai_item)
        self.ai_change_checkbox.var.set(trainer.ai_change)
        self.view_horizontal_angle_field.var.set(str(trainer.view_horizontal_angle))
        self.view_vertical_angle_field.var.set(str(trainer.view_vertical_angle))
        self.view_range_field.var.set(str(trainer.view_range))
        self.hearing_range_field.var.set(str(trainer.hearing_range))
        for pokemon_field, poke in zip(
            self.pokemon_fields,
            (
                trainer.poke_1,
                trainer.poke_2,
                trainer.poke_3,
                trainer.poke_4,
                trainer.poke_5,
                trainer.poke_6,
            ),
        ):
            pokemon_field.update_pokemon_data(poke)
