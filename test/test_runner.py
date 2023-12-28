import pytest, sys, os, typing as ty
from loguru import logger

from skypy.fav.main import main


def test_runner_main() -> None:
    """Test main script."""
    main()


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
    pytest.main([__file__, "-x", "-s"])
