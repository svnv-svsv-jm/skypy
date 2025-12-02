__all__ = ["ZATrainerEditor"]

import json
import os
import sys
import typing as ty

import customtkinter as ctk
import pyinstrument
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

# inverted_waza_translation = {value: key for key, value in waza_translation.items()}
# inverted_dev_translation = {value: key for key, value in dev_translation.items()}
# inverted_item_translation = {value: key for key, value in item_translation.items()}
wazas = [ZAWazaData(waza_id=waza).waza_id_english for waza in ty.get_args(ZAWazaID)]
wazas.sort()


def _get_app_directory() -> str:
    """Get the directory where the app is running from.

    For bundled `.app`, returns the directory containing the `.app` bundle.
    For running from code, returns the current working directory.
    """
    if getattr(sys, "frozen", False):
        # Running as bundled app - sys.executable is like:
        # /path/to/ZA-Trainer-Editor.app/Contents/MacOS/ZA-Trainer-Editor
        # Go up 3 levels to get the directory containing the .app
        return os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(sys.executable)))
        )
    # Running from source
    return os.getcwd()


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

        # Load trainer data
        self.trdata = self.load_trainer_data(
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

    def load_trainer_data(
        self,
        file_name: str | None = None,
        input_dir: str | None = None,
        output_dir: str | None = None,
        ignore_output_dir: bool = False,
    ) -> list[ZATrainerData]:
        """Load trainer data from a JSON file."""
        logger.trace("Loading trainer data...")
        # Inputs
        file_name = os.path.basename(file_name or self.file_name)
        input_dir = input_dir or self.input_dir
        output_dir = output_dir or self.output_dir

        # If output folder exists, use it
        dir_path = input_dir
        logger.trace(f"Set target directory to {dir_path}")
        if (
            os.path.exists(os.path.join(output_dir, file_name))
            and not ignore_output_dir
        ):
            logger.trace(f"Output folder exists ({output_dir}), using it....")
            dir_path = output_dir
            logger.trace(f"Set new target directory to {dir_path}")

        # Load data
        logger.trace(f"Joining {dir_path} and {file_name}")
        path = os.path.join(dir_path, file_name)
        logger.trace(f"Loading data from {path}...")
        with open(path, encoding="utf-8") as f:
            trdata: dict = json.load(f)
        assert isinstance(trdata, dict), f"Expected dict, got {type(trdata)}"
        trainers: ZATrainerDataArray = ZATrainerDataArray(**trdata)
        logger.trace(f"Loaded trainer data from {path}.")
        return trainers.values

    def create_top_frame(self) -> None:
        """Create the top frame."""
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(fill="x", padx=10, pady=10)

    def create_trainer_combobox(self) -> None:
        """Create the trainer combobox."""
        # Create a label for the combobox
        label = ctk.CTkLabel(self.top_frame, text="Select Trainer:")
        label.pack(side="left", padx=10)

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

    def create_output_directory_input(self) -> None:
        """Let the user change the output directory."""

        def on_output_directory_change(*_: object) -> None:
            """On output directory change."""
            self.output_dir = self._output_dir_var.get()
            logger.trace(f"Output directory changed to: {self.output_dir}")

        self._output_dir_var = ctk.StringVar(value=self.output_dir)
        self._output_dir_var.trace_add("write", on_output_directory_change)

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

    def create_bfbs_file_input(self) -> None:
        """Let the user change the output directory."""

        def on_bfbs_file_change(*_: object) -> None:
            """On BFBS file change."""
            self.bfbs_file = self._bfbs_file_var.get()
            logger.trace(f"BFBS file changed to: {self.bfbs_file}")

        self._bfbs_file_var = ctk.StringVar(value=self.bfbs_file)
        self._bfbs_file_var.trace_add("write", on_bfbs_file_change)

        self.output_directory_label = ctk.CTkLabel(
            self.top_frame,
            text="BFBS File:",
        )
        self.output_directory_label.pack(side="left", padx=(10, 5))

        self.output_directory_input = ctk.CTkEntry(
            self.top_frame,
            textvariable=self._output_dir_var,
            width=200,
        )
        self.output_directory_input.pack(side="left", padx=(0, 10))

    @pyinstrument.profile()
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

    @pyinstrument.profile()
    def display_trainer_data(self) -> None:
        """Display the current trainer's data."""
        logger.trace(f"Displaying trainer data ({type(self)}): {self}")

        # Clear existing widgets
        for widget in self.data_frame.winfo_children():
            logger.trace(f"Destroying widget: {widget}")
            widget.destroy()

        logger.trace(f"Selecting trainer index: {self.selected_trainer_index}")
        trainer: ZATrainerData = self.trdata[self.selected_trainer_index]

        # Basic Information Section
        basic_label = ctk.CTkLabel(
            self.data_frame, text="Basic Information", font=("Helvetica", 16, "bold")
        )
        basic_label.pack(pady=(10, 5), anchor="w")

        self._create_field(
            "Trainer ID",
            trainer.tr_id,
            readonly=True,
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
            "Last Hand Mega",
            trainer.last_hand,
            lambda v: setattr(trainer, "last_hand", v),
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
                label,
                getattr(trainer, flag),
                lambda v, f=flag: setattr(trainer, f, v),  # type: ignore
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
            poke_attr: ZAPokemonData = getattr(trainer, f"poke_{i}")
            # Show all pokemon slots, even if empty
            poke_frame = ctk.CTkFrame(self.data_frame)
            poke_frame.pack(fill="x", pady=5, padx=10)

            poke_title = ctk.CTkLabel(
                poke_frame, text=f"Pokemon {i}", font=("Helvetica", 14, "bold")
            )
            poke_title.pack(anchor="w", padx=10, pady=5)

            def on_dev_id_change(val: str) -> None:
                """On Dev ID Change."""
                logger.trace(f"On Dev ID Change: {val}")
                poke_attr.dev_id = settings.za_species_table.index(val)
                logger.trace(f"New Dev ID: {poke_attr.dev_id} | {val}")

            self._create_dropdown(
                "Dev ID",
                poke_attr.dev_id_english,
                values=[
                    ZAPokemonData(dev_id=dev).dev_id_english
                    for dev in ty.get_args(ZADevID)
                ],
                setter=on_dev_id_change,
                parent=poke_frame,
            )

            def on_item_change(val: str) -> None:
                """On Item Change."""
                logger.trace(f"On Item Change: {val}")
                poke_attr.item = settings.za_items_table.index(val)
                logger.trace(f"New Item: {poke_attr.item} | {val}")

            self._create_dropdown(
                "Item",
                poke_attr.item_english,
                values=[
                    ZAPokemonData(item=item).item_english
                    for item in ty.get_args(ZAItemID)
                ],
                setter=on_item_change,
                parent=poke_frame,
            )

            def on_level_change(val: str) -> None:
                """On Level Change."""
                logger.trace(f"On Level Change: {val}")
                poke_attr.level = int(val)
                logger.trace(f"New Level: {poke_attr.level} | {val}")

            self._create_field(
                "Level",
                str(poke_attr.level),
                setter=on_level_change,
                parent=poke_frame,
            )

            def on_form_id_change(val: str) -> None:
                """On Form ID Change."""
                logger.trace(f"On Form ID Change: {val}")
                poke_attr.form_id = int(val)  # type: ignore
                logger.trace(f"New Form ID: {poke_attr.form_id} | {val}")

            self._create_field(
                "Form ID",
                str(poke_attr.form_id),
                setter=on_form_id_change,
                parent=poke_frame,
            )

            def on_sex_change(val: str) -> None:
                """On Sex Change."""
                logger.trace(f"On Sex Change: {val}")
                poke_attr.sex = int(val)  # type: ignore
                logger.trace(f"New Sex: {poke_attr.sex} | {val}")

            self._create_dropdown(
                "Sex",
                str(poke_attr.sex),
                list(str(ty.get_args(Sex))),
                setter=on_sex_change,
                parent=poke_frame,
            )

            def on_ball_id_change(val: str) -> None:
                """On Ball ID Change."""
                logger.trace(f"On Ball ID Change: {val}")
                poke_attr.ball_id = settings.za_items_table.index(val)  # type: ignore
                logger.trace(f"New Ball ID: {poke_attr.ball_id} | {val}")

            self._create_dropdown(
                "Ball ID",
                poke_attr.ball_id_english,
                list(str(ty.get_args(ZABallID))),
                setter=on_ball_id_change,
                parent=poke_frame,
            )

            def on_scale_value_change(val: str) -> None:
                """On Scale Value Change."""
                logger.trace(f"On Scale Value Change: {val}")
                poke_attr.scale_value = int(val)
                logger.trace(f"New Scale Value: {poke_attr.scale_value} | {val}")

            self._create_field(
                "Scale Value",
                str(poke_attr.scale_value),
                setter=on_scale_value_change,
                parent=poke_frame,
            )

            # WAZA (Moves) Section
            waza_label = ctk.CTkLabel(
                poke_frame, text="Moves", font=("Helvetica", 12, "bold")
            )
            waza_label.pack(anchor="w", padx=20, pady=(10, 5))

            for waza_num in range(1, 5):
                waza_key = f"waza_{waza_num}"
                waza_data: ZAWazaData = getattr(poke_attr, waza_key)

                # Create a frame for each move
                waza_frame = ctk.CTkFrame(poke_frame)
                waza_frame.pack(fill="x", pady=2, padx=30)

                waza_name_label = ctk.CTkLabel(
                    waza_frame, text=f"Move {waza_num}:", width=100
                )
                waza_name_label.pack(side="left", padx=5)

                # Move ID Entry
                def on_waza_change(val: str) -> None:
                    """On Waza Change.

                    Args:
                        val (str):
                            The value to set the Waza ID to.
                            This is the English name of the Waza ID if we translated it already, otherwise it's the original ID.
                    """
                    logger.trace(f"On Waza Change: {val}")
                    waza_data.waza_id = settings.za_waza_table.index(val)
                    logger.trace(f"New Waza ID: {waza_data.waza_id} | {val}")

                waza_option_menu = ctk.CTkOptionMenu(
                    waza_frame,
                    values=wazas,
                    command=on_waza_change,
                )
                waza_option_menu.set(str(waza_data.waza_id_english))
                waza_option_menu.pack(side="left", fill="x", expand=True, padx=5)

                # Plus Checkbox
                def on_plus_change() -> None:
                    """On Plus Change."""
                    logger.trace(f"On Plus Change: {waza_data.is_plus_waza}")
                    waza_data.is_plus_waza = not waza_data.is_plus_waza
                    logger.trace(f"New Plus Waza: {waza_data.is_plus_waza}")

                plus_checkbox = ctk.CTkCheckBox(
                    waza_frame,
                    text="Plus Waza",
                    variable=ctk.BooleanVar(value=waza_data.is_plus_waza),
                    command=on_plus_change,
                )
                plus_checkbox.pack(side="left", padx=5)

        logger.trace(f"Displayed trainer data ({type(self)}): {self}")

    @logger.catch((ValueError, TypeError), reraise=False)
    def _set_attr(self, obj: ty.Any, attr: str, value: str, dtype: type = str) -> None:
        """Helper to safely set attributes with type conversion."""
        if dtype is bool:
            # This shouldn't happen for entries usually, but for completeness
            val = value.lower() == "true"
        else:
            val = dtype(value)
        setattr(obj, attr, val)

    def _create_field(
        self,
        label_text: str,
        value: str,
        setter: ty.Callable[[str], None] | None = None,
        readonly: bool = False,
        parent: ctk.CTkFrame | None = None,
    ) -> None:
        """Create a label and entry field pair."""
        logger.trace(f"Creating field: {label_text} = {value} (readonly: {readonly})")

        field_frame = ctk.CTkFrame(parent or self.data_frame)
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

    def _create_checkbox(
        self, label_text: str, value: bool, setter: ty.Callable[[bool], None]
    ) -> None:
        """Create a checkbox field."""
        logger.trace(f"Creating checkbox: {label_text} = {value}")
        # Use IntVar for checkbox variable
        var = ctk.IntVar(value=1 if value else 0)
        var.trace_add("write", lambda *args: setter(bool(var.get())))

        checkbox = ctk.CTkCheckBox(self.data_frame, text=label_text, variable=var)
        checkbox.pack(anchor="w", padx=20, pady=2)

    def _create_dropdown(
        self,
        label_text: str,
        value: str,
        values: list[str],
        setter: ty.Callable[[str], None],
        parent: ctk.CTkFrame | None = None,
    ) -> None:
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
