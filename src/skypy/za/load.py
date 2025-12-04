__all__ = ["load_trainer_data"]

import json
import os

from loguru import logger

from skypy import settings
from skypy.schemas import ZATrainerDataArray


def load_trainer_data(
    file_name: str = settings.files.file_trainer_data,
    input_dir: str = os.path.dirname(settings.files.file_trainer_data),
    output_dir: str | None = None,
    ignore_output_dir: bool = False,
) -> ZATrainerDataArray:
    """Load trainer data from a JSON file."""
    logger.trace("Loading trainer data...")

    # If output folder exists, use it
    dir_path = input_dir
    logger.trace(f"Set target directory to {dir_path}")
    if (
        output_dir is not None
        and os.path.exists(os.path.join(output_dir, file_name))
        and not ignore_output_dir
    ):
        logger.trace(f"Output folder exists ({output_dir}), using it....")
        dir_path = output_dir
        logger.trace(f"Set new target directory to {dir_path}")

    # Load data
    logger.trace(f"Joining {dir_path} and {file_name}")
    path = os.path.join(dir_path, file_name)
    logger.info(f"Loading data from {path}...")
    with open(path, encoding="utf-8") as f:
        trdata: dict = json.load(f)
    assert isinstance(trdata, dict), f"Expected dict, got {type(trdata)}"
    trainers: ZATrainerDataArray = ZATrainerDataArray(**trdata)
    logger.trace(f"Loaded trainer data from {path}.")
    return trainers
