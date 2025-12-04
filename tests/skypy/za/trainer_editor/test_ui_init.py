import os
from unittest import mock

import customtkinter as ctk
import pytest
from loguru import logger

from skypy.schemas import ZATrainerDataArray
from skypy.za import TrainerFrame, ZATrainerEditor


@pytest.mark.parametrize("output_dir", ["assets/za/Output"])
@pytest.mark.parametrize("title", ["Test UI"])
@pytest.mark.parametrize("width", [950])
@pytest.mark.parametrize("height", [900])
def test_ui_initialization_simple(
    output_dir: str,
    title: str,
    width: int,
    height: int,
) -> None:
    """Test UI initialization: test that some attributes are set correctly."""
    fname = os.path.join(output_dir, "trdata_array.json")
    if os.path.exists(fname):
        os.remove(fname)

    with (
        mock.patch.object(ZATrainerEditor, "withdraw") as withdraw,
        mock.patch.object(ZATrainerEditor, "title") as ttile,
        mock.patch.object(ZATrainerEditor, "geometry") as geometry,
    ):
        ui = ZATrainerEditor(
            visible=False,
            output_dir=output_dir,
            title=title,
            width=width,
            height=height,
        )
        logger.info(f"UI: {ui}")

    withdraw.assert_called_once()
    ttile.assert_called_with(title)
    geometry.assert_called_with(f"{width}x{height}")
    assert ui.output_dir == output_dir
    assert ui.app_title == title
    assert isinstance(ui.trdata, ZATrainerDataArray)
    assert isinstance(ui._output_dir_var, ctk.StringVar)
    assert isinstance(ui._bfbs_file_var, ctk.StringVar)
    assert isinstance(ui.top_frame, ctk.CTkFrame)
    assert isinstance(ui.trainer_frame, TrainerFrame)
    assert isinstance(ui.data_frame, ctk.CTkScrollableFrame)
    assert isinstance(ui.bottom_frame, ctk.CTkFrame)
    assert isinstance(ui.trainer_frame.pokemon_label, ctk.CTkLabel)

    # Test Trainer combobox
    assert isinstance(ui.trainer_combobox, ctk.CTkComboBox)
    assert isinstance(ui.trainer_combobox_label, ctk.CTkLabel)
    assert ui.trainer_combobox_label._text == "Select Trainer:"
    assert ui.trainer_combobox.get() == ui.trdata.values[0].tr_id
    assert ui.trainer_combobox._values == [
        trainer.tr_id for trainer in ui.trdata.values
    ]
    assert ui.trainer_combobox._command == ui.on_trainer_selected

    # Test Save button
    assert isinstance(ui.save_button, ctk.CTkButton)
    assert ui.save_button._text == "Save Changes"
    assert ui.save_button._command == ui.save_trainer_data

    # Test Status label
    assert isinstance(ui.status_label, ctk.CTkLabel)
    assert ui.status_label._text == "Have fun!"
    assert ui.status_label._text_color == "white"

    # Test Output directory
    assert isinstance(ui.output_directory_label, ctk.CTkLabel)
    assert isinstance(ui.output_directory_input, ctk.CTkEntry)
    assert isinstance(ui._output_dir_var, ctk.StringVar)
    assert ui.output_directory_label._text == "Output Directory:"
    assert ui.output_directory_input._textvariable == ui._output_dir_var

    # Test
    assert isinstance(ui.bfbs_file_label, ctk.CTkLabel)
    assert isinstance(ui.bfbs_file_input, ctk.CTkEntry)
    assert isinstance(ui._bfbs_file_var, ctk.StringVar)
    assert ui.bfbs_file_label._text == "BFBS File:"
    assert ui.bfbs_file_input._textvariable == ui._bfbs_file_var


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
