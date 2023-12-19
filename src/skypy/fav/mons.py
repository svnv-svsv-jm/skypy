from typing import Any, List
from loguru import logger

import pandas as pd

from skypy.ops import add_move, read_data, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal import PersonalEditor


def mons(df: pd.DataFrame = None, **kwargs: Any) -> pd.DataFrame:
    """Mons."""
    # Table
    if df is None:
        df = read_data(**kwargs)
    # Run
    editor = PersonalEditor(df)
    df = editor.run()
    # Exit
    return df
