__all__ = ["UnovaEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class UnovaEditor(PersonalEditor):
    """Unova."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Zoroark
        pokemon = "Zoroark"
        df = set_pokemon(
            df,
            pokemon,
            stats={
                "base_stats.HP": 75,
                "base_stats.ATK": 60,
                "base_stats.DEF": 65,
                "base_stats.SPA": 130,
                "base_stats.SPD": 65,
                "base_stats.SPE": 115,
            },
        )
        # Bisharp
        df = add_evo(df, "Bisharp", level=50, into="Kingambit")
        # Hydreigon
        df = set_pokemon(df, "deino", ability="shed skin")
        df = add_evo(df, "deino", level=30, into="Zweilous")
        df = set_pokemon(df, "Zweilous", ability="shed skin")
        df = add_evo(df, "Zweilous", level=50, into="Hydreigon")
        df = set_pokemon(
            df,
            "Hydreigon",
            stats={
                "base_stats.HP": 92,
                "base_stats.ATK": 80,
                "base_stats.DEF": 90,
                "base_stats.SPA": 130,
                "base_stats.SPD": 90,
                "base_stats.SPE": 118,
            },
        )
        return df
