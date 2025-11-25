import pydantic
import pytest

from skypy.schemas import ZATrainerData
from skypy.za import ZATrainerEditor


def test_layout(running_locally: bool) -> None:
    """Test layout - manual visual test."""
    if not running_locally:
        pytest.skip("Skipping manual visual test.")
    ui = ZATrainerEditor()
    pydantic.TypeAdapter(list[ZATrainerData]).validate_python(ui.trdata)
    assert ui.selected_trainer_index == 0
    ui.mainloop()


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
