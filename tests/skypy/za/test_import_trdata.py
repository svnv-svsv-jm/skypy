import pydantic
import pytest
from loguru import logger

from skypy.schemas import ZATrainerData


def test_parsing_trainer_data(za_trainer_data_raw: dict) -> None:
    """Test `ZATrainerData` class can parse original trainer data."""
    logger.info(f"({type(za_trainer_data_raw)}): ")
    trdata = za_trainer_data_raw["values"]
    pydantic.TypeAdapter(list[ZATrainerData]).validate_python(trdata)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
