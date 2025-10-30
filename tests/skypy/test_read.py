import pytest
import sys
import typing as ty
from loguru import logger

from skypy.const import POKEMON, MOVES
from skypy.ops import read_data, read_waza
from skypy.ops.getters import resume_waza, resume_pokemon


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
