import pytest, sys
from typing import Union, Sequence, Dict
from loguru import logger

from skypy.const.pkmn import POKEMON
from skypy.const.waza import MOVES
from skypy.ops import get_pokemon, read_data, add_evo, get_evo_data


@pytest.mark.parametrize(
    "pokemon, level, into",
    [
        ("dewott", 32, "hisuian samurott"),
    ],
)
def test_edit_evo(pokemon: str, level: int, into: str) -> None:
    """Resume Pokemon."""
    # Get pokemon
    df = read_data()
    evo_data = get_evo_data(df, pokemon)
    logger.info(evo_data)
    df = add_evo(df, pokemon, level=level, into=into)
    evo_data = get_evo_data(df, pokemon)
    logger.info(evo_data)


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    pytest.main([__file__, "-x", "-s"])
