import pytest
import sys
import os
import typing as ty
from loguru import logger

from skypy.ops import read_waza
from skypy.ops.getters import resume_waza
from skypy.ops.setters import set_waza


@pytest.mark.parametrize(
    "waza, accuracy",
    [
        ("surf", 5),
        ("scald", 100),
        ("Thunderclap", 101),
    ],
)
def test_set_waza_acc(
    waza: str,
    accuracy: int,
) -> None:
    """Test we can set a pokemon's ability."""
    # Get database
    df = read_waza()
    logger.info(resume_waza(df, waza))
    # Change waza
    df = set_waza(df, waza, accuracy=accuracy)
    r = resume_waza(df, waza)
    acc = r["accuracy"].values[0]
    logger.info(f"accuracy={acc}")
    assert acc == accuracy


@pytest.mark.parametrize(
    "waza, waza_type",
    [
        ("surf", "fire"),
        ("scald", "electric"),
        ("Thunderclap", "normal"),
    ],
)
def test_set_waza_type(
    waza: str,
    waza_type: str,
) -> None:
    """Test we can set a pokemon's ability."""
    # Get database
    df = read_waza()
    logger.info(resume_waza(df, waza))
    # Change waza
    df = set_waza(df, waza, waza_type)
    r = resume_waza(df, waza)
    logger.info(r["type"])
    assert r["type"].values[0].lower() == waza_type.lower()


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    pytest.main([__file__, "-x", "-s"])
