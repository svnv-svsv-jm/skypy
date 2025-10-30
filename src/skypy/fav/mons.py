from typing import Any

import pandas as pd

from skypy.fav.personal import PersonalEditor
from skypy.ops import read_data


def mons(df: pd.DataFrame | None = None, **kwargs: Any) -> pd.DataFrame:
    """Mons."""
    # Table
    if df is None:
        df = read_data(**kwargs)
    # Run
    editor = PersonalEditor(df)
    df = editor.run()
    # Exit
    return df
