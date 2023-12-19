__all__ = ["SinnohEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class SinnohEditor(PersonalEditor):
    """Sinnoh."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Empoleon
        pokemon = "Empoleon"
        df = set_pokemon(
            df,
            pokemon,
            ability="Competitive",
            stats={
                "base_stats.HP": 94,
                "base_stats.ATK": 70,
                "base_stats.DEF": 88,
                "base_stats.SPA": 116,
                "base_stats.SPD": 107,
                "base_stats.SPE": 60,
            },
        )
        df = add_move(df, pokemon, {"level": 40, "move": "freeze-dry"})
        df = add_move(df, pokemon, {"level": 38, "move": "air slash"})
        # Luxray
        pokemon = "Luxray"
        df = set_pokemon(
            df,
            pokemon,
            types=("electric", "dark"),
            ability="Intimidate",
            stats={
                "base_stats.HP": 80,
                "base_stats.ATK": 120,
                "base_stats.DEF": 79,
                "base_stats.SPA": 70,
                "base_stats.SPD": 79,
                "base_stats.SPE": 95,
            },
        )
        df = add_move(df, pokemon, {"level": 38, "move": "crunch"})
        df = add_move(df, pokemon, {"level": 38, "move": "thunder fang"})
        df = add_move(df, pokemon, {"level": 38, "move": "ice fang"})
        df = add_move(df, pokemon, {"level": 38, "move": "fire fang"})
        df = add_move(df, pokemon, {"level": 38, "move": "iron tail"})
        # Darkrai
        df = set_pokemon(
            df,
            "Darkrai",
            types=("dark", "ghost"),
            stats={
                "base_stats.HP": 92,
                "base_stats.ATK": 50,
                "base_stats.DEF": 78,
                "base_stats.SPA": 143,
                "base_stats.SPD": 95,
                "base_stats.SPE": 142,
            },
        )
        df = add_move(df, "Darkrai", {"level": 22, "move": "shadow ball"})
        df = add_move(df, "Darkrai", {"level": 40, "move": "psyshock"})
        df = add_move(df, "Darkrai", {"level": 44, "move": "mystical fire"})
        return df
