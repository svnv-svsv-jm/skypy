import os
from unittest.mock import MagicMock, patch

import customtkinter as ctk
import pytest

from skypy import settings
from skypy.schemas import ZATrainerDataArray
from skypy.za import ZATrainerEditor


@pytest.mark.parametrize("output_dir", [None, "pytest_artifacts/za/Output"])
def test_ui_save(
    za_trainer_editor_app: ZATrainerEditor,
    output_dir: str | None,
) -> None:
    """Test `save_trainer_data`."""
    app = za_trainer_editor_app
    status_label = MagicMock(spec=ctk.CTkLabel)
    configure = MagicMock()
    status_label.configure = configure
    with (
        patch.object(ZATrainerDataArray, "dump") as dump,
        patch.object(app, "status_label", status_label, create=True),
    ):
        app.trdata.values[0].tr_id = "test_trainer"
        assert app.trdata.values[0].tr_id == "test_trainer"
        app.save_trainer_data(output_dir=output_dir)
        dump.assert_called_once()
        if output_dir is None:
            expected_output_dir = app.output_dir
        else:
            expected_output_dir = output_dir
        dump.assert_called_once_with(
            os.path.join(expected_output_dir, app.file_name),
            bfbs_file=settings.files.za_trainers_bfbs_file,
            create_binaries=True,
        )
        configure.assert_called()


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
