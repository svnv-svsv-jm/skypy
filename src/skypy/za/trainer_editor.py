__all__ = ["FieldFrame", "ZATrainerEditor"]

import os
import sys
import typing as ty

import customtkinter as ctk
from loguru import logger

from skypy import settings
from skypy.schemas import ZAPokemonData, ZATrainerData, ZATrainerDataArray, ZAWazaData
from skypy.types.za import (
    Sex,
    ZABallID,
    ZADevID,
    ZAItemID,
    ZAWazaID,
)

from .fields import CheckboxFrame, DropdownFrame, FieldFrame, PkmnFrame, WazaFrame
from .load import load_trainer_data

wazas = [ZAWazaData(waza_id=waza).waza_id_english for waza in ty.get_args(ZAWazaID)]
wazas.sort()


def _get_app_directory() -> str:
    """Get the directory where the app is running from.

    For bundled `.app`, returns the directory containing the `.app` bundle.
    For running from code, returns the current working directory.
    """
    if getattr(sys, "frozen", False):  # pragma: no cover
        # Running as bundled app - sys.executable is like:
        # /path/to/ZA-Trainer-Editor.app/Contents/MacOS/ZA-Trainer-Editor
        # Go up 3 levels to get the directory containing the .app
        return os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(sys.executable)))
        )
    # Running from source
    return os.getcwd()


@logger.catch((ValueError, TypeError), reraise=False)
def _set_attr(obj: ty.Any, attr: str, value: str, dtype: type = str) -> None:
    """Helper to safely set attributes with type conversion."""
    if dtype is bool:
        val = value.lower() == "true"
    else:
        val = dtype(value)
    setattr(obj, attr, val)


