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
    with mock.patch.object(ZATrainerEditor, "withdraw") as withdraw:
        ui = ZATrainerEditor(
            visible=False,
            output_dir=output_dir,
            title="Test UI Initialization",
        )
        logger.info(f"UI: {ui}")
    withdraw.assert_called_once()
    assert ui.selected_trainer_index == 0
    assert ui.output_dir == output_dir
    assert ui.app_title == "Test UI Initialization"

    pydantic.TypeAdapter(list[ZATrainerData]).validate_python(ui.trdata)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
