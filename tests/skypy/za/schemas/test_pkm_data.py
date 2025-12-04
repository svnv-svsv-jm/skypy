import typing as ty

import pytest
from loguru import logger

from skypy import settings
from skypy.schemas import ZAPokemonData
from skypy.types import ZABallID


def test_pokemon_data_from_str() -> None:
    """Test `ZAPokemonData` class can parse original trainer data from string representation, not only from the `int` version."""
    data = ZAPokemonData(dev_id="DEV_PIKATYUU")  # type: ignore
    assert data.dev_id == 25
    assert data.dev_id_english == "Pikachu"


@pytest.mark.parametrize("dev_id", [25])
def test_pokemon_data_to_eng_pikachu(
    za_debug_pkmn_data: dict,
    dev_id: int,
) -> None:
    """Test `ZATrainerData` class can parse original trainer data."""
    logger.info(za_debug_pkmn_data)
    data = ZAPokemonData(**za_debug_pkmn_data)
    data.dev_id = dev_id
    assert data.dev_id_english == "Pikachu"


@pytest.mark.parametrize("dev_id", range(1, 100))
def test_pokemon_data_to_eng(za_debug_pkmn_data: dict, dev_id: int) -> None:
    """Test `ZATrainerData` class can parse original trainer data."""
    data = ZAPokemonData(**za_debug_pkmn_data)
    data.dev_id = dev_id
    assert data.dev_id_english == settings.za_species_table[dev_id]


@pytest.mark.parametrize("ball_id", ty.get_args(ZABallID))
def test_pokemon_data_poke_ball_to_eng(
    za_debug_pkmn_data: dict,
    ball_id: ZABallID,
) -> None:
    """Test `ZATrainerData` class can parse original trainer data."""
    data = ZAPokemonData(**za_debug_pkmn_data)
    data.ball_id = ball_id
    assert data.ball_id_english == settings.za_items_table[ball_id]


@pytest.mark.parametrize("waza_id", range(1, 25))
@pytest.mark.parametrize("waza_nr", [1, 2, 3, 4])
def test_pokemon_waza_to_eng(
    za_debug_pkmn_data: dict,
    waza_id: int,
    waza_nr: int,
) -> None:
    """Test `ZATrainerData` class can parse original trainer data."""
    data = ZAPokemonData(**za_debug_pkmn_data)
    waza = getattr(data, f"waza_{waza_nr}")
    waza.waza_id = waza_id
    assert waza.waza_id_english == settings.za_waza_table[waza_id]


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
