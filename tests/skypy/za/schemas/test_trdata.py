import pydantic
import pytest
from loguru import logger

from skypy.schemas import ZATrainerData


def test_trainer_data(za_trainers: list[dict]) -> None:
    """Test `ZATrainerData` class can parse original trainer data."""
    logger.info(f"({type(za_trainers[0])}): {za_trainers[0]}")
    data = ZATrainerData(**za_trainers[0])
    logger.info(data)


def test_trainer_data_all(za_trainers: list[dict]) -> None:
    """Test `ZATrainerData` class can parse original trainer data."""
    pydantic.TypeAdapter(list[ZATrainerData]).validate_python(za_trainers)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
