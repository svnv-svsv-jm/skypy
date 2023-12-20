# pylint: disable=unused-import
# pylint: disable=unused-argument
__all__ = ["nb_init"]

import typing as ty
import os, sys
from loguru import logger
import warnings
import pyrootutils
import pandas as pd

from skypy.const import ABILITIES, POKEMON, TYPES, MOVES


def nb_init(logger_level: str = "INFO", add_std: bool = False) -> None:
    """Disables warnings and correctly finds the root directory of the project. Very handy when running notebooks.
    Args:
        logger_level (str): 'INFO'
            Logging level for loguru's logger.
    """
    warnings.filterwarnings("ignore")
    root = pyrootutils.setup_root(
        search_from=".",
        indicator=[".git", "pyproject.toml"],
        pythonpath=True,
        dotenv=True,
        cwd=True,
    )
    os.chdir(root)
    logger.remove()
    logger.add(sys.stderr, level=logger_level, format="{level} | {function} | {message}")
    logger.info(f"Set current dir to {os.path.basename(root)}")
    logger.info(f"You are using Python {sys.version}")
    logger.debug("You will see DEBUG messages.")


def pretty_waza(waza: pd.DataFrame) -> pd.DataFrame:
    """Create a pretty version of the waza table, to show in Data Viewer."""
    waza_pretty = waza
    waza_pretty["move_id"] = pd.Series(MOVES)
    waza_pretty["type"] = waza["type"].apply(lambda x: TYPES[x]).astype("string")
    return waza_pretty


def pretty_df(df: pd.DataFrame) -> pd.DataFrame:
    """Create a pretty version of the Pkm table, to show in Data Viewer."""
    df_pretty = df.copy()
    df_pretty["type_1"] = df["type_1"].apply(lambda x: TYPES[x]).astype("string")
    df_pretty["type_2"] = df["type_2"].apply(lambda x: TYPES[x]).astype("string")
    df_pretty["ability_1"] = df["ability_1"].apply(lambda x: ABILITIES[x]).astype("string")
    df_pretty["ability_2"] = df["ability_2"].apply(lambda x: ABILITIES[x]).astype("string")
    df_pretty["ability_hidden"] = df["ability_hidden"].apply(lambda x: ABILITIES[x]).astype("string")
    df_pretty["name"] = df.reset_index()["index"].apply(lambda x: POKEMON[x]).astype("string")
    # Add Base STAT TOTAL
    cols = [c for c in df.columns if "base_stats." in c.lower()]
    tot = 0
    for c in cols:
        tot += df[c].to_numpy()  # type: ignore
    df_pretty["BST"] = tot
    # Reorder
    df_pretty = select_fist_columns(
        df_pretty,
        ["name", "type_1", "type_2", "ability_1", "ability_2", "ability_hidden", "BST"] + cols,
    )
    df_pretty = df_pretty.loc[df["is_present"], :]
    df_pretty = df_pretty.drop(columns=["is_present"])
    return df_pretty


def select_fist_columns(df: pd.DataFrame, cols: ty.List[str]) -> pd.DataFrame:
    """Places first the provided columns."""
    for i, c in enumerate(cols):
        df = _reorder_columns(df, c, pos=i)
    return df


def _reorder_columns(df: pd.DataFrame, column_to_move: str, pos: int = 0) -> pd.DataFrame:
    """Reorder columns."""
    # Get the list of columns
    columns = list(df.columns)
    # Move the specified column to the second position
    columns.insert(pos, columns.pop(columns.index(column_to_move)))
    # Reorder the DataFrame columns
    df = df[columns]
    return df
