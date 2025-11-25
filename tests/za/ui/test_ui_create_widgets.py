from unittest import mock

import customtkinter as ctk
import pytest
from loguru import logger

from skypy.schemas import ZATrainerDataArray
from skypy.za import ZATrainerEditor


def test_create_widgets(zatrdata: ZATrainerDataArray) -> None:
    """Test `create_widgets` method."""
    with (
        mock.patch.object(
            ZATrainerEditor,
            "load_trainer_data",
            return_value=zatrdata.values,
        ) as load_trainer_data,
        mock.patch.object(
            ZATrainerEditor, "display_trainer_data"
        ) as display_trainer_data,
        mock.patch.object(ZATrainerEditor, "create_top_frame") as create_top_frame,
        mock.patch.object(
            ZATrainerEditor, "create_trainer_combobox"
        ) as create_trainer_combobox,
        mock.patch.object(ZATrainerEditor, "create_data_frame") as create_data_frame,
        mock.patch.object(
            ZATrainerEditor, "create_bottom_frame"
        ) as create_bottom_frame,
        mock.patch.object(ZATrainerEditor, "create_save_button") as create_save_button,
        mock.patch.object(
            ZATrainerEditor, "create_status_label"
        ) as create_status_label,
    ):
        ui = ZATrainerEditor(visible=False)
        logger.info(f"UI: {ui}")
        load_trainer_data.assert_called_once()
        display_trainer_data.assert_called_once()
        create_top_frame.assert_called_once()
        create_trainer_combobox.assert_called_once()
        create_data_frame.assert_called_once()
        create_bottom_frame.assert_called_once()
        create_save_button.assert_called_once()
        create_status_label.assert_called_once()


def test_create_top_frame(za_trainer_editor_app: ZATrainerEditor) -> None:
    """Test `create_top_frame` method."""
    ui = za_trainer_editor_app
    with (
        mock.patch.object(ZATrainerEditor, "display_trainer_data"),
        mock.patch.object(ctk.CTkFrame, "__init__", return_value=None) as __init__,
        mock.patch.object(ctk.CTkFrame, "pack", return_value=None) as pack,
    ):
        ui.create_top_frame()
        __init__.assert_called_once_with(ui)
        pack.assert_called_once_with(fill="x", padx=10, pady=10)


def test_create_trainer_combobox(za_trainer_editor_app: ZATrainerEditor) -> None:
    """Test `create_trainer_combobox` method."""
    ui = za_trainer_editor_app
    with (
        mock.patch.object(ZATrainerEditor, "display_trainer_data"),
        mock.patch.object(
            ctk.CTkLabel, "__init__", side_effect=ctk.CTkLabel.__init__, autospec=True
        ) as label_init,
    ):
        ui.create_trainer_combobox()
        label_init.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
