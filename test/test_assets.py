import pytest
import sys
import typing as ty
from loguru import logger

import pandas as pd

from skypy.const import DEV_ID
from skypy.ops import read_devid


def test_dev_id() -> None:
    """Test DEV_ID constant."""
    logger.info(DEV_ID)
    dev_id = read_devid()
    logger.info(dev_id.head())


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    pytest.main([__file__, "-x", "-s"])
