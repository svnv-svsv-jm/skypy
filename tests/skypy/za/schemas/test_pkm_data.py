import typing as ty

import pytest
from loguru import logger

from skypy import settings
from skypy.schemas import ZAPokemonData
from skypy.schemas.za import get_key_by_value
from skypy.types import ZABallID


def test_pokemon_data_null_dump() -> None:
    """Test we can dump a `ZAPokemonData` object to the string representation when it is null."""
    empty_pkmn = {
        "ballId": "MONSUTAABOORU",
        "waza1": {},
        "waza2": {},
        "waza3": {},
        "waza4": {},
        "seikaku": "GANBARIYA",
        "talentValue": {},
        "effortValue": {},
        "rareType": "NO_RARE",
        "scaleValue": 128,
    }
    data = ZAPokemonData(**empty_pkmn)
    raw = data.model_dump(mode="json", by_alias=True, exclude_unset=True)
    assert raw == empty_pkmn


def test_pokemon_data_to_str() -> None:
    """Test we can dump a `ZAPokemonData` object to the string representation."""
    data = ZAPokemonData(
        dev_id=25,
        sex=0,
        item=0,
        ball_id=4,
        seikaku=1,
        tokusei=0,
        rare_type=1,
    )
    raw = data.model_dump(mode="json")
    assert raw["dev_id"] == get_key_by_value(settings.za_species_mappings, data.dev_id)
    assert raw["sex"] == get_key_by_value(settings.za_sex_mappings, data.sex)
    assert raw["item"] == get_key_by_value(settings.za_item_mappings, data.item)
    assert raw["ball_id"] == get_key_by_value(settings.za_ball_mappings, data.ball_id)
    assert raw["seikaku"] == get_key_by_value(
        settings.za_seikaku_mappings, data.seikaku
    )
    assert raw["tokusei"] == get_key_by_value(
        settings.za_tokusei_mappings, data.tokusei
    )
    assert raw["rare_type"] == get_key_by_value(
        settings.za_rare_type_mappings, data.rare_type
    )


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
    pytest.main([__file__, "-x", "-s", "-vv"])
