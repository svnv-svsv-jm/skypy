import pprint as pp

import pydantic
import pytest
from loguru import logger

from skypy.schemas import ZATrainerData, ZATrainerDataArray


def test_trainer_data_array(za_trainers: list[dict]) -> None:
    """Test `ZATrainerDataArray` class can parse original trainer data."""
    zatrdata = ZATrainerDataArray(Table=za_trainers)  # type: ignore
    with pytest.raises(ValueError):
        zatrdata.get_trainer("xxx")


def test_trainer_data(za_debug_trainer_data: dict) -> None:
    """Test `ZATrainerData` class can parse original trainer data."""
    logger.info(f"{pp.pformat(za_debug_trainer_data)}")

    data = ZATrainerData(**za_debug_trainer_data)
    logger.info(f"({type(data)}):\n{pp.pformat(data)}")

    raw = data.model_dump(mode="json", by_alias=True, exclude_unset=True)
    logger.info(f"({type(raw)}):\n{pp.pformat(raw)}")

    assert raw == za_debug_trainer_data


def test_trainer_data_all(za_trainers: list[dict]) -> None:
    """Test `ZATrainerData` class can parse original trainer data."""
    pydantic.TypeAdapter(list[ZATrainerData]).validate_python(za_trainers)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
