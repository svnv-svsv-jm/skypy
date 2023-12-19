__all__ = ["PaldeaEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from .base import PersonalEditor


class PaldeaEditor(PersonalEditor):
    """Paldea."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Garganacl
        pokemon = "Garganacl"
        df = set_pokemon(
            df,
            pokemon,
            types=("Rock", "Rock"),
            ability="Purifying Salt",
            stats={
                "base_stats.HP": 100,
                "base_stats.ATK": 100,
                "base_stats.DEF": 130,
                "base_stats.SPA": 45,
                "base_stats.SPD": 90,
                "base_stats.SPE": 35,
            },
        )
        # Glimmora
        df = set_pokemon(
            df,
            "Glimmora",
            ability=("Toxic Debris", "Toxic Debris", "Corrosion"),
            stats={
                "base_stats.HP": 113,
                "base_stats.ATK": 55,
                "base_stats.DEF": 80,
                "base_stats.SPA": 130,
                "base_stats.SPD": 81,
                "base_stats.SPE": 96,
            },
        )
        df = add_move(df, pokemon, {"level": 40, "move": "iron defense"})
        df = add_move(df, pokemon, {"level": 42, "move": "calm mind"})
        df = add_move(df, pokemon, {"level": 43, "move": "aura sphere"})
        df = add_move(df, pokemon, {"level": 44, "move": "earth power"})
        df = add_move(df, pokemon, {"level": 45, "move": "sludge bomb"})
        return df
