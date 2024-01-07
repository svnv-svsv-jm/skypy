__all__ = [
    "read_data",
    "read_trainer",
    "read_trainer_map",
    "read_waza",
    "read_devid",
    "display_trainer",
    "write_df_to_json",
    "df_to_formatted_json",
    "write_waza_to_json",
    "write_trainer_to_json",
    "write_personal_to_json",
]

from loguru import logger
from typing import Union, Sequence, Any, List, Dict, Tuple, Optional
import pandas as pd
import numpy as np
import json
import os
from pathlib import Path

from skypy.const.loc import (
    FILENAME,
    FILENAME_WAZA,
    FILENAME_DEVID,
    OUTPUT_FOLDER,
    INPUT_FOLDER,
    FILENAME_TR,
    FILENAME_TR_MAP,
)
from skypy.const.schema import INT_COLUMNS
from skypy.const.devid import DEV_ID


def display_trainer(df: pd.DataFrame) -> pd.DataFrame:
    """Trainer data."""
    devid = read_devid()
    tmp = df.copy()
    for i in range(6):
        c = f"poke{i+1}.devId"
        tmp[c] = tmp[c].apply(lambda x: devid.loc[devid["devName"] == x, "name"].values[0])
    return tmp


def read_devid(**kwargs: Any) -> pd.DataFrame:
    """Read waza data."""
    df = pd.json_normalize(DEV_ID, record_path="values")
    df = force_columns_to_int(df)
    df = df.fillna(np.nan)
    return df


def read_waza(**kwargs: Any) -> pd.DataFrame:
    """Read waza data."""
    kwargs.setdefault("filename", FILENAME_WAZA)
    kwargs.setdefault("record_path", "table")
    return read_data(**kwargs)


def read_personal(**kwargs: Any) -> pd.DataFrame:
    """Read personal data."""
    kwargs.setdefault("filename", FILENAME)
    kwargs.setdefault("record_path", "entry")
    return read_data(**kwargs)


def read_trainer_map(**kwargs: Any) -> pd.DataFrame:
    """Read mapping from Trainer ID's to readable names."""
    kwargs.setdefault("filename", FILENAME_TR_MAP)
    kwargs.setdefault("record_path", "trainers")
    return read_data(**kwargs)


def read_trainer(**kwargs: Any) -> pd.DataFrame:
    """Read personal data."""
    kwargs.setdefault("filename", FILENAME_TR)
    kwargs.setdefault("record_path", "values")
    return read_data(**kwargs)


def read_data(
    filename: str = FILENAME,
    *,
    record_path: str = "entry",
    loc: str = None,
    anew: bool = False,
    f: str = None,
) -> pd.DataFrame:
    """Read JSON data.

    Args:
        filename (str, optional):
            Name of the .json file. Defaults to 'personal_array.json'.
        record_path (str, optional): _description_. Defaults to "entry".
        loc (str, optional):
            Location of the `filename`. Defaults to None.

    Returns:
        pd.DataFrame: _description_
    """
    if f is None:
        if anew:
            loc = INPUT_FOLDER
        if loc is None:
            loc = OUTPUT_FOLDER
        if Path(loc).exists():
            f = os.path.join(loc, filename)
            if not Path(f).exists():
                loc = INPUT_FOLDER
        else:
            loc = INPUT_FOLDER
        logger.trace(f"loc={loc}")
        f = os.path.join(loc, filename)
    logger.trace(f"f={f}")
    with open(f) as json_file:
        data = json.load(json_file)
    df = pd.json_normalize(data, record_path=record_path)
    df = force_columns_to_int(df)
    df = df.fillna(np.nan)
    return df


def force_columns_to_int(df: pd.DataFrame) -> pd.DataFrame:
    """Force relevant columns to int."""
    for c in INT_COLUMNS:
        df = _to_int(df, c)
    return df


def _to_int(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Force column to int."""
    if col in df.columns:
        df[col] = df[col].astype("Int64")
    return df


def write_waza_to_json(
    df: pd.DataFrame,
    filename: str = FILENAME_WAZA,
    loc: str = OUTPUT_FOLDER,
    **kwargs: Any,
) -> None:
    """Write results to file."""
    kwargs.setdefault("keys_to_suspect", None)
    kwargs.setdefault("first_key", "table")
    write_df_to_json(df, filename, loc=loc, **kwargs)


def write_trainer_to_json(
    df: pd.DataFrame,
    filename: str = FILENAME_TR,
    loc: str = OUTPUT_FOLDER,
    **kwargs: Any,
) -> None:
    """Write results to file."""
    kwargs.setdefault("keys_to_suspect", None)
    kwargs.setdefault("first_key", "values")
    for c, t in zip(df.columns, df.dtypes):
        if t == "float64":
            df = _to_int(df, c)
    write_df_to_json(df, filename, loc=loc, **kwargs)


def write_personal_to_json(
    df: pd.DataFrame,
    filename: str = FILENAME,
    loc: str = OUTPUT_FOLDER,
    **kwargs: Any,
) -> None:
    """Write results to file."""
    kwargs.setdefault("keys_to_suspect", ["dex"])
    kwargs.setdefault("first_key", "entry")
    write_df_to_json(df, filename, loc=loc, **kwargs)


def write_df_to_json(
    df: pd.DataFrame,
    filename: str = FILENAME,
    loc: str = OUTPUT_FOLDER,
    **kwargs: Any,
) -> None:
    """Write results to file."""
    df = force_columns_to_int(df)
    data = df_to_formatted_json(df, **kwargs)
    Path(loc).mkdir(parents=True, exist_ok=True)
    outfile = os.path.join(loc, filename)
    with open(outfile, mode="w") as f:
        json.dump(data, f, indent=2, allow_nan=True)
    logger.info(f"Saved to {outfile}")


def df_to_formatted_json(
    df: pd.DataFrame,
    sep: str = ".",
    first_key: str = "entry",
    keys_to_suspect: Optional[List[str]] = ["dex"],
) -> Dict[str, Any]:
    """The opposite of `json_normalize`."""
    result = []
    for _, row in df.iterrows():
        parsed_row: Dict[str, Any] = {}
        for col_label, v in row.items():
            keys = col_label.split(sep)  # type: ignore
            current = parsed_row
            for i, k in enumerate(keys):
                if i == len(keys) - 1:
                    try:
                        if v == v:  # avoid nan's
                            current[k] = v
                    except:
                        pass
                else:
                    if k not in current:
                        current[k] = {}
                    current = current[k]
        if keys_to_suspect is not None:
            for sk in keys_to_suspect:
                t = parsed_row[sk]
                if isinstance(t, dict) and not t:
                    parsed_row.pop(sk, None)
        # save
        result.append(parsed_row)
    out = {first_key: result}
    return out
