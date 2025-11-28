import pytest

from skypy.za import ZATrainerEditor


@pytest.mark.parametrize("output_dir", [None, "pytest_artifacts/za/Output"])
def test_ui_save(
    za_trainer_editor_app: ZATrainerEditor,
    output_dir: str,
) -> None:
    """Test `save_trainer_data`."""
    za_trainer_editor_app.save_trainer_data(output_dir=output_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
