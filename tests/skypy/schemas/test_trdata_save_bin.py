import os

import pytest

from skypy.schemas import ZATrainerDataArray


def test_trdata_save_with_bfbs_file(
    artifacts_path: str,
    za_trainers: list[dict],
) -> None:
    """Test `ZATrainerDataArray.dump()`."""
    zatrdata = ZATrainerDataArray(values=za_trainers)  # type: ignore
    fname = os.path.join(artifacts_path, "trdata_array.json")
    zatrdata.dump(fname, create_binaries=True)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s", "-vv"])
