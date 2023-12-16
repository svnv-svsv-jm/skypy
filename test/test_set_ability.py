import pytest, sys, os, typing as ty
from loguru import logger

from skypy.ops import get_ability, set_pokemon, read_data, resume_pokemon


@pytest.mark.parametrize(
    "pokemon, ability_to_give",
    [
        ("deino", "Tera Shift"),
        ("squirtle", "Wonder Guard"),
        ("terapagos", "guts"),
    ],
)
def test_set_ability(
    pokemon: str,
    ability_to_give: str,
) -> None:
    """Test we can set a pokemon's ability."""
    # Get database
    df = read_data()
    # Print current abilities
    logger.info(resume_pokemon(df, pokemon))
    # Change them
    df = set_pokemon(df, pokemon, ability=ability_to_give)
    # Test change happened
    abilities = get_ability(df, pokemon)
    logger.info(abilities)
    for a in abilities:
        assert a.lower() == ability_to_give.lower()


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    pytest.main([__file__, "-x", "-s"])
