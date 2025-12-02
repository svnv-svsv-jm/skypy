from unittest.mock import patch

import pytest
from click.testing import CliRunner

from skypy.__main__ import app
from skypy.za import ZATrainerEditor


def test_main(cli_runner: CliRunner) -> None:
    """Test the main function."""
    with (
        patch.object(ZATrainerEditor, "__init__", return_value=None) as init,
        patch.object(ZATrainerEditor, "mainloop", return_value=None) as mainloop,
    ):
        result = cli_runner.invoke(app)  # type: ignore
        assert result.exit_code == 0, result.output
        init.assert_called_once()
        mainloop.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
