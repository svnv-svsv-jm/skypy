import pydantic
import pytest
from loguru import logger

from skypy.schemas import ZATrainerData
from skypy.za import ZATrainerEditor


def test_ui_load_trainer_data(za_trainer_editor_app: ZATrainerEditor) -> None:
    """Test UI load trainer data."""
    logger.info(f"({type(za_trainer_editor_app)}): {za_trainer_editor_app}")
    trdata = za_trainer_editor_app.load_trainer_data()
    pydantic.TypeAdapter(list[ZATrainerData]).validate_python(trdata)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
