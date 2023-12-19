__all__ = ["KalosEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class KalosEditor(PersonalEditor):
    """Kalos."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Goodra
        df = add_evo(df, "Goomy", level=25, into="Hisuian Sliggoo")
        pokemon = "Goodra"
        df = set_pokemon(
            df,
            pokemon,
            ability=["Sap Sipper", "Hydration", "Gooey"],
            stats={
                "base_stats.HP": 90,
                "base_stats.ATK": 70,
                "base_stats.DEF": 100,
                "base_stats.SPA": 110,
                "base_stats.SPD": 150,
                "base_stats.SPE": 80,
            },
        )
        df = add_move(df, pokemon, {"level": 36, "move": "sludge bomb"})
        df = add_move(df, pokemon, {"level": 33, "move": "ice beam"})
        df = add_move(df, pokemon, {"level": 33, "move": "water pulse"})
        return df
