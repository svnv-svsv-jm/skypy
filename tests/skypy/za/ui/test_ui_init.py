from unittest import mock

import pydantic
import pytest

from skypy.schemas import ZATrainerData
from skypy.za import ZATrainerEditor


@pytest.mark.parametrize("input_dir", ["assets/za/Raw", "assets/za/Output"])
@pytest.mark.parametrize("output_dir", ["assets/za/Raw", "assets/za/Output"])
def test_ui_initialization_simple(
    input_dir: str,
    output_dir: str,
) -> None:
    """Test UI initialization: test that some attributes are set correctly."""
    with mock.patch.object(ZATrainerEditor, "withdraw") as withdraw:
        ui = ZATrainerEditor(
            visible=False,
            input_dir=input_dir,
            output_dir=output_dir,
            title="Test UI Initialization",
        )
    withdraw.assert_called_once()
    assert ui.selected_trainer_index == 0
    assert ui.input_dir == input_dir
    assert ui.output_dir == output_dir
    assert ui.app_title == "Test UI Initialization"

    pydantic.TypeAdapter(list[ZATrainerData]).validate_python(ui.trdata)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
