import pytest
from loguru import logger

from skypy.schemas import ZAPokemonData


def test_pokemon_data(za_pokemon_data_raw: list[dict]) -> None:
    """Test `ZATrainerData` class can parse original trainer data."""
    data = ZAPokemonData(**za_pokemon_data_raw[0])
    logger.info(data)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
