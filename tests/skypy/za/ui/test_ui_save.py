import pytest

from skypy.za import ZATrainerEditor


def test_ui_save(
    za_trainer_editor_app: ZATrainerEditor,
    artifacts_path: str,
) -> None:
    """Test `save_trainer_data`."""
    za_trainer_editor_app.save_trainer_data(output_dir=artifacts_path)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
