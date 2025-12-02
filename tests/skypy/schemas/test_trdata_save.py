import json
import os
import pprint as pp
import subprocess
import tempfile
from unittest.mock import patch

import pytest
from loguru import logger

from skypy import settings
from skypy.schemas import ZATrainerDataArray


def test_trdata_save(
    artifacts_path: str,
    za_trainers: list[dict],
) -> None:
    """Test `ZATrainerDataArray` class can save data.

    Create a temporary file, make sure it is empty, dump the data to it, and make sure the file is not empty.
    Also make sure the data is dumped correctly.
    This way, we also check that the file can be overwritten.
    """
    # Create the data
    trainers = {"values": za_trainers[:3]}
    zatrdata = ZATrainerDataArray(**trainers)  # type: ignore
    logger.info(f"({type(zatrdata)}):\n{pp.pformat(zatrdata)}")

    raw = zatrdata.model_dump(mode="json", by_alias=True, exclude_unset=True)
    logger.info(f"({type(raw)}):\n{pp.pformat(raw)}")
    assert raw == trainers, f"`model_dump()` failed. Expected {trainers} but got {raw}"

    with tempfile.NamedTemporaryFile(dir=artifacts_path, suffix=".json") as f:
        # Make sure the file is empty
        assert os.path.exists(f.name)
        with pytest.raises(json.JSONDecodeError):
            json.load(open(f.name))

        logger.info(f"Temporary file: {f.name}")
        # Dump the data
        with patch.object(subprocess, "run") as run:
            zatrdata.dump(f.name, create_binaries=True)
            run.assert_called_once_with(
                [
                    "flatc",
                    "-b",
                    "-o",
                    artifacts_path,
                    settings.files.za_trainers_bfbs_file,
                    f.name,
                ]
            )

        # Tests
        assert os.path.exists(f.name)
        dumped_data = json.load(open(f.name))
        assert dumped_data == trainers, f"Expected {trainers} but got {dumped_data}"


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s", "-vv"])
