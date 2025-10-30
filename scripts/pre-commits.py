# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "pyrootutils",
#   "pyyaml",
#   "toml",
#   "typer",
#   "loguru",
# ]
# ///
import glob
import os
import subprocess
import sys

import pyrootutils
import typer
from loguru import logger

app = typer.Typer()

pyrootutils.setup_root(".", cwd=True)


def find_libs(directory: str) -> list[str]:
    """Find all main package directories under `libs/**/src/`.

    Same as: `find libs -type d -path "libs/*/src/*" -not -path "*/ __pycache__/*" -prune -o -type d -path "libs/*/src/*" | while read -r dir; do basename "$dir"; done | sort -u | xargs ...`
    """
    lib_dirs: set[str] = set()
    for root, dirs, _ in os.walk(directory):
        # Exclude __pycache__ dirs
        dirs[:] = [d for d in dirs if d != "__pycache__"]

        # Check if this directory is directly under libs/*/src/
        # The path should be: libs/some_lib/src/some_package (exactly 4 parts)
        parts = root.split(os.sep)
        if len(parts) == 4 and parts[-2] == "src":
            # The library name is the last part (i.e., the main package directory under src/)
            lib_dirs.add(os.path.basename(root))

    libs = sorted(lib_dirs)
    logger.info(f"Found {len(libs)} libraries in `{directory}/` directory: {libs}")
    return libs


@app.command()
def test_build(
    libs: list[str] | None = typer.Argument(None, help="List of library names to test."),
    python: str = typer.Option(sys.executable, help="Python interpreter to use."),
    dist_dir: str = typer.Option("dist", help="Directory to look for wheel files."),
    libs_dir: str = typer.Option("libs", help="Directory to look for library names."),
) -> None:
    """Checks that the packages in the dist directory are importable."""
    if libs is None:
        libs = find_libs(libs_dir)

    wheel_files = list(glob.glob(f"{dist_dir}/*.whl"))

    if not wheel_files:
        logger.warning(f"No wheel files found in `{dist_dir}/` directory")
        return

    subprocess.check_call(["uv", "pip", "install", "--python", python] + wheel_files)

    for lib in libs:
        logger.info(f"Attempting to import: {lib}")
        __import__(lib)

    logger.success(f"All packages installed and importable: {libs}")




if __name__ == "__main__":
    app()
