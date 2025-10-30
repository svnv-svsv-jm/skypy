__all__ = ["to_bin"]

import os
import shutil
import subprocess

from skypy.const.loc import BIN_FOLDER, FILENAME_WAZA, WAZA_SCHEMA


def to_bin(
    output_dir: str = BIN_FOLDER,
    waza_schema: str = WAZA_SCHEMA,
) -> None:
    """Creates the waza.bin file."""
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Command to execute
    command = [
        "flatc",
        "-b",
        waza_schema,
        os.path.join(output_dir, FILENAME_WAZA),
    ]

    # Run the command
    subprocess.run(command, check=False)

    # Example: Copy the generated binary file to another directory
    output_binary_path = os.path.join(output_dir, "personal_array.bin")
    shutil.copy(os.path.join(output_dir, "personal_array.json"), output_binary_path)

    print(f"Binary file copied to {output_binary_path}")
