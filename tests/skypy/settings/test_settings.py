import pytest
import sys
import typing as ty
from loguru import logger

import skypy


def test_settings() -> None:
    """Test `settings`."""
    logger.info(skypy.settings.files.data_devid)


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    pytest.main([__file__, "-x", "-s"])
