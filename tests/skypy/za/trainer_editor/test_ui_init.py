import os
from unittest import mock

import customtkinter as ctk
import pydantic
import pytest
from loguru import logger

from skypy.schemas import ZATrainerData
from skypy.za import CheckboxFrame, FieldFrame, PkmnFrame, ZATrainerEditor


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
    assert ui.selected_trainer_index == 0
    assert ui.output_dir == output_dir
    assert ui.app_title == title
    assert isinstance(ui._output_dir_var, ctk.StringVar)
    assert isinstance(ui._bfbs_file_var, ctk.StringVar)
    assert isinstance(ui.top_frame, ctk.CTkFrame)
    assert isinstance(ui.trainer_combobox_label, ctk.CTkLabel)
    assert isinstance(ui.trainer_combobox, ctk.CTkComboBox)
    assert isinstance(ui.data_frame, ctk.CTkScrollableFrame)
    assert isinstance(ui.bottom_frame, ctk.CTkFrame)
    assert isinstance(ui.save_button, ctk.CTkButton)
    assert isinstance(ui.status_label, ctk.CTkLabel)
    assert isinstance(ui.output_directory_label, ctk.CTkLabel)
    assert isinstance(ui.output_directory_input, ctk.CTkEntry)
    assert isinstance(ui.bfbs_file_label, ctk.CTkLabel)
    assert isinstance(ui.bfbs_file_input, ctk.CTkEntry)
    assert isinstance(ui.basic_information_label, ctk.CTkLabel)
    assert isinstance(ui.flags_label, ctk.CTkLabel)
    assert isinstance(ui.trainer_id_field, FieldFrame)
    assert isinstance(ui.money_rate_field, FieldFrame)
    assert isinstance(ui.meg_evolution_checkbox, CheckboxFrame)
    assert isinstance(ui.last_hand_checkbox, CheckboxFrame)
    assert isinstance(ui.ai_label, ctk.CTkLabel)
    assert isinstance(ui.ai_basic_checkbox, CheckboxFrame)
    assert isinstance(ui.ai_high_checkbox, CheckboxFrame)
    assert isinstance(ui.ai_expert_checkbox, CheckboxFrame)
    assert isinstance(ui.ai_double_checkbox, CheckboxFrame)
    assert isinstance(ui.ai_raid_checkbox, CheckboxFrame)
    assert isinstance(ui.ai_weak_checkbox, CheckboxFrame)
    assert isinstance(ui.ai_item_checkbox, CheckboxFrame)
    assert isinstance(ui.ai_change_checkbox, CheckboxFrame)
    assert isinstance(ui.view_settings_label, ctk.CTkLabel)
    assert isinstance(ui.view_horizontal_angle_field, FieldFrame)
    assert isinstance(ui.view_vertical_angle_field, FieldFrame)
    assert isinstance(ui.view_range_field, FieldFrame)
    assert isinstance(ui.hearing_range_field, FieldFrame)
    assert isinstance(ui.pokemon_label, ctk.CTkLabel)
    pydantic.TypeAdapter(list[PkmnFrame]).validate_python(ui.pokemon_fields)

    pydantic.TypeAdapter(list[ZATrainerData]).validate_python(ui.trdata)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