class ZATrainerEditor(ctk.CTk):
    """ZA Trainer Editor."""

    def __init__(
        self,
        width: int = 950,
        height: int = 600,
        input_dir: str = settings.files.za_assets,
        output_dir: str | None = None,
        bfbs_file: str | None = None,
        file_name: str = "trdata_array.json",
        title: str = "ZA Trainer Editor",
        ignore_output_dir: bool = False,
        visible: bool = True,
        **kwargs: ty.Any,
    ) -> None:
        """Init.

        Args:
            width (int):
                Width of the window.

            height (int):
                Height of the window.

            input_dir (str):
                Directory to load trainer data from.

            output_dir (str):
                Directory to save trainer data to.

            bfbs_file (str):
                BFBS file to load trainer data from.
                Default is `"trdata_array.bfbs"`.

            file_name (str):
                File name to load trainer data from.
                Default is `"trdata_array.json"`.

            title (str):
                Title of the window.
                Default is `"ZA Trainer Editor"`.

            ignore_output_dir (bool):
                Whether to not use the output directory.
                Default is `False`.

            visible (bool):
                Whether to show the window.

            **kwargs (Any):
                Additional keyword arguments to pass to the parent class.
        """
        super().__init__(**kwargs)
        # Set up attributes
        self.app_title = title
        self.input_dir = input_dir
        self.output_dir = output_dir or os.path.join(_get_app_directory(), "Output")
        self.bfbs_file = bfbs_file or settings.files.za_trainers_bfbs_file
        self.file_name = file_name
        self.selected_trainer_index: int = 0
        self.ignore_output_dir = ignore_output_dir

        # Private
        self._output_dir_var = ctk.StringVar(value=self.output_dir)
        self._bfbs_file_var = ctk.StringVar(value=self.bfbs_file)

        # Load trainer data
        self.trdata = load_trainer_data(
            file_name=self.file_name,
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            ignore_output_dir=ignore_output_dir,
        )

        # Set up UI
        self.title(self.app_title)
        self.geometry(f"{width}x{height}")
        self.create_widgets()
        self.display_trainer_data()

        # Hide window if not visible
        if not visible:
            self.withdraw()
        logger.trace(f"Initialized ({type(self)}): {self}")

    def create_top_frame(self) -> None:
        """Create the top frame."""
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(fill="x", padx=10, pady=10)

    def create_trainer_combobox(self) -> None:
        """Create the trainer combobox."""
        # Create a label for the combobox
        self.trainer_combobox_label = ctk.CTkLabel(
            self.top_frame, text="Select Trainer:"
        )
        self.trainer_combobox_label.pack(side="left", padx=10)

        # Get list of trainer IDs for the combobox
        trainer_ids = [trainer.tr_id for trainer in self.trdata]

        # Create combobox
        self.trainer_combobox = ctk.CTkComboBox(
            self.top_frame,
            values=trainer_ids,
            command=self.on_trainer_selected,
        )
        self.trainer_combobox.pack(side="left", padx=10, fill="x", expand=True)

        # Set default selection
        self.trainer_combobox.set(trainer_ids[0])

    def create_data_frame(self) -> None:
        """Create the data frame."""
        self.data_frame = ctk.CTkScrollableFrame(self)
        self.data_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def create_bottom_frame(self) -> None:
        """Create the bottom frame."""
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(fill="x", padx=10, pady=10)

    def create_save_button(self) -> None:
        """Create the save button."""
        self.save_button = ctk.CTkButton(
            self.bottom_frame, text="Save Changes", command=self.save_trainer_data
        )
        self.save_button.pack(side="left", padx=10)

    def create_status_label(self) -> None:
        """Create the status label."""
        self.status_label = ctk.CTkLabel(
            self.bottom_frame,
            text="Have fun!",
            text_color="white",
        )
        self.status_label.pack(side="left", padx=10)

    def _on_output_directory_change(self, *_: object) -> None:
        """On output directory change."""
        self.output_dir = self._output_dir_var.get()
        logger.trace(f"Output directory changed to: {self.output_dir}")

    def create_output_directory_input(self) -> None:
        """Let the user change the output directory."""
        self._output_dir_var.trace_add("write", self._on_output_directory_change)

        self.output_directory_label = ctk.CTkLabel(
            self.top_frame,
            text="Output Directory:",
        )
        self.output_directory_label.pack(side="left", padx=(10, 5))

        self.output_directory_input = ctk.CTkEntry(
            self.top_frame,
            textvariable=self._output_dir_var,
            width=200,
        )
        self.output_directory_input.pack(side="left", padx=(0, 10))

    def _on_bfbs_file_change(self, *_: object) -> None:
        """On BFBS file change."""
        self.bfbs_file = self._bfbs_file_var.get()
        logger.trace(f"BFBS file changed to: {self.bfbs_file}")

    def create_bfbs_file_input(self) -> None:
        """Let the user change the output directory."""
        self._bfbs_file_var.trace_add("write", self._on_bfbs_file_change)

        self.bfbs_file_label = ctk.CTkLabel(
            self.top_frame,
            text="BFBS File:",
        )
        self.bfbs_file_label.pack(side="left", padx=(10, 5))

        self.bfbs_file_input = ctk.CTkEntry(
            self.top_frame,
            textvariable=self._bfbs_file_var,
            width=200,
        )
        self.bfbs_file_input.pack(side="left", padx=(0, 10))

    def create_widgets(self) -> None:
        """Create UI widgets."""
        logger.trace(f"Creating widgets ({type(self)}): {self}")

        # Top frame for combobox
        self.create_top_frame()

        # Create output directory input
        self.create_output_directory_input()

        # Create BFBS file input
        self.create_bfbs_file_input()

        # Create a label for the combobox
        self.create_trainer_combobox()

        # Create scrollable frame for trainer data
        self.create_data_frame()

        # Create bottom frame for save button and status
        self.create_bottom_frame()

        # Create save button
        self.create_save_button()

        # Create status label
        self.create_status_label()

        logger.trace(f"Created widgets ({type(self)}): {self}")

    def display_trainer_data(self) -> None:
        """Display the current trainer's data."""
        logger.trace(f"Displaying trainer data ({type(self)}): {self}")

        logger.trace(f"Selecting trainer index: {self.selected_trainer_index}")
        trainer: ZATrainerData = self.trdata[self.selected_trainer_index]

        # Basic Information Section
        self.basic_information_label = ctk.CTkLabel(
            self.data_frame, text="Basic Information", font=("Helvetica", 16, "bold")
        )
        self.basic_information_label.pack(pady=(10, 5), anchor="w")

        self.trainer_id_field = self._create_field(
            "Trainer ID",
            trainer.tr_id,
            readonly=True,
        )
        self.money_rate_field = self._create_field(
            "Money Rate",
            str(trainer.money_rate),
            lambda v: _set_attr(trainer, "money_rate", v, int),
        )

        # Boolean Flags Section
        self.flags_label = ctk.CTkLabel(
            self.data_frame, text="Flags", font=("Helvetica", 16, "bold")
        )
        self.flags_label.pack(pady=(20, 5), anchor="w")

        self.meg_evolution_checkbox = self._create_checkbox(
            "Mega Evolution",
            trainer.meg_evolution,
            lambda v: setattr(trainer, "meg_evolution", v),
        )
        self.last_hand_checkbox = self._create_checkbox(
            "Last Hand Mega",
            trainer.last_hand,
            lambda v: setattr(trainer, "last_hand", v),
        )

        # AI Flags Section
        self.ai_label = ctk.CTkLabel(
            self.data_frame, text="AI Settings", font=("Helvetica", 16, "bold")
        )
        self.ai_label.pack(pady=(20, 5), anchor="w")

        # AI Basic Checkbox
        self.ai_basic_checkbox = self._create_checkbox(
            "AI Basic",
            trainer.ai_basic,
            lambda v: setattr(trainer, "ai_basic", v),
        )
        self.ai_high_checkbox = self._create_checkbox(
            "AI High",
            trainer.ai_high,
            lambda v: setattr(trainer, "ai_high", v),
        )
        self.ai_expert_checkbox = self._create_checkbox(
            "AI Expert",
            trainer.ai_expert,
            lambda v: setattr(trainer, "ai_expert", v),
        )
        self.ai_double_checkbox = self._create_checkbox(
            "AI Double",
            trainer.ai_double,
            lambda v: setattr(trainer, "ai_double", v),
        )
        self.ai_raid_checkbox = self._create_checkbox(
            "AI Raid",
            trainer.ai_raid,
            lambda v: setattr(trainer, "ai_raid", v),
        )
        self.ai_weak_checkbox = self._create_checkbox(
            "AI Weak",
            trainer.ai_weak,
            lambda v: setattr(trainer, "ai_weak", v),
        )
        self.ai_item_checkbox = self._create_checkbox(
            "AI Item",
            trainer.ai_item,
            lambda v: setattr(trainer, "ai_item", v),
        )
        self.ai_change_checkbox = self._create_checkbox(
            "AI Change",
            trainer.ai_change,
            lambda v: setattr(trainer, "ai_change", v),
        )

        # View Settings Section
        self.view_settings_label = ctk.CTkLabel(
            self.data_frame, text="View Settings", font=("Helvetica", 16, "bold")
        )
        self.view_settings_label.pack(pady=(20, 5), anchor="w")

        self.view_horizontal_angle_field = self._create_field(
            "View Horizontal Angle",
            str(trainer.view_horizontal_angle),
            lambda v: _set_attr(trainer, "view_horizontal_angle", v, float),
        )
        self.view_vertical_angle_field = self._create_field(
            "View Vertical Angle",
            str(trainer.view_vertical_angle),
            lambda v: _set_attr(trainer, "view_vertical_angle", v, float),
        )
        self.view_range_field = self._create_field(
            "View Range",
            str(trainer.view_range),
            lambda v: _set_attr(trainer, "view_range", v, float),
        )
        self.hearing_range_field = self._create_field(
            "Hearing Range",
            str(trainer.hearing_range),
            lambda v: _set_attr(trainer, "hearing_range", v, float),
        )

        # Pokemon Section
        self.pokemon_label = ctk.CTkLabel(
            self.data_frame,
            text="Pokemon",
            font=("Helvetica", 16, "bold"),
        )
        self.pokemon_label.pack(pady=(20, 5), anchor="w")

        self.pokemon_fields: list[PkmnFrame] = [
            self._create_pokemon_field(1, trainer.poke_1),
            self._create_pokemon_field(2, trainer.poke_2),
            self._create_pokemon_field(3, trainer.poke_3),
            self._create_pokemon_field(4, trainer.poke_4),
            self._create_pokemon_field(5, trainer.poke_5),
            self._create_pokemon_field(6, trainer.poke_6),
        ]

        logger.trace(f"Displayed trainer data ({type(self)}): {self}")

    def _create_pokemon_field(
        self,
        index: int,
        pkmn: ZAPokemonData,
    ) -> PkmnFrame:
        """Create a pokemon field."""
        # Show all pokemon slots, even if empty
        poke_frame = ctk.CTkFrame(self.data_frame)
        poke_title = ctk.CTkLabel(
            poke_frame, text=f"Pokemon {index}", font=("Helvetica", 14, "bold")
        )

        def on_dev_id_change(val: str) -> None:
            """On Dev ID Change."""
            logger.trace(f"On Dev ID Change: {val}")
            pkmn.dev_id = settings.za_species_table.index(val)  # pragma: no cover
            logger.trace(f"New Dev ID: {pkmn.dev_id} | {val}")

        dev_id_field = self._create_dropdown(
            "Dev ID",
            pkmn.dev_id_english,
            values=[
                ZAPokemonData(dev_id=dev).dev_id_english for dev in ty.get_args(ZADevID)
            ],
            setter=on_dev_id_change,
            parent=poke_frame,
        )

        def on_item_change(val: str) -> None:
            """On Item Change."""
            logger.trace(f"On Item Change: {val}")
            pkmn.item = settings.za_items_table.index(val)  # pragma: no cover
            logger.trace(f"New Item: {pkmn.item} | {val}")

        item_field = self._create_dropdown(
            "Item",
            pkmn.item_english,
            values=[
                ZAPokemonData(item=item).item_english for item in ty.get_args(ZAItemID)
            ],
            setter=on_item_change,
            parent=poke_frame,
        )

        def on_level_change(val: str) -> None:
            """On Level Change."""
            logger.trace(f"On Level Change: {val}")
            pkmn.level = int(val)  # pragma: no cover
            logger.trace(f"New Level: {pkmn.level} | {val}")

        level_field = self._create_field(
            "Level",
            str(pkmn.level),
            setter=on_level_change,
            parent=poke_frame,
        )

        def on_form_id_change(val: str) -> None:
            """On Form ID Change."""
            logger.trace(f"On Form ID Change: {val}")
            pkmn.form_id = int(val)  # type: ignore # pragma: no cover
            logger.trace(f"New Form ID: {pkmn.form_id} | {val}")

        form_id_field = self._create_field(
            "Form ID",
            str(pkmn.form_id),
            setter=on_form_id_change,
            parent=poke_frame,
        )

        def on_sex_change(val: str) -> None:  # pragma: no cover
            """On Sex Change."""
            logger.trace(f"On Sex Change: {val}")
            pkmn.sex = int(val)  # type: ignore
            logger.trace(f"New Sex: {pkmn.sex} | {val}")

        sex_field = self._create_dropdown(
            "Sex",
            str(pkmn.sex),
            list(str(ty.get_args(Sex))),
            setter=on_sex_change,
            parent=poke_frame,
        )

        def on_ball_id_change(val: str) -> None:  # pragma: no cover
            """On Ball ID Change."""
            logger.trace(f"On Ball ID Change: {val}")
            pkmn.ball_id = settings.za_items_table.index(val)  # type: ignore
            logger.trace(f"New Ball ID: {pkmn.ball_id} | {val}")

        ball_id_field = self._create_dropdown(
            "Ball ID",
            pkmn.ball_id_english,
            list(str(ty.get_args(ZABallID))),
            setter=on_ball_id_change,
            parent=poke_frame,
        )

        def on_scale_value_change(val: str) -> None:  # pragma: no cover
            """On Scale Value Change."""
            logger.trace(f"On Scale Value Change: {val}")
            pkmn.scale_value = int(val)
            logger.trace(f"New Scale Value: {pkmn.scale_value} | {val}")

        scale_value_field = self._create_field(
            "Scale Value",
            str(pkmn.scale_value),
            setter=on_scale_value_change,
            parent=poke_frame,
        )

        # WAZA (Moves) Section
        waza_label = ctk.CTkLabel(
            poke_frame,
            text="Moves",
            font=("Helvetica", 12, "bold"),
        )
        waza_label.pack(anchor="w", padx=20, pady=(10, 5))

        waza_frames: list[WazaFrame] = [
            self._create_waza_field(1, pkmn.waza_1, poke_frame),
            self._create_waza_field(2, pkmn.waza_2, poke_frame),
            self._create_waza_field(3, pkmn.waza_3, poke_frame),
            self._create_waza_field(4, pkmn.waza_4, poke_frame),
        ]

        return PkmnFrame(
            frame=poke_frame,
            title=poke_title,
            dev_id_field=dev_id_field,
            item_field=item_field,
            level_field=level_field,
            form_id_field=form_id_field,
            sex_field=sex_field,
            waza_frames=waza_frames,
            waza_label=waza_label,
            ball_id_field=ball_id_field,
            scale_value_field=scale_value_field,
        )

    def _create_waza_field(
        self,
        index: int,
        waza: ZAWazaData,
        parent: ctk.CTkFrame,
    ) -> WazaFrame:
        """Create a waza field."""
        # Create a frame for each move
        waza_frame = ctk.CTkFrame(parent)
        waza_frame.pack(fill="x", pady=2, padx=30)

        waza_name_label = ctk.CTkLabel(waza_frame, text=f"Move {index}:", width=100)
        waza_name_label.pack(side="left", padx=5)

        # Move ID Entry
        def on_waza_change(val: str) -> None:  # pragma: no cover
            """On Waza Change.

            Args:
                val (str):
                    The value to set the Waza ID to.
                    This is the English name of the Waza ID if we translated it already, otherwise it's the original ID.
            """
            logger.trace(f"On Waza Change: {val}")
            waza.waza_id = settings.za_waza_table.index(val)
            logger.trace(f"New Waza ID: {waza.waza_id} | {val}")

        waza_option_menu = ctk.CTkOptionMenu(
            waza_frame,
            values=wazas,
            command=on_waza_change,
        )
        waza_option_menu.set(str(waza.waza_id_english))
        waza_option_menu.pack(side="left", fill="x", expand=True, padx=5)

        # Plus Checkbox
        def on_plus_change() -> None:  # pragma: no cover
            """On Plus Change."""
            logger.trace(f"On Plus Change: {waza.is_plus_waza}")
            waza.is_plus_waza = not waza.is_plus_waza
            logger.trace(f"New Plus Waza: {waza.is_plus_waza}")

        plus_checkbox = ctk.CTkCheckBox(
            waza_frame,
            text="Plus Waza",
            variable=ctk.BooleanVar(value=waza.is_plus_waza),
            command=on_plus_change,
        )
        plus_checkbox.pack(side="left", padx=5)

        return WazaFrame(
            frame=waza_frame,
            name_label=waza_name_label,
            option_menu=waza_option_menu,
            plus_checkbox=plus_checkbox,
        )

    def _create_field(
        self,
        label_text: str,
        value: str,
        setter: ty.Callable[[str], None] | None = None,
        readonly: bool = False,
        parent: ctk.CTkFrame | None = None,
    ) -> FieldFrame:
        """Create a label and entry field pair.

        The field is created and retained, but through the widget hierarchy rather than explicit instance attributes.

        Here's how it works:

        Widget Parenting: When you create `ctk.CTkFrame(parent or self.data_frame)`, the new frame becomes a child of the parent. The parent frame internally maintains references to all its children.

        `.pack()` adds to hierarchy: Calling `field_frame.pack(...)` adds the widget to its parent's layout manager, which keeps it alive and visible.

        Reference chain: `self.data_frame` → holds → `field_frame` → holds → `label` and `entry`

        So the widgets persist because they're part of the GUI tree rooted at `self.data_frame`.
        """
        logger.trace(f"Creating field: {label_text} = {value} (readonly: {readonly})")

        parent_frame = parent or self.data_frame

        field_frame = ctk.CTkFrame(parent_frame)
        field_frame.pack(fill="x", pady=2, padx=10)

        label = ctk.CTkLabel(field_frame, text=f"{label_text}:", width=200)
        label.pack(side="left", padx=5)

        var = ctk.StringVar(value=value)
        if readonly:
            entry = ctk.CTkLabel(field_frame, text=value, anchor="w")
        else:
            if setter:
                var.trace_add("write", lambda *args: setter(var.get()))
            entry = ctk.CTkEntry(field_frame, textvariable=var)

        entry.pack(side="left", fill="x", expand=True, padx=5)

        return FieldFrame(
            field_frame=field_frame,
            label=label,
            entry=entry,
            var=var,
        )

    def _create_checkbox(
        self,
        label_text: str,
        value: bool,
        setter: ty.Callable[[bool], None],
    ) -> None:
        """Create a checkbox field."""
        logger.trace(f"Creating checkbox: {label_text} = {value}")
        # Use IntVar for checkbox variable
        var = ctk.IntVar(value=1 if value else 0)
        var.trace_add("write", lambda *args: setter(bool(var.get())))

        checkbox = ctk.CTkCheckBox(self.data_frame, text=label_text, variable=var)
        checkbox.pack(anchor="w", padx=20, pady=2)

        return CheckboxFrame(
            var=var,
            checkbox=checkbox,
        )

    def _create_dropdown(
        self,
        label_text: str,
        value: str,
        values: list[str],
        setter: ty.Callable[[str], None],
        parent: ctk.CTkFrame | None = None,
    ) -> DropdownFrame:
        """Create a dropdown field."""
        logger.trace(f"Creating dropdown: {label_text} = {value} (values: {values})")
        field_frame = ctk.CTkFrame(parent or self.data_frame)
        field_frame.pack(fill="x", pady=2, padx=10)

        label = ctk.CTkLabel(field_frame, text=f"{label_text}:", width=200)
        label.pack(side="left", padx=5)

        logger.trace("Sorting values...")
        values.sort()
        logger.trace("Sorted values.")

        option_menu = ctk.CTkOptionMenu(field_frame, values=values, command=setter)
        option_menu.set(value)
        option_menu.pack(side="left", fill="x", expand=True, padx=5)

        return DropdownFrame(
            field_frame=field_frame,
            label=label,
            option_menu=option_menu,
        )

    def on_trainer_selected(self, choice: str) -> None:
        """Handle trainer selection from combobox."""
        # Find the index of the selected trainer
        for idx, trainer in enumerate(self.trdata):
            if trainer.tr_id == choice:
                self.selected_trainer_index = idx
                break
        # Update displayed data
        self.display_trainer_data()

    def save_trainer_data(
        self,
        output_dir: str | None = None,
        file_name: str | None = None,
        bfbs_file: str | None = None,
    ) -> None:
        """Save all trainer data to the JSON file and create binaries."""
        with logger.catch(
            Exception,
            reraise=False,
            onerror=lambda e: self.status_label.configure(
                text=f"Error: {e}",
                text_color="red",
            ),
        ):
            logger.trace(f"Saving trainer data ({type(self)}): {self}")
            output_dir = output_dir or self.output_dir
            file_name = file_name or self.file_name
            bfbs_file = bfbs_file or self.bfbs_file
            os.makedirs(output_dir, exist_ok=True)

            # Convert pydantic models back to dict format
            zatrdata = ZATrainerDataArray(Table=self.trdata)
            file_out = os.path.join(output_dir, file_name)
            logger.trace(f"Dumping data to {file_out}...")
            zatrdata.dump(file_out, bfbs_file=bfbs_file, create_binaries=True)
            logger.trace(f"Data dumped to {file_out}.")

            # Show confirmation
            self.status_label.configure(
                text=f"Saved to {file_out}",
                text_color="green",
            )

            # Clear status after 3 seconds
            self.after(
                3000, lambda: self.status_label.configure(text="", text_color="gray")
            )
