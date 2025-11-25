from unittest import mock

import pydantic
import pytest

from skypy.schemas import ZATrainerData
from skypy.za import ZATrainerEditor


@pytest.mark.parametrize("input_dir", ["assets/za/Input", "assets/za/Output"])
@pytest.mark.parametrize("output_dir", ["assets/za/Input", "assets/za/Output"])
def test_ui_initialization(
    running_locally: bool,
    input_dir: str,
    output_dir: str,
    za_trainer_data_dummy_parsed: list[ZATrainerData],
) -> None:
    """Test UI initialization."""
    if not running_locally:
        pytest.skip("Skipping manual visual test.")

    with (
        mock.patch.object(ZATrainerEditor, "create_widgets") as create_widgets,
        mock.patch.object(
            ZATrainerEditor,
            "load_trainer_data",
            return_value=za_trainer_data_dummy_parsed,
        ) as load_trainer_data,
        mock.patch.object(
            ZATrainerEditor, "display_trainer_data"
        ) as display_trainer_data,
    ):
        ui = ZATrainerEditor(
            visible=False,
            input_dir=input_dir,
            output_dir=output_dir,
        )
        create_widgets.assert_called_once()
        display_trainer_data.assert_called_once()
        load_trainer_data.assert_called_once()
    pydantic.TypeAdapter(list[ZATrainerData]).validate_python(ui.trdata)
    assert ui.selected_trainer_index == 0
    assert ui.input_dir == input_dir
    assert ui.output_dir == output_dir


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
