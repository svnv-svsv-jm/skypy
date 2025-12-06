from unittest.mock import MagicMock, patch

import customtkinter as ctk
import pytest

from skypy.za import ZATrainerEditor
from skypy.za.trainer_editor import _set_attr


def test_set_attr() -> None:
    """Test `_set_attr` method."""
    obj = MagicMock()
    _set_attr(obj, "money_rate", "100", dtype=int)
    assert obj.money_rate == 100

    _set_attr(obj, "money_rate", "true", dtype=bool)
    assert obj.money_rate is True


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
        ui.create_status_label()
        __init__.assert_called_once()
        pack.assert_called_once()


@pytest.mark.parametrize("readonly", [True, False])
def test__create_field(readonly: bool) -> None:
    """Test `_create_field` method."""
    ui = ZATrainerEditor()
    ui._create_field(
        label_text="Money Rate",
        value="100",
        setter=lambda *args, **kwargs: None,  # type: ignore
        readonly=readonly,
    )


def test_on_trainer_selected() -> None:
    """Test `on_trainer_selected` method."""
    with patch.object(ZATrainerEditor, "display_trainer_data") as display_trainer_data:
        ui = ZATrainerEditor(visible=False)
        ui.on_trainer_selected(ui.trdata.values[0].tr_id)
        assert ui.selected_trainer_index == 0
        display_trainer_data.assert_called()


def test__on_bfbs_file_change() -> None:
    """Test `_on_bfbs_file_change` method."""
    ui = ZATrainerEditor()
    with patch.object(
        ui._bfbs_file_var, "get", return_value="test.bfbs"
    ) as bfbs_file_var:
        ui._on_bfbs_file_change()
        bfbs_file_var.assert_called_once()
        assert ui.bfbs_file == "test.bfbs"


def test__on_output_directory_change() -> None:
    """Test `_on_output_directory_change` method."""
    ui = ZATrainerEditor()
    with patch.object(
        ui._output_dir_var, "get", return_value="test/output"
    ) as output_dir_var:
        ui._on_output_directory_change()
        output_dir_var.assert_called_once()
        assert ui.output_dir == "test/output"


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
