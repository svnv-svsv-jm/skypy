import pytest, sys, os, typing as ty
from loguru import logger

from skypy.fav.main import main
from skypy.fav.personal import PersonalEditor


def test_runner_main() -> None:
    """Test main script."""
    editor = PersonalEditor()
    klasses = editor.get_children()
    logger.info(klasses)


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
    pytest.main([__file__, "-x", "-s"])
