__all__ = ["GalarEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class GalarEditor(PersonalEditor):
    """Galar."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Inteleon
        df = set_pokemon(
            df,
            "Inteleon",
            types=("water", "ghost"),
            ability=("sniper", "sniper", "sniper"),
            stats={
                "base_stats.HP": 70,
                "base_stats.ATK": 85,
                "base_stats.DEF": 65,
                "base_stats.SPA": 125,
                "base_stats.SPD": 65,
                "base_stats.SPE": 120,
            },
        )
        df = add_move(df, "Inteleon", {"level": 36, "move": "shadow ball"})
        # Urshifu
        df = add_evo(df, "Kubfu", level=42, into="Urshifu")
        df = add_move(df, "Urshifu", {"level": 1, "move": "wicked blow"})
        df = add_move(df, "Urshifu", {"level": 1, "move": "iron head"})
        df = add_move(df, "Urshifu", {"level": 1, "move": "drain punch"})
        df = add_move(df, "Urshifu", {"level": 1, "move": "bulk up"})
        return df
