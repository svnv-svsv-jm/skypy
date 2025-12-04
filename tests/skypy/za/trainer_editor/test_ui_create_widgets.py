from unittest import mock

import pytest
from loguru import logger

from skypy.za import ZATrainerEditor


def test_create_widgets() -> None:
    """Test `create_widgets` method."""
    with (
        mock.patch.object(
            ZATrainerEditor, "create_trainer_data"
        ) as create_trainer_data,
        mock.patch.object(
            ZATrainerEditor, "create_output_directory_input"
        ) as create_output_directory_input,
        mock.patch.object(
            ZATrainerEditor, "create_bfbs_file_input"
        ) as create_bfbs_file_input,
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
        create_bfbs_file_input.assert_called_once()
        create_output_directory_input.assert_called_once()
        create_trainer_data.assert_called_once()
        create_top_frame.assert_called_once()
        create_trainer_combobox.assert_called_once()
        create_data_frame.assert_called_once()
        create_bottom_frame.assert_called_once()
        create_save_button.assert_called_once()
        create_status_label.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
