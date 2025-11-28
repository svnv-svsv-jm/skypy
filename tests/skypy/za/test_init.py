import pytest
from loguru import logger


def test_za_init() -> None:
    """Test that `za` module can be imported."""
    import za

    logger.info(za)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
