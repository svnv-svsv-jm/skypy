__all__ = ["ZATrainerEditor"]

import json
import os
import typing as ty

import customtkinter as ctk
import pydantic

from skypy.schemas import ZAPokemonData, ZATrainerData


class ZATrainerEditor(ctk.CTk):
    """ZA Trainer Editor."""

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        input_dir: str = "assets/za/Input",
        output_dir: str = "assets/za/Output",
        visible: bool = True,
        **kwargs: ty.Any,
    ) -> None:
        """Init."""
        super().__init__(**kwargs)
        if not visible:
            self.withdraw()
        self.title("ZA Trainer Editor")
        self.geometry(f"{width}x{height}")
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.trdata = self.load_trainer_data()
        self.selected_trainer_index: int = 0
        self.create_widgets()
        # Display initial trainer data
        self.display_trainer_data()

    def load_trainer_data(self, input_dir: str | None = None) -> list[ZATrainerData]:
        """Load trainer data from a JSON file."""
        input_dir = input_dir or self.input_dir
        path = os.path.join(input_dir, "trdata_array.json")
        with open(path, encoding="utf-8") as f:
            trdata = json.load(f)
        trdata = pydantic.TypeAdapter(list[ZATrainerData]).validate_python(
            trdata["values"]
        )
        return trdata

    def create_widgets(self) -> None:
        """Create UI widgets."""
        # Top frame for combobox
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=10, pady=10)

        # Create a label for the combobox
        label = ctk.CTkLabel(top_frame, text="Select Trainer:")
        label.pack(side="left", padx=10)

        # Get list of trainer IDs for the combobox
        trainer_ids = [trainer.trid for trainer in self.trdata]

        # Create combobox
        self.trainer_combobox = ctk.CTkComboBox(
            top_frame,
            values=trainer_ids,
            command=self.on_trainer_selected,
        )
        self.trainer_combobox.pack(side="left", padx=10, fill="x", expand=True)
        # Set default selection
        if trainer_ids:
            self.trainer_combobox.set(trainer_ids[0])

        # Create scrollable frame for trainer data
        self.data_frame = ctk.CTkScrollableFrame(self)
        self.data_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create bottom frame for save button and status
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(fill="x", padx=10, pady=10)

        # Create save button
        save_button = ctk.CTkButton(
            bottom_frame, text="Save Changes", command=self.save_trainer_data
        )
        save_button.pack(side="left", padx=10)

        # Create status label
        self.status_label = ctk.CTkLabel(bottom_frame, text="", text_color="gray")
        self.status_label.pack(side="left", padx=10)

    def display_trainer_data(self) -> None:
        """Display the current trainer's data."""
        # Clear existing widgets
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        trainer = self.trdata[self.selected_trainer_index]

        # Basic Information Section
        basic_label = ctk.CTkLabel(
            self.data_frame, text="Basic Information", font=("Helvetica", 16, "bold")
        )
        basic_label.pack(pady=(10, 5), anchor="w")

        self._create_field("Trainer ID", trainer.trid, readonly=True)
        self._create_field(
            "Trainer Type",
            str(trainer.trtype),
            lambda v: self._set_attr(trainer, "trtype", v, int),
        )
        self._create_field(
            "Trainer Type 2",
            str(trainer.trtype2),
            lambda v: self._set_attr(trainer, "trtype2", v, int),
        )
        self._create_field(
            "ZA Rank", trainer.za_rank, lambda v: self._set_attr(trainer, "za_rank", v)
        )
        self._create_field(
            "Money Rate",
            str(trainer.money_rate),
            lambda v: self._set_attr(trainer, "money_rate", v, int),
        )

        # Boolean Flags Section
        flags_label = ctk.CTkLabel(
            self.data_frame, text="Flags", font=("Helvetica", 16, "bold")
        )
        flags_label.pack(pady=(20, 5), anchor="w")

        self._create_checkbox(
            "Mega Evolution",
            trainer.meg_evolution,
            lambda v: setattr(trainer, "meg_evolution", v),
        )
        self._create_checkbox(
            "Last Hand", trainer.last_hand, lambda v: setattr(trainer, "last_hand", v)
        )

        # AI Flags Section
        ai_label = ctk.CTkLabel(
            self.data_frame, text="AI Settings", font=("Helvetica", 16, "bold")
        )
        ai_label.pack(pady=(20, 5), anchor="w")

        ai_flags = [
            "ai_basic",
            "ai_high",
            "ai_expert",
            "ai_double",
            "ai_raid",
            "ai_weak",
            "ai_item",
            "ai_change",
        ]
        for flag in ai_flags:
            label = flag.replace("_", " ").title()
            # Capture flag in closure default arg
            self._create_checkbox(
                label, getattr(trainer, flag), lambda v, f=flag: setattr(trainer, f, v)
            )

        # View Settings Section
        view_label = ctk.CTkLabel(
            self.data_frame, text="View Settings", font=("Helvetica", 16, "bold")
        )
        view_label.pack(pady=(20, 5), anchor="w")

        self._create_field(
            "View Horizontal Angle",
            str(trainer.view_horizontal_angle),
            lambda v: self._set_attr(trainer, "view_horizontal_angle", v, float),
        )
        self._create_field(
            "View Vertical Angle",
            str(trainer.view_vertical_angle),
            lambda v: self._set_attr(trainer, "view_vertical_angle", v, float),
        )
        self._create_field(
            "View Range",
            str(trainer.view_range),
            lambda v: self._set_attr(trainer, "view_range", v, float),
        )
        self._create_field(
            "Hearing Range",
            str(trainer.hearing_range),
            lambda v: self._set_attr(trainer, "hearing_range", v, float),
        )

        # Pokemon Section
        pokemon_label = ctk.CTkLabel(
            self.data_frame, text="Pokemon", font=("Helvetica", 16, "bold")
        )
        pokemon_label.pack(pady=(20, 5), anchor="w")

        for i in range(1, 7):
            poke_attr: ZAPokemonData = getattr(trainer, f"poke{i}")
            # Show all pokemon slots, even if empty
            poke_frame = ctk.CTkFrame(self.data_frame)
            poke_frame.pack(fill="x", pady=5, padx=10)

            poke_title = ctk.CTkLabel(
                poke_frame, text=f"Pokemon {i}", font=("Helvetica", 14, "bold")
            )
            poke_title.pack(anchor="w", padx=10, pady=5)

            self._create_field_in_frame(
                poke_frame,
                "Dev ID",
                poke_attr.dev_id,
                lambda v, p=poke_attr: self._set_attr(p, "dev_id", v),
            )
            self._create_field_in_frame(
                poke_frame,
                "Level",
                str(poke_attr.level),
                lambda v, p=poke_attr: self._set_attr(p, "level", v, int),
            )
            self._create_field_in_frame(
                poke_frame,
                "Form ID",
                str(poke_attr.form_id),
                lambda v, p=poke_attr: self._set_attr(p, "form_id", v, int),
            )
            self._create_field_in_frame(
                poke_frame,
                "Sex",
                poke_attr.sex,
                lambda v, p=poke_attr: self._set_attr(p, "sex", v),
            )
            self._create_field_in_frame(
                poke_frame,
                "Item",
                poke_attr.item,
                lambda v, p=poke_attr: self._set_attr(p, "item", v),
            )
            self._create_field_in_frame(
                poke_frame,
                "Ball ID",
                poke_attr.ball_id,
                lambda v, p=poke_attr: self._set_attr(p, "ball_id", v),
            )
            self._create_field_in_frame(
                poke_frame,
                "Seikaku",
                poke_attr.seikaku,
                lambda v, p=poke_attr: self._set_attr(p, "seikaku", v),
            )
            self._create_field_in_frame(
                poke_frame,
                "Tokusei",
                poke_attr.tokusei,
                lambda v, p=poke_attr: self._set_attr(p, "tokusei", v),
            )
            self._create_field_in_frame(
                poke_frame,
                "Rare Type",
                poke_attr.rare_type,
                lambda v, p=poke_attr: self._set_attr(p, "rare_type", v),
            )
            self._create_field_in_frame(
                poke_frame,
                "Scale Value",
                str(poke_attr.scale_value),
                lambda v, p=poke_attr: self._set_attr(p, "scale_value", v, int),
            )

            # WAZA (Moves) Section
            waza_label = ctk.CTkLabel(
                poke_frame, text="Moves", font=("Helvetica", 12, "bold")
            )
            waza_label.pack(anchor="w", padx=20, pady=(10, 5))

            for waza_num in range(1, 5):
                waza_key = f"waza{waza_num}"
                waza_data = getattr(poke_attr, waza_key)
                # Handle both dict and object access
                if isinstance(waza_data, dict):
                    waza_id = waza_data.get("wazaId", "WAZA_NULL")
                    is_plus = waza_data.get("isPlusWaza", False)
                else:
                    # If it's an object, try attribute access
                    waza_id = getattr(
                        waza_data, "wazaId", getattr(waza_data, "waza_id", "WAZA_NULL")
                    )
                    is_plus = getattr(
                        waza_data,
                        "isPlusWaza",
                        getattr(waza_data, "is_plus_waza", False),
                    )

                # Create a frame for each move
                waza_frame = ctk.CTkFrame(poke_frame)
                waza_frame.pack(fill="x", pady=2, padx=30)

                waza_name_label = ctk.CTkLabel(
                    waza_frame, text=f"Move {waza_num}:", width=100
                )
                waza_name_label.pack(side="left", padx=5)

                # Move ID Entry
                waza_var = ctk.StringVar(value=str(waza_id))

                def on_waza_change(val: str, wd=waza_data) -> None:  # Capture waza_data
                    if isinstance(wd, dict):
                        wd["wazaId"] = val
                    else:
                        if hasattr(wd, "wazaId"):
                            wd.wazaId = val
                        elif hasattr(wd, "waza_id"):
                            wd.waza_id = val

                waza_var.trace_add(
                    "write", lambda *args, v=waza_var: on_waza_change(v.get())
                )
                waza_id_entry = ctk.CTkEntry(waza_frame, textvariable=waza_var)
                waza_id_entry.pack(side="left", fill="x", expand=True, padx=5)

                # Plus Checkbox
                def on_plus_change(val: bool, wd=waza_data) -> None:
                    if isinstance(wd, dict):
                        wd["isPlusWaza"] = val
                    else:
                        if hasattr(wd, "isPlusWaza"):
                            wd.isPlusWaza = val
                        elif hasattr(wd, "is_plus_waza"):
                            wd.is_plus_waza = val

                # Re-doing checkbox logic to capture widget
                # Define variable
                plus_var = ctk.IntVar(value=1 if is_plus else 0)
                plus_var.trace_add(
                    "write", lambda *args, v=plus_var: on_plus_change(bool(v.get()))
                )

                plus_checkbox = ctk.CTkCheckBox(
                    waza_frame,
                    text="Plus Waza",
                    variable=plus_var,
                )
                plus_checkbox.pack(side="left", padx=5)

    def _set_attr(self, obj: ty.Any, attr: str, value: str, dtype: type = str) -> None:
        """Helper to safely set attributes with type conversion."""
        try:
            if dtype is bool:
                # This shouldn't happen for entries usually, but for completeness
                val = value.lower() == "true"
            else:
                val = dtype(value)
            setattr(obj, attr, val)
        except (ValueError, TypeError):
            pass

    def _create_field(
        self,
        label_text: str,
        value: str,
        setter: ty.Callable[[str], None] | None = None,
        readonly: bool = False,
    ) -> None:
        """Create a label and entry field pair."""
        field_frame = ctk.CTkFrame(self.data_frame)
        field_frame.pack(fill="x", pady=2, padx=10)

        label = ctk.CTkLabel(field_frame, text=f"{label_text}:", width=200)
        label.pack(side="left", padx=5)

        if readonly:
            entry = ctk.CTkLabel(field_frame, text=value, anchor="w")
            entry.pack(side="left", fill="x", expand=True, padx=5)
        else:
            var = ctk.StringVar(value=value)
            if setter:
                var.trace_add("write", lambda *args: setter(var.get()))
            entry = ctk.CTkEntry(field_frame, textvariable=var)
            entry.pack(side="left", fill="x", expand=True, padx=5)

    def _create_field_in_frame(
        self,
        parent: ctk.CTkFrame,
        label_text: str,
        value: str,
        setter: ty.Callable[[str], None] | None = None,
    ) -> None:
        """Create a label and entry field pair within a parent frame."""
        field_frame = ctk.CTkFrame(parent)
        field_frame.pack(fill="x", pady=2, padx=10)

        label = ctk.CTkLabel(field_frame, text=f"{label_text}:", width=150)
        label.pack(side="left", padx=5)

        var = ctk.StringVar(value=value)
        if setter:
            var.trace_add("write", lambda *args: setter(var.get()))
        entry = ctk.CTkEntry(field_frame, textvariable=var)
        entry.pack(side="left", fill="x", expand=True, padx=5)

    def _create_checkbox(
        self, label_text: str, value: bool, setter: ty.Callable[[bool], None]
    ) -> None:
        """Create a checkbox field."""
        # Use IntVar for checkbox variable
        var = ctk.IntVar(value=1 if value else 0)
        var.trace_add("write", lambda *args: setter(bool(var.get())))

        checkbox = ctk.CTkCheckBox(self.data_frame, text=label_text, variable=var)
        checkbox.pack(anchor="w", padx=20, pady=2)

    def on_trainer_selected(self, choice: str) -> None:
        """Handle trainer selection from combobox."""
        # Find the index of the selected trainer
        for idx, trainer in enumerate(self.trdata):
            if trainer.trid == choice:
                self.selected_trainer_index = idx
                break
        # Update displayed data
        self.display_trainer_data()

    def save_trainer_data(self) -> None:
        """Save all trainer data to the JSON file."""
        # Convert pydantic models back to dict format
        trainer_dicts = [trainer.model_dump(by_alias=True) for trainer in self.trdata]

        # Create the JSON structure
        output_data = {"values": trainer_dicts}

        # Write to file
        path = os.path.join(self.output_dir, "trdata_array.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        # Show confirmation
        self.status_label.configure(text=f"Saved to {path}", text_color="green")

        # Clear status after 3 seconds
        self.after(
            3000, lambda: self.status_label.configure(text="", text_color="gray")
        )
