__all__ = ["FieldFrame", "ZATrainerEditor"]

import functools
import os
import sys
import tkinter as tk
import typing as ty

import customtkinter as ctk
from loguru import logger

from skypy import settings
from skypy.schemas import ZAPokemonData, ZATrainerData, ZATrainerDataArray, ZAWazaData
from skypy.types.za import Sex, ZABallID

from .frames import (
    CheckboxFrame,
    DropdownFrame,
    FieldFrame,
    PkmnFrame,
    TrainerFrame,
    WazaFrame,
)
from .load import load_trainer_data

WAZAS = sorted(settings.za_waza_table)
ITEMS = sorted(settings.za_items_table)
SPECIES = sorted(settings.za_species_table)
RANKS = sorted(settings.za_rank_mappings.keys())


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
        self.ignore_output_dir = ignore_output_dir

        # Private
        self._output_dir_var = ctk.StringVar(value=self.output_dir)
        self._bfbs_file_var = ctk.StringVar(value=self.bfbs_file)

        # Scaling/zoom settings
        self._scale = 1.0
        self._scale_min = 0.5
        self._scale_max = 2.0
        self._scale_step = 0.1

        # Set up UI
        self.title(self.app_title)
        self.geometry(f"{width}x{height}")
        logger.info(f"Loading {type(self.trdata)} data...")
        self.create_widgets()
        self.trainer_frame = self.create_trainer_data()

        # Bind zoom keyboard shortcuts
        self._bind_zoom_shortcuts()

        # Hide window if not visible
        if not visible:
            self.withdraw()
        logger.trace(f"Initialized ({type(self)}): {self}")

    @functools.cached_property
    def trdata(self) -> ZATrainerDataArray:
        """Trainer data."""
        return load_trainer_data(
            file_name=self.file_name,
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            ignore_output_dir=self.ignore_output_dir,
        )

    @functools.cached_property
    def top_frame(self) -> ctk.CTkFrame:
        """Top frame."""
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=10, pady=10)
        return top_frame

    @functools.cached_property
    def data_frame(self) -> ctk.CTkScrollableFrame:
        """Data frame.

        Note: On macOS with Tk 9, trackpad scrolling doesn't work with Canvas-based
        widgets (a Tk limitation). Use the scrollbar or keyboard (arrow keys, Page Up/Down).
        """
        data_frame = ctk.CTkScrollableFrame(self)
        data_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Unbind the default CustomTkinter mouse wheel event
        data_frame.unbind_all("<MouseWheel>")

        def _on_mousewheel(event: tk.Event) -> None:
            """On macOS, event.delta is usually small; scale it to feel natural."""
            logger.trace(f"On Mouse Wheel: {event.delta}")
            data_frame._parent_canvas.yview("scroll", int(-event.delta / 60), "units")

        data_frame.bind_all("<MouseWheel>", _on_mousewheel, add="+")

        return data_frame

    @functools.cached_property
    def bottom_frame(self) -> ctk.CTkFrame:
        """Bottom frame."""
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        return bottom_frame

    @functools.cached_property
    def trainer_combobox_label(self) -> ctk.CTkLabel:
        """Trainer combobox label."""
        trainer_combobox_label = ctk.CTkLabel(
            self.top_frame,
            text="Select Trainer:",
        )
        trainer_combobox_label.pack(side="left", padx=10)
        return trainer_combobox_label

    @functools.cached_property
    def trainer_combobox(self) -> ctk.CTkComboBox:
        """Trainer combobox."""
        trainer_combobox = ctk.CTkComboBox(
            self.top_frame,
            values=[trainer.tr_id for trainer in self.trdata.values],
            command=self.on_trainer_selected,
        )
        trainer_combobox.pack(side="left", padx=10, fill="x", expand=True)
        # Bind Enter key to trigger selection when typing
        trainer_combobox.bind(
            "<Return>",
            lambda event: self.on_trainer_selected(trainer_combobox.get()),
        )
        return trainer_combobox

    @functools.cached_property
    def save_button(self) -> ctk.CTkButton:
        """Save button."""
        save_button = ctk.CTkButton(
            self.bottom_frame,
            text="Save Changes",
            command=self.save_trainer_data,
        )
        save_button.pack(side="left", padx=10)
        return save_button

    @functools.cached_property
    def status_label(self) -> ctk.CTkLabel:
        """Status label."""
        status_label = ctk.CTkLabel(
            self.bottom_frame,
            text="Have fun!",
            text_color="white",
        )
        status_label.pack(side="left", padx=10)
        return status_label

    @functools.cached_property
    def zoom_frame(self) -> ctk.CTkFrame:
        """Zoom control frame."""
        zoom_frame = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        zoom_frame.pack(side="right", padx=10)
        return zoom_frame

    @functools.cached_property
    def zoom_out_button(self) -> ctk.CTkButton:
        """Zoom out button."""
        zoom_out_button = ctk.CTkButton(
            self.zoom_frame,
            text="−",
            width=30,
            command=self.zoom_out,
        )
        zoom_out_button.pack(side="left", padx=2)
        return zoom_out_button

    @functools.cached_property
    def zoom_label(self) -> ctk.CTkLabel:
        """Zoom level label."""
        zoom_label = ctk.CTkLabel(
            self.zoom_frame,
            text="100%",
            width=50,
        )
        zoom_label.pack(side="left", padx=5)
        return zoom_label

    @functools.cached_property
    def zoom_in_button(self) -> ctk.CTkButton:
        """Zoom in button."""
        zoom_in_button = ctk.CTkButton(
            self.zoom_frame,
            text="+",
            width=30,
            command=self.zoom_in,
        )
        zoom_in_button.pack(side="left", padx=2)
        return zoom_in_button

    @functools.cached_property
    def zoom_reset_button(self) -> ctk.CTkButton:
        """Zoom reset button."""
        zoom_reset_button = ctk.CTkButton(
            self.zoom_frame,
            text="Reset",
            width=50,
            command=self.zoom_reset,
        )
        zoom_reset_button.pack(side="left", padx=5)
        return zoom_reset_button

    @functools.cached_property
    def output_directory_label(self) -> ctk.CTkLabel:
        """Output directory label."""
        output_directory_label = ctk.CTkLabel(
            self.top_frame,
            text="Output Directory:",
        )
        output_directory_label.pack(side="left", padx=(10, 5))
        return output_directory_label

    @functools.cached_property
    def output_directory_input(self) -> ctk.CTkEntry:
        """Output directory input."""
        self._output_dir_var.trace_add("write", self._on_output_directory_change)
        output_directory_input = ctk.CTkEntry(
            self.top_frame,
            textvariable=self._output_dir_var,
            width=200,
        )
        output_directory_input.pack(side="left", padx=(0, 10))
        return output_directory_input

    @functools.cached_property
    def bfbs_file_label(self) -> ctk.CTkLabel:
        """BFBS file label."""
        bfbs_file_label = ctk.CTkLabel(
            self.top_frame,
            text="BFBS File:",
        )
        bfbs_file_label.pack(side="left", padx=(10, 5))
        return bfbs_file_label

    @functools.cached_property
    def bfbs_file_input(self) -> ctk.CTkEntry:
        """BFBS file input."""
        self._bfbs_file_var.trace_add("write", self._on_bfbs_file_change)
        bfbs_file_input = ctk.CTkEntry(
            self.top_frame,
            textvariable=self._bfbs_file_var,
            width=200,
        )
        bfbs_file_input.pack(side="left", padx=(0, 10))
        return bfbs_file_input

    def create_top_frame(self) -> ctk.CTkFrame:
        """Create the top frame."""
        return self.top_frame

    def create_data_frame(self) -> ctk.CTkScrollableFrame:
        """Create the data frame."""
        return self.data_frame

    def create_bottom_frame(self) -> ctk.CTkFrame:
        """Create the bottom frame."""
        return self.bottom_frame

    def create_trainer_combobox_label(self) -> ctk.CTkLabel:
        """Create the trainer combobox label."""
        return self.trainer_combobox_label

    def create_trainer_combobox(self) -> ctk.CTkComboBox:
        """Create the trainer combobox."""
        return self.trainer_combobox

    def create_save_button(self) -> ctk.CTkButton:
        """Create the save button."""
        return self.save_button

    def create_status_label(self) -> ctk.CTkLabel:
        """Create the status label."""
        return self.status_label

    def create_output_directory_input(self) -> tuple[ctk.CTkLabel, ctk.CTkEntry]:
        """Let the user change the output directory."""
        return self.output_directory_label, self.output_directory_input

    def create_bfbs_file_input(self) -> tuple[ctk.CTkLabel, ctk.CTkEntry]:
        """Let the user change the BFBS file."""
        return self.bfbs_file_label, self.bfbs_file_input

    def _on_output_directory_change(self, *_: object) -> None:
        """On output directory change."""
        self.output_dir = self._output_dir_var.get()
        logger.trace(f"Output directory changed to: {self.output_dir}")

    def _on_bfbs_file_change(self, *_: object) -> None:
        """On BFBS file change."""
        self.bfbs_file = self._bfbs_file_var.get()
        logger.trace(f"BFBS file changed to: {self.bfbs_file}")

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

        # Create zoom controls
        self.create_zoom_controls()

        logger.trace(f"Created widgets ({type(self)}): {self}")

    def create_zoom_controls(self) -> None:
        """Create zoom control widgets."""
        # Access the cached properties to create them
        _ = self.zoom_frame
        _ = self.zoom_out_button
        _ = self.zoom_label
        _ = self.zoom_in_button
        _ = self.zoom_reset_button

    def create_trainer_data(self) -> TrainerFrame:
        """Display the current trainer's data."""
        trainer: ZATrainerData = self.trdata.values[0]

        # Basic Information Section
        basic_information_label = ctk.CTkLabel(
            self.data_frame,
            text="Basic Information",
            font=("Helvetica", 16, "bold"),
        )
        basic_information_label.pack(anchor="w", padx=10, pady=5)
        trainer_id_field = self._create_field(
            "Trainer ID",
            trainer.tr_id,
            readonly=True,
        )
        # Create fields with no setter initially - will configure after frame creation
        money_rate_field = self._create_field(
            "Money Rate",
            str(trainer.money_rate),
            setter=None,
        )

        # Flags and AI Settings in a horizontal layout
        flags_ai_frame = ctk.CTkFrame(self.data_frame, fg_color="transparent")
        flags_ai_frame.pack(fill="x", pady=(20, 5), padx=10)

        # Left column: Flags
        flags_column = ctk.CTkFrame(flags_ai_frame, fg_color="transparent")
        flags_column.pack(side="left", fill="both", expand=True, padx=(0, 20))

        flags_label = ctk.CTkLabel(
            flags_column,
            text="Flags",
            font=("Helvetica", 16, "bold"),
        )
        flags_label.pack(anchor="w", pady=(0, 5))

        # Flags row - checkboxes side by side
        flags_row = ctk.CTkFrame(flags_column, fg_color="transparent")
        flags_row.pack(fill="x", anchor="w")

        meg_evolution_checkbox = self._create_checkbox_inline(
            "Mega Evolution",
            trainer.meg_evolution,
            lambda v: None,
            parent=flags_row,
        )
        last_hand_checkbox = self._create_checkbox_inline(
            "Last Hand Mega",
            trainer.last_hand,
            lambda v: None,
            parent=flags_row,
        )

        # Right column: AI Settings
        ai_column = ctk.CTkFrame(flags_ai_frame, fg_color="transparent")
        ai_column.pack(side="left", fill="both", expand=True)

        ai_label = ctk.CTkLabel(
            ai_column,
            text="AI Settings",
            font=("Helvetica", 16, "bold"),
        )
        ai_label.pack(anchor="w", pady=(0, 5))

        # AI row 1 - first 4 checkboxes side by side
        ai_row_1 = ctk.CTkFrame(ai_column, fg_color="transparent")
        ai_row_1.pack(fill="x", anchor="w", pady=2)

        ai_basic_checkbox = self._create_checkbox_inline(
            "Basic",
            trainer.ai_basic,
            lambda v: None,
            parent=ai_row_1,
        )
        ai_high_checkbox = self._create_checkbox_inline(
            "High",
            trainer.ai_high,
            lambda v: None,
            parent=ai_row_1,
        )
        ai_expert_checkbox = self._create_checkbox_inline(
            "Expert",
            trainer.ai_expert,
            lambda v: None,
            parent=ai_row_1,
        )
        ai_double_checkbox = self._create_checkbox_inline(
            "Double",
            trainer.ai_double,
            lambda v: None,
            parent=ai_row_1,
        )

        # AI row 2 - next 4 checkboxes side by side
        ai_row_2 = ctk.CTkFrame(ai_column, fg_color="transparent")
        ai_row_2.pack(fill="x", anchor="w", pady=2)

        ai_raid_checkbox = self._create_checkbox_inline(
            "Raid",
            trainer.ai_raid,
            lambda v: None,
            parent=ai_row_2,
        )
        ai_weak_checkbox = self._create_checkbox_inline(
            "Weak",
            trainer.ai_weak,
            lambda v: None,
            parent=ai_row_2,
        )
        ai_item_checkbox = self._create_checkbox_inline(
            "Item",
            trainer.ai_item,
            lambda v: None,
            parent=ai_row_2,
        )
        ai_change_checkbox = self._create_checkbox_inline(
            "Change",
            trainer.ai_change,
            lambda v: None,
            parent=ai_row_2,
        )

        # View Settings Section - compact 2x2 layout
        view_settings_label = ctk.CTkLabel(
            self.data_frame,
            text="View Settings",
            font=("Helvetica", 16, "bold"),
        )
        view_settings_label.pack(pady=(20, 5), anchor="w", padx=10)

        # Row 1: Horizontal Angle and Vertical Angle
        view_row_1 = ctk.CTkFrame(self.data_frame, fg_color="transparent")
        view_row_1.pack(fill="x", padx=10, pady=2)

        view_horizontal_angle_field = self._create_field_inline(
            "H. Angle",
            str(trainer.view_horizontal_angle),
            parent=view_row_1,
        )
        view_vertical_angle_field = self._create_field_inline(
            "V. Angle",
            str(trainer.view_vertical_angle),
            parent=view_row_1,
        )

        # Row 2: View Range and Hearing Range
        view_row_2 = ctk.CTkFrame(self.data_frame, fg_color="transparent")
        view_row_2.pack(fill="x", padx=10, pady=2)

        view_range_field = self._create_field_inline(
            "View Range",
            str(trainer.view_range),
            parent=view_row_2,
        )
        hearing_range_field = self._create_field_inline(
            "Hearing Range",
            str(trainer.hearing_range),
            parent=view_row_2,
        )

        # Pokemon Section
        pokemon_label = ctk.CTkLabel(
            self.data_frame,
            text="Pokemon",
            font=("Helvetica", 16, "bold"),
        )
        pokemon_label.pack(pady=(20, 5), anchor="w")

        pokemon_fields: list[PkmnFrame] = [
            self._create_pokemon_field(1, trainer.poke_1),
            self._create_pokemon_field(2, trainer.poke_2),
            self._create_pokemon_field(3, trainer.poke_3),
            self._create_pokemon_field(4, trainer.poke_4),
            self._create_pokemon_field(5, trainer.poke_5),
            self._create_pokemon_field(6, trainer.poke_6),
        ]

        logger.trace(f"Displayed trainer data ({type(self)}): {self}")
        trainer_frame = TrainerFrame(
            basic_information_label=basic_information_label,
            trainer_id_field=trainer_id_field,
            money_rate_field=money_rate_field,
            flags_label=flags_label,
            meg_evolution_checkbox=meg_evolution_checkbox,
            last_hand_checkbox=last_hand_checkbox,
            ai_label=ai_label,
            ai_basic_checkbox=ai_basic_checkbox,
            ai_high_checkbox=ai_high_checkbox,
            ai_expert_checkbox=ai_expert_checkbox,
            ai_double_checkbox=ai_double_checkbox,
            ai_raid_checkbox=ai_raid_checkbox,
            ai_weak_checkbox=ai_weak_checkbox,
            ai_item_checkbox=ai_item_checkbox,
            ai_change_checkbox=ai_change_checkbox,
            view_settings_label=view_settings_label,
            view_horizontal_angle_field=view_horizontal_angle_field,
            view_vertical_angle_field=view_vertical_angle_field,
            view_range_field=view_range_field,
            hearing_range_field=hearing_range_field,
            pokemon_label=pokemon_label,
            pokemon_fields=pokemon_fields,
            trainer_ref=trainer,
        )

        # Now configure setters that use trainer_frame.trainer_ref
        self._configure_trainer_setters(trainer_frame)

        return trainer_frame

    def _create_pokemon_field(
        self,
        index: int,
        pkmn: ZAPokemonData,
    ) -> PkmnFrame:
        """Create a pokemon field."""
        # Show all pokemon slots, even if empty
        poke_frame = ctk.CTkFrame(self.data_frame)
        poke_frame.pack(fill="x", pady=5, padx=10)
        poke_title = ctk.CTkLabel(
            poke_frame,
            text=f"Pokemon {index}",
            font=("Helvetica", 14, "bold"),
        )
        poke_title.pack(anchor="w", padx=10, pady=5)

        # Horizontal layout: Pokemon details on left, Moves on right
        content_frame = ctk.CTkFrame(poke_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=5)

        # Left column: Pokemon details
        details_column = ctk.CTkFrame(content_frame, fg_color="transparent")
        details_column.pack(side="left", fill="both", expand=True)

        # Create dropdowns/fields with placeholder setters initially
        # We'll reconfigure them after creating the frame
        dev_id_field = self._create_dropdown(
            "Dev ID",
            pkmn.dev_id_english,
            values=SPECIES,
            setter=lambda v: None,
            parent=details_column,
        )

        item_field = self._create_dropdown(
            "Item",
            pkmn.item_english,
            values=ITEMS,
            setter=lambda v: None,
            parent=details_column,
        )

        # Row for Level, Form ID, Sex (compact)
        stats_row = ctk.CTkFrame(details_column, fg_color="transparent")
        stats_row.pack(fill="x", padx=10, pady=2)

        level_field = self._create_field_inline(
            "Lv",
            str(pkmn.level),
            parent=stats_row,
            width=50,
        )

        form_id_field = self._create_field_inline(
            "Form",
            str(pkmn.form_id),
            parent=stats_row,
            width=50,
        )

        sex_field = self._create_dropdown_inline(
            "Sex",
            str(pkmn.sex),
            [str(x) for x in ty.get_args(Sex)],
            setter=lambda v: None,
            parent=stats_row,
        )

        # Row for Ball ID and Scale Value (compact)
        extra_row = ctk.CTkFrame(details_column, fg_color="transparent")
        extra_row.pack(fill="x", padx=10, pady=2)

        ball_id_field = self._create_dropdown_inline(
            "Ball",
            pkmn.ball_id_english,
            [settings.za_items_table[ball_id] for ball_id in ty.get_args(ZABallID)],
            setter=lambda v: None,
            parent=extra_row,
        )

        scale_value_field = self._create_field_inline(
            "Scale",
            str(pkmn.scale_value),
            parent=extra_row,
            width=50,
        )

        # Right column: Moves
        moves_column = ctk.CTkFrame(content_frame, fg_color="transparent")
        moves_column.pack(side="left", fill="both", expand=True, padx=(20, 0))

        waza_label = ctk.CTkLabel(
            moves_column,
            text="Moves",
            font=("Helvetica", 12, "bold"),
        )
        waza_label.pack(anchor="w", pady=(0, 5))

        waza_frames: list[WazaFrame] = [
            self._create_waza_field(1, pkmn.waza_1, moves_column),
            self._create_waza_field(2, pkmn.waza_2, moves_column),
            self._create_waza_field(3, pkmn.waza_3, moves_column),
            self._create_waza_field(4, pkmn.waza_4, moves_column),
        ]

        # Create the frame first
        pkmn_frame = PkmnFrame(
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
            pokemon_ref=pkmn,
        )

        # Now configure setters that use pkmn_frame.pokemon_ref
        # This ensures changes always go to the currently selected pokemon
        def on_dev_id_change(val: str) -> None:
            """On Dev ID Change."""
            logger.trace(f"On Dev ID Change: {val}")
            pkmn_frame.pokemon_ref.dev_id = settings.za_species_table.index(val)
            logger.trace(f"New Dev ID: {pkmn_frame.pokemon_ref.dev_id} | {val}")

        def on_item_change(val: str) -> None:
            """On Item Change."""
            logger.trace(f"On Item Change: {val}")
            pkmn_frame.pokemon_ref.item = settings.za_items_table.index(val)
            logger.trace(f"New Item: {pkmn_frame.pokemon_ref.item} | {val}")

        def on_level_change(val: str) -> None:
            """On Level Change."""
            logger.trace(f"On Level Change: {val}")
            pkmn_frame.pokemon_ref.level = int(val)
            logger.trace(f"New Level: {pkmn_frame.pokemon_ref.level} | {val}")

        def on_form_id_change(val: str) -> None:
            """On Form ID Change."""
            logger.trace(f"On Form ID Change: {val}")
            pkmn_frame.pokemon_ref.form_id = int(val)  # type: ignore
            logger.trace(f"New Form ID: {pkmn_frame.pokemon_ref.form_id} | {val}")

        def on_sex_change(val: str) -> None:
            """On Sex Change."""
            logger.trace(f"On Sex Change: {val}")
            pkmn_frame.pokemon_ref.sex = int(val)  # type: ignore
            logger.trace(f"New Sex: {pkmn_frame.pokemon_ref.sex} | {val}")

        def on_ball_id_change(val: str) -> None:
            """On Ball ID Change."""
            logger.trace(f"On Ball ID Change: {val}")
            pkmn_frame.pokemon_ref.ball_id = settings.za_items_table.index(val)  # type: ignore
            logger.trace(f"New Ball ID: {pkmn_frame.pokemon_ref.ball_id} | {val}")

        def on_scale_value_change(val: str) -> None:
            """On Scale Value Change."""
            logger.trace(f"On Scale Value Change: {val}")
            pkmn_frame.pokemon_ref.scale_value = int(val)
            logger.trace(
                f"New Scale Value: {pkmn_frame.pokemon_ref.scale_value} | {val}"
            )

        # Reconfigure the option menus with proper setters
        dev_id_field.option_menu.configure(command=on_dev_id_change)
        item_field.option_menu.configure(command=on_item_change)
        sex_field.option_menu.configure(command=on_sex_change)
        ball_id_field.option_menu.configure(command=on_ball_id_change)

        # For entry fields, add trace callbacks
        level_field.var.trace_add(
            "write", lambda *args: on_level_change(level_field.var.get())
        )
        form_id_field.var.trace_add(
            "write", lambda *args: on_form_id_change(form_id_field.var.get())
        )
        scale_value_field.var.trace_add(
            "write", lambda *args: on_scale_value_change(scale_value_field.var.get())
        )

        # Reconfigure waza frame setters
        self._configure_waza_setters(pkmn_frame)

        return pkmn_frame

    def _create_waza_field(
        self,
        index: int,
        waza: ZAWazaData,
        parent: ctk.CTkFrame,
    ) -> WazaFrame:
        """Create a waza field."""
        # Create a frame for each move
        waza_frame_widget = ctk.CTkFrame(parent)
        waza_frame_widget.pack(fill="x", pady=2, padx=10)
        waza_name_label = ctk.CTkLabel(
            waza_frame_widget, text=f"Move {index}:", width=100
        )
        waza_name_label.pack(anchor="w", padx=10, pady=5)

        waza_variable = ctk.StringVar(value=waza.waza_id_english)
        waza_option_menu = ctk.CTkOptionMenu(
            waza_frame_widget,
            values=WAZAS,
            command=lambda v: None,  # Placeholder, will be configured later
            variable=waza_variable,
        )
        waza_option_menu.pack(side="left", fill="x", expand=True, padx=5)

        plus_var = ctk.BooleanVar(value=waza.is_plus_waza)
        plus_checkbox = ctk.CTkCheckBox(
            waza_frame_widget,
            text="Plus Waza",
            variable=plus_var,
            command=lambda: None,  # Placeholder, will be configured later
        )

        return WazaFrame(
            frame=waza_frame_widget,
            name_label=waza_name_label,
            waza_variable=waza_variable,
            option_menu=waza_option_menu,
            plus_var=plus_var,
            plus_checkbox=plus_checkbox,
            waza_ref=waza,
        )

    def _configure_waza_setters(self, pkmn_frame: PkmnFrame) -> None:
        """Configure waza setters to use waza_ref from the frame.

        This must be called after the PkmnFrame is created so that
        the setters can reference waza_ref which gets updated when
        a new trainer is selected.
        """
        for waza_frame in pkmn_frame.waza_frames:

            def make_on_waza_change(wf: WazaFrame) -> ty.Callable[[str], None]:
                """Factory to create waza change handler with proper closure."""

                def on_waza_change(val: str) -> None:
                    logger.trace(f"On Waza Change: {val}")
                    wf.waza_ref.waza_id = settings.za_waza_table.index(val)
                    logger.trace(f"New Waza ID: {wf.waza_ref.waza_id} | {val}")

                return on_waza_change

            def make_on_plus_change(wf: WazaFrame) -> ty.Callable[[], None]:
                """Factory to create plus change handler with proper closure."""

                def on_plus_change() -> None:
                    logger.trace(f"On Plus Change: {wf.waza_ref.is_plus_waza}")
                    wf.waza_ref.is_plus_waza = not wf.waza_ref.is_plus_waza
                    logger.trace(f"New Plus Waza: {wf.waza_ref.is_plus_waza}")

                return on_plus_change

            waza_frame.option_menu.configure(command=make_on_waza_change(waza_frame))
            waza_frame.plus_checkbox.configure(command=make_on_plus_change(waza_frame))

    def _configure_trainer_setters(self, trainer_frame: TrainerFrame) -> None:
        """Configure trainer setters to use trainer_ref from the frame.

        This must be called after the TrainerFrame is created so that
        the setters can reference trainer_ref which gets updated when
        a new trainer is selected.
        """
        tf = trainer_frame  # Short alias

        # Configure field setters via var.trace_add
        def on_money_rate_change(*_: object) -> None:
            _set_attr(tf.trainer_ref, "money_rate", tf.money_rate_field.var.get(), int)

        def on_view_horizontal_angle_change(*_: object) -> None:
            _set_attr(
                tf.trainer_ref,
                "view_horizontal_angle",
                tf.view_horizontal_angle_field.var.get(),
                float,
            )

        def on_view_vertical_angle_change(*_: object) -> None:
            _set_attr(
                tf.trainer_ref,
                "view_vertical_angle",
                tf.view_vertical_angle_field.var.get(),
                float,
            )

        def on_view_range_change(*_: object) -> None:
            _set_attr(
                tf.trainer_ref, "view_range", tf.view_range_field.var.get(), float
            )

        def on_hearing_range_change(*_: object) -> None:
            _set_attr(
                tf.trainer_ref, "hearing_range", tf.hearing_range_field.var.get(), float
            )

        tf.money_rate_field.var.trace_add("write", on_money_rate_change)
        tf.view_horizontal_angle_field.var.trace_add(
            "write", on_view_horizontal_angle_change
        )
        tf.view_vertical_angle_field.var.trace_add(
            "write", on_view_vertical_angle_change
        )
        tf.view_range_field.var.trace_add("write", on_view_range_change)
        tf.hearing_range_field.var.trace_add("write", on_hearing_range_change)

        # Configure checkbox setters
        def make_checkbox_setter(
            attr_name: str,
        ) -> ty.Callable[[str, str, str], None]:
            """Factory to create checkbox setter."""

            def setter(*_: object) -> None:
                checkbox = getattr(tf, f"{attr_name}_checkbox")
                setattr(tf.trainer_ref, attr_name, bool(checkbox.var.get()))

            return setter

        # Map checkbox attributes to their names
        checkbox_attrs = [
            "meg_evolution",
            "last_hand",
            "ai_basic",
            "ai_high",
            "ai_expert",
            "ai_double",
            "ai_raid",
            "ai_weak",
            "ai_item",
            "ai_change",
        ]

        for attr in checkbox_attrs:
            checkbox = getattr(tf, f"{attr}_checkbox")
            checkbox.var.trace_add("write", make_checkbox_setter(attr))

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

    def _create_field_inline(
        self,
        label_text: str,
        value: str,
        parent: ctk.CTkFrame,
        setter: ty.Callable[[str], None] | None = None,
        width: int = 80,
    ) -> FieldFrame:
        """Create a compact inline field that packs horizontally."""
        logger.trace(f"Creating inline field: {label_text} = {value}")

        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(side="left", padx=(0, 20), pady=2)

        label = ctk.CTkLabel(field_frame, text=f"{label_text}:")
        label.pack(side="left", padx=(0, 5))

        var = ctk.StringVar(value=value)
        if setter:
            var.trace_add("write", lambda *args: setter(var.get()))
        entry = ctk.CTkEntry(field_frame, textvariable=var, width=width)
        entry.pack(side="left")

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
        parent: ctk.CTkFrame | None = None,
    ) -> CheckboxFrame:
        """Create a checkbox field."""
        logger.trace(f"Creating checkbox: {label_text} = {value}")
        parent_frame = parent or self.data_frame
        # Use IntVar for checkbox variable
        var = ctk.IntVar(value=1 if value else 0)
        var.trace_add("write", lambda *args: setter(bool(var.get())))

        checkbox = ctk.CTkCheckBox(parent_frame, text=label_text, variable=var)
        checkbox.pack(anchor="w", padx=20, pady=2)

        return CheckboxFrame(
            var=var,
            checkbox=checkbox,
        )

    def _create_checkbox_inline(
        self,
        label_text: str,
        value: bool,
        setter: ty.Callable[[bool], None],
        parent: ctk.CTkFrame,
    ) -> CheckboxFrame:
        """Create a checkbox that packs horizontally (inline with siblings)."""
        logger.trace(f"Creating inline checkbox: {label_text} = {value}")
        # Use IntVar for checkbox variable
        var = ctk.IntVar(value=1 if value else 0)
        var.trace_add("write", lambda *args: setter(bool(var.get())))

        checkbox = ctk.CTkCheckBox(parent, text=label_text, variable=var)
        checkbox.pack(side="left", padx=(0, 15), pady=2)

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

    def _create_dropdown_inline(
        self,
        label_text: str,
        value: str,
        values: list[str],
        setter: ty.Callable[[str], None],
        parent: ctk.CTkFrame,
        width: int = 100,
    ) -> DropdownFrame:
        """Create a compact inline dropdown that packs horizontally."""
        logger.trace(f"Creating inline dropdown: {label_text} = {value}")

        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(side="left", padx=(0, 15), pady=2)

        label = ctk.CTkLabel(field_frame, text=f"{label_text}:")
        label.pack(side="left", padx=(0, 5))

        values_sorted = sorted(values)
        option_menu = ctk.CTkOptionMenu(
            field_frame, values=values_sorted, command=setter, width=width
        )
        option_menu.set(value)
        option_menu.pack(side="left")

        return DropdownFrame(
            field_frame=field_frame,
            label=label,
            option_menu=option_menu,
        )

    def on_trainer_selected(self, trainer_id: str) -> None:
        """Handle trainer selection from combobox.

        Args:
            trainer_id (str):
                The choice from the combobox.
                This is the trainer ID.
        """
        # Find the index of the selected trainer
        trainer: ZATrainerData = self.trdata.get_trainer(trainer_id)

        # Update displayed data
        self.trainer_frame.update_trainer_data(trainer)

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
            file_out = os.path.join(output_dir, file_name)
            logger.trace(f"Dumping data to {file_out}...")
            self.trdata.dump(file_out, bfbs_file=bfbs_file, create_binaries=True)
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

    def zoom_in(self, event: tk.Event | None = None) -> None:
        """Zoom in (increase scale)."""
        new_scale = min(self._scale + self._scale_step, self._scale_max)
        if new_scale != self._scale:
            self._scale = new_scale
            self._apply_scale()
            logger.trace(f"Zoomed in to {self._scale:.0%}")

    def zoom_out(self, event: tk.Event | None = None) -> None:
        """Zoom out (decrease scale)."""
        new_scale = max(self._scale - self._scale_step, self._scale_min)
        if new_scale != self._scale:
            self._scale = new_scale
            self._apply_scale()
            logger.trace(f"Zoomed out to {self._scale:.0%}")

    def zoom_reset(self, event: tk.Event | None = None) -> None:
        """Reset zoom to 100%."""
        if self._scale != 1.0:
            self._scale = 1.0
            self._apply_scale()
            logger.trace("Zoom reset to 100%")

    def _apply_scale(self) -> None:
        """Apply the current scale to widgets."""
        ctk.set_widget_scaling(self._scale)
        self.zoom_label.configure(text=f"{self._scale:.0%}")
        logger.trace(f"Applied scale: {self._scale:.0%}")

    def _bind_zoom_shortcuts(self) -> None:
        """Bind keyboard shortcuts for zooming."""
        # Cmd/Ctrl + Plus to zoom in
        self.bind("<Command-plus>", self.zoom_in)
        self.bind("<Command-equal>", self.zoom_in)  # For keyboards where + is Shift+=
        self.bind("<Control-plus>", self.zoom_in)
        self.bind("<Control-equal>", self.zoom_in)

        # Cmd/Ctrl + Minus to zoom out
        self.bind("<Command-minus>", self.zoom_out)
        self.bind("<Control-minus>", self.zoom_out)

        # Cmd/Ctrl + 0 to reset zoom
        self.bind("<Command-0>", self.zoom_reset)
        self.bind("<Control-0>", self.zoom_reset)

        logger.trace("Zoom shortcuts bound")
