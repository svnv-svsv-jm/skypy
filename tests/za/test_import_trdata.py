import json

import pytest
from loguru import logger


def test_import_legends_za_trainer_data(
    za_trainer_data: str,
    za_trainer_data_complete: str,
) -> None:
    """Load Legends ZA trainer data JSON and assert it is non-empty."""
    # Prefer the complete trainer data dump if available
    candidates = [za_trainer_data_complete, za_trainer_data]
    data_file = next((p for p in candidates if p.exists()), None)

    assert data_file is not None, "No ZA trainer data JSON found in assets/za"
    logger.info(f"Loading ZA trainer data from {data_file}")

    with data_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data, "Loaded ZA trainer data is empty"
    assert isinstance(data, dict) or isinstance(
        data, list
    ), "Unexpected JSON structure for ZA trainer data"
    logger.info(
        "ZA trainer data loaded: type=%s",
        type(data).__name__,
    )


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
