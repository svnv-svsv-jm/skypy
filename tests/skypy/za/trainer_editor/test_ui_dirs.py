from unittest.mock import patch

import customtkinter as ctk
import pytest

from skypy.za import ZATrainerEditor


def test_create_output_directory_input(za_trainer_editor_app: ZATrainerEditor) -> None:
    """Test `create_output_directory_input` method."""
    ui = za_trainer_editor_app
    with (
        patch.object(ctk.CTkLabel, "__init__", return_value=None) as __init__,
        patch.object(ctk.CTkLabel, "pack", return_value=None) as pack,
        patch.object(ctk.CTkEntry, "__init__", return_value=None) as entry_init,
        patch.object(ctk.CTkEntry, "pack", return_value=None) as entry_pack,
    ):
        ui.create_top_frame()
        ui.create_output_directory_input()
        __init__.assert_called_once()
        pack.assert_called_once()
        entry_init.assert_called_with(
            ui.top_frame, textvariable=ui._output_dir_var, width=200
        )
        entry_pack.assert_called_with(side="left", padx=(0, 10))


def test_create_bfbs_file_input(za_trainer_editor_app: ZATrainerEditor) -> None:
    """Test `create_bfbs_file_input` method."""
    ui = za_trainer_editor_app
    with (
        patch.object(ctk.CTkLabel, "__init__", return_value=None) as __init__,
        patch.object(ctk.CTkLabel, "pack", return_value=None) as pack,
        patch.object(ctk.CTkEntry, "__init__", return_value=None) as entry_init,
        patch.object(ctk.CTkEntry, "pack", return_value=None) as entry_pack,
    ):
        ui.create_top_frame()
        ui.create_bfbs_file_input()
        __init__.assert_called_once()
        pack.assert_called_once()
        entry_init.assert_called_with(
            ui.top_frame, textvariable=ui._bfbs_file_var, width=200
        )
        entry_pack.assert_called_with(side="left", padx=(0, 10))


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
