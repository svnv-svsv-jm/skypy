__all__ = ["AlolaEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from .base import PersonalEditor


class AlolaEditor(PersonalEditor):
    """Alola."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Lycanroc-1
        df = set_pokemon(
            df,
            "Lycanroc-1",
            types=("rock", "ghost"),
            ability=("No Guard", "No Guard", "No Guard"),
            stats={
                "base_stats.HP": 85,
                "base_stats.ATK": 115,
                "base_stats.DEF": 75,
                "base_stats.SPA": 55,
                "base_stats.SPD": 75,
                "base_stats.SPE": 82,
            },
        )
        return df
