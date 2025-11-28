import os

import pytest

from skypy.schemas import ZATrainerDataArray
from skypy.za import create_trdata_mod


def test_trainer_data_editor(zatrdata: ZATrainerDataArray, artifacts_path: str) -> None:
    """Test we can edit the trainer data."""
    create_trdata_mod(
        zatrdata,
        path=os.path.join(artifacts_path, "trdata_array.json"),
    )


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
