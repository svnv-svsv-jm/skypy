import pytest
from loguru import logger

from skypy.ops import read_devid


def test_dev_id() -> None:
    """Test DEV_ID constant."""
    dev_id = read_devid()
    logger.info(dev_id.head())


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
