import pytest
import sys
import os
import typing as ty
from loguru import logger

from skypy.schemas import EvoData


def test_evo_data() -> None:
    """Test we can covert this to a `dict`."""
    new_evo = EvoData(level=1, species=1)
    assert new_evo.level == 1
    assert new_evo.species == 1
    x = new_evo.to_dict()
    logger.info(x)
    assert isinstance(x, dict)
    x = dict(new_evo)
    logger.info(x)
    assert isinstance(x, dict)


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    pytest.main([__file__, "-x", "-s"])
