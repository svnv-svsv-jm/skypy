from typing import Any
import pandas as pd

from skypy.ops import read_trainer
from skypy.const.pkmn import POKEMON


def trainer(
    df: pd.DataFrame = None,
    lvl_multiplier: float = 1.1,
    compass: bool = True,
    **kwargs: Any,
) -> pd.DataFrame:
    """."""
    if df is None:
        df = read_trainer(**kwargs)
    # Copy from Compass 2.0.0
    if compass:
        df_compass = read_trainer(filename="trdata_array_compass.json", anew=True)
        for i in range(df_compass.shape[0]):
            trainer_data = df_compass.loc[i, :]
            trid = trainer_data["trid"]
            loc = df["trid"] == trid
            if loc.sum() > 0:
                df.loc[loc, df_compass.columns] = trainer_data
    # Level multiplier
    if lvl_multiplier is not None:
        for i in range(df.shape[0]):
            for l in range(6):
                c = f"poke{l+1}.level"
                lvl = df.loc[i, c]
                if isinstance(lvl, int):
                    new_level = int(lvl * lvl_multiplier)
                    df.loc[i, c] = min(100, new_level)
    # Exit
    return df
