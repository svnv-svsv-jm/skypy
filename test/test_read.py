import pytest, sys
from typing import Union, Sequence, Dict
from loguru import logger

from skypy.const.pkmn import POKEMON
from skypy.const.waza import MOVES
from skypy.ops import resume_pokemon, read_data, read_waza, resume_waza


def test_read() -> None:
    """Resume Pokemon."""
    # Get pokemon
    df = read_data(anew=True)
    logger.info(f"{df.shape}")
    assert df.shape[0] == len(POKEMON)
    data = resume_pokemon(df, name="Terapagos")
    logger.info(data)
    # Get waza
    df = read_waza()
    assert df.shape[0] == len(MOVES)
    waza = resume_waza(df, "surf")
    logger.info(waza)
    t = str(waza["type"].values[0]).lower()
    logger.info(t)
    assert t == "water"
    logger.info(waza["accuracy"])
    waza["accuracy"] = 25
    logger.info(waza["accuracy"])


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    pytest.main([__file__, "-x", "-s"])
