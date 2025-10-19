import pytest, sys, os, typing as ty
from loguru import logger

from skypy.ops import read_data
from skypy.ops.getters import get_type
from skypy.ops.setters import set_pokemon


@pytest.mark.parametrize(
    "pokemon, expected_types",
    [
        ("deino", ["Dark", "Dragon"]),
        ("squirtle", ["Water", "Water"]),
        ("Nidoran♀", ["Poison", "Poison"]),
    ],
)
def test_set_ability(
    pokemon: str,
    expected_types: ty.List[str],
) -> None:
    """Test we can set a pokemon's ability."""
    # Get database
    df = read_data()
    # Print current types
    types = get_type(df, pokemon)
    logger.info(f"Original types: {types}")
    for t, xt in zip(types, expected_types):
        assert t.lower() == xt.lower()
    # Change them
    types_to_give = ("ground", "fairy")
    df = set_pokemon(df, pokemon, types=types_to_give)
    # Test change happened
    types = get_type(df, pokemon)
    logger.info(f"New types: {types}")
    for t, xt in zip(types, types_to_give):
        assert t.lower() == xt.lower()


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    pytest.main([__file__, "-x", "-s"])
