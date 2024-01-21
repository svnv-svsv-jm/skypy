__all__ = ["AlolaEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops.setters import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class AlolaEditor(PersonalEditor):
    """Alola."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Decidueye
        pokemon = "Decidueye"
        df = set_pokemon(
            df,
            pokemon,
            ability="Long Reach",
            stats={
                "base_stats.HP": 78,
                "base_stats.ATK": 117,
                "base_stats.DEF": 80,
                "base_stats.SPA": 55,
                "base_stats.SPD": 80,
                "base_stats.SPE": 120,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "bulk up"})
        df = add_move(df, pokemon, {"level": 1, "move": "jungle healing"})
        df = add_move(df, pokemon, {"level": 1, "move": "triple arrows"})
        # Lycanroc-1
        pokemon = "Lycanroc-1"
        df = set_pokemon(
            df,
            pokemon,
            types=("rock", "ghost"),
            ability=["no guard", "no guard", "defiant"],
            stats={
                "base_stats.HP": 85,
                "base_stats.ATK": 115,
                "base_stats.DEF": 75,
                "base_stats.SPA": 55,
                "base_stats.SPD": 75,
                "base_stats.SPE": 82,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "accelerock"})
        df = add_move(df, pokemon, {"level": 1, "move": "shadow claw"})
        df = add_move(df, pokemon, {"level": 1, "move": "drain punch"})
        df = add_move(df, pokemon, {"level": 1, "move": "bulk up"})
        return df
