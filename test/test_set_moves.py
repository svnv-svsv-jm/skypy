import pytest, sys, os, typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import (
    read_data,
    get_learnset,
    get_learnset_raw,
    add_move,
    add_move_raw,
    resume_pokemon,
)
from skypy.ops.setters import _check_moves_are_there
from skypy.ops.getters import LVLUP_MOVE_TYPE


@pytest.mark.parametrize(
    "pokemon, move_to_add",
    [
        ("squirtle", {"level": 7, "move": "quick attack"}),
        ("Nidoran♀", [{"level": 7, "move": "quick attack"}]),
        ("arceus", {"level": 7, "move": "quick attack"}),
    ],
)
def test_set_moves(
    pokemon: str,
    move_to_add: ty.Union[LVLUP_MOVE_TYPE, ty.Sequence[LVLUP_MOVE_TYPE]],
) -> None:
    """Test we can set a pokemon's moves."""
    # Get database
    df = read_data()
    logger.info(resume_pokemon(df, pokemon))
    # Show moves
    learnset = get_learnset(df, pokemon, readable=True)
    logger.info(f"\n{pokemon}:\n{learnset}")
    # Add move raw
    logger.info(f"Adding {move_to_add}")
    learnset_raw = add_move_raw(df, pokemon, move_to_add, readable=True)
    if isinstance(move_to_add, dict):
        move_to_add = [move_to_add]
    _check_moves_are_there(move_to_add, learnset_raw)
    # Add move
    logger.info(f"Adding {move_to_add}")
    df = add_move(df, pokemon, move_to_add)
    # Show moves
    learnset_new = get_learnset(df, pokemon, readable=True)
    logger.info(f"\n{pokemon} (new):\n{learnset_new}")
    learnset_new_raw = get_learnset_raw(df, pokemon, readable=True)
    _check_moves_are_there(move_to_add, learnset_new_raw)


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    pytest.main([__file__, "-x", "-s"])
