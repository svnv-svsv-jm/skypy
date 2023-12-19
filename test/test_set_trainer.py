import pytest, sys, os, typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import read_trainer, read_devid


@pytest.mark.parametrize(
    "waza, accuracy",
    [
        ("surf", 5),
    ],
)
def test_set_trainer(
    waza: str,
    accuracy: int,
) -> None:
    """Test we can set a pokemon's ability."""
    # Get database
    df = read_trainer()
    logger.info(df)
    devid = read_devid()
    # Change waza


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    pytest.main([__file__, "-x", "-s"])
