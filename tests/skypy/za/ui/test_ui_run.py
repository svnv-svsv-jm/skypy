import pytest

from skypy.za import ZATrainerEditor


def test_running_ui_locally(running_locally: bool) -> None:
    """Test layout - manual visual test."""
    if not running_locally:
        pytest.skip("Skipping manual visual test.")
    ui = ZATrainerEditor()
    ui.mainloop()


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
