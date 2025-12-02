from unittest.mock import patch

import customtkinter as ctk
import pytest
from loguru import logger

from skypy.za import ZATrainerEditor


def test_create_trainer_combobox(za_trainer_editor_app: ZATrainerEditor) -> None:
    """Test `create_trainer_combobox` method."""
    ui = za_trainer_editor_app
    with (
        patch.object(ctk.CTkScrollableFrame, "__init__", return_value=None) as __init__,
        patch.object(ctk.CTkScrollableFrame, "pack", return_value=None) as pack,
    ):
        ui.create_data_frame()
        __init__.assert_called_once_with(ui)
        pack.assert_called_once()


def test_create_bottom_frame(za_trainer_editor_app: ZATrainerEditor) -> None:
    """Test `create_bottom_frame` method."""
    ui = za_trainer_editor_app
    with (
        patch.object(ctk.CTkFrame, "__init__", return_value=None) as __init__,
        patch.object(ctk.CTkFrame, "pack", return_value=None) as pack,
    ):
        ui.create_bottom_frame()
        __init__.assert_called_once_with(ui)
        pack.assert_called_once()


def test_create_save_button(za_trainer_editor_app: ZATrainerEditor) -> None:
    """Test `create_save_button` method."""
    ui = za_trainer_editor_app
    with (
        patch.object(ctk.CTkButton, "__init__", return_value=None) as __init__,
        patch.object(ctk.CTkButton, "pack", return_value=None) as pack,
    ):
        with pytest.raises(AttributeError):
            ui.create_save_button()
        ui.create_bottom_frame()
        ui.create_save_button()
        __init__.assert_called_once()
        pack.assert_called_once()


def test_create_status_label(za_trainer_editor_app: ZATrainerEditor) -> None:
    """Test `create_status_label` method."""
    ui = za_trainer_editor_app
    with (
        patch.object(ctk.CTkLabel, "__init__", return_value=None) as __init__,
        patch.object(ctk.CTkLabel, "pack", return_value=None) as pack,
    ):
        with pytest.raises(AttributeError):
            ui.create_status_label()
        ui.create_bottom_frame()
        ui.create_status_label()
        __init__.assert_called_once()
        pack.assert_called_once()


def test_create_output_directory_input(za_trainer_editor_app: ZATrainerEditor) -> None:
    """Test `create_output_directory_input` method."""
    ui = za_trainer_editor_app
    with (
        patch.object(ctk.CTkLabel, "__init__", return_value=None) as __init__,
        patch.object(ctk.CTkLabel, "pack", return_value=None) as pack,
    ):
        ui.create_top_frame()
        ui.create_output_directory_input()
        __init__.assert_called_once()
        pack.assert_called_once()


def test_create_bfbs_file_input(za_trainer_editor_app: ZATrainerEditor) -> None:
    """Test `create_bfbs_file_input` method."""
    ui = za_trainer_editor_app
    with (
        patch.object(ctk.CTkLabel, "__init__", return_value=None) as __init__,
        patch.object(ctk.CTkLabel, "pack", return_value=None) as pack,
    ):
        ui.create_top_frame()
        ui.create_bfbs_file_input()
        __init__.assert_called_once()
        pack.assert_called_once()


def test_running_ui_locally(running_locally: bool) -> None:
    """Test layout - manual visual test."""
    if not running_locally:
        pytest.skip("Skipping manual visual test.")
    ui = ZATrainerEditor()
    logger.info(f"UI: {ui}")


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
