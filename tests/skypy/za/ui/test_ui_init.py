import os
from unittest import mock

import pydantic
import pytest
from loguru import logger

from skypy.schemas import ZATrainerData
from skypy.za import ZATrainerEditor


@pytest.mark.parametrize("output_dir", ["assets/za/Output"])
def test_ui_initialization_simple(output_dir: str) -> None:
    """Test UI initialization: test that some attributes are set correctly."""
    try:
        os.remove(os.path.join(output_dir, "trdata_array.json"))
    except FileNotFoundError:
        pass

    with (
        mock.patch.object(ZATrainerEditor, "withdraw") as withdraw,
        mock.patch.object(ZATrainerEditor, "create_widgets") as create_widgets,
        mock.patch.object(
            ZATrainerEditor, "display_trainer_data"
        ) as display_trainer_data,
    ):
        ui = ZATrainerEditor(
            visible=False,
            output_dir=output_dir,
            title="Test UI Initialization",
        )
        logger.info(f"UI: {ui}")

    create_widgets.assert_called_once()
    display_trainer_data.assert_called_once()
    withdraw.assert_called_once()
    assert ui.selected_trainer_index == 0
    assert ui.output_dir == output_dir
    assert ui.app_title == "Test UI Initialization"

    pydantic.TypeAdapter(list[ZATrainerData]).validate_python(ui.trdata)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
