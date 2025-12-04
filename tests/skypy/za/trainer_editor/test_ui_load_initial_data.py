import os
import tempfile
from unittest import mock

import pytest

from skypy.schemas import ZATrainerDataArray
from skypy.za import ZATrainerEditor


def test_ui_load_initial_data(
    zatrdata: ZATrainerDataArray,
    artifacts_path: str,
) -> None:
    """Test behavior of how the UI loads the initial data.

    We check that it reads from the input folder, but that it reads from the output folder if it exists.
    """
    zatrdata_new = zatrdata.model_copy(deep=True)
    zatrdata_new.table[0].ai_basic = not zatrdata_new.table[0].ai_basic
    with (
        mock.patch.object(ZATrainerEditor, "create_widgets"),
        mock.patch.object(ZATrainerEditor, "create_trainer_data"),
    ):
        with (
            tempfile.TemporaryDirectory(
                dir=artifacts_path, prefix="input_"
            ) as temp_dir_input,
            tempfile.NamedTemporaryFile(
                dir=temp_dir_input, suffix=".json"
            ) as temp_file_input,
            tempfile.TemporaryDirectory(
                dir=artifacts_path, prefix="output_"
            ) as temp_dir_output,
            tempfile.NamedTemporaryFile(
                dir=temp_dir_output, suffix=".json"
            ) as temp_file_output,
        ):
            temp_file_input.write(
                zatrdata.model_dump_json(by_alias=True).encode("utf-8")
            )
            temp_file_output.write(
                zatrdata_new.model_dump_json(by_alias=True).encode("utf-8")
            )
            ui = ZATrainerEditor(
                visible=False,
                input_dir=temp_dir_input,
                output_dir=temp_dir_output,
                file_name=os.path.basename(temp_file_output.name),
            )
            assert ui.file_name == os.path.basename(temp_file_output.name)
            assert (
                ui.trdata.values[0].ai_basic != zatrdata.table[0].ai_basic
            ), "UI did not load initial data from Output folder."
            assert (
                ui.trdata.values[0].ai_basic == zatrdata_new.table[0].ai_basic
            ), "UI did not load initial data from Output folder."


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
