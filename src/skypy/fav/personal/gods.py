__all__ = ["GodsEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from .base import PersonalEditor


class GodsEditor(PersonalEditor):
    """Choose who becomes a God."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Dialga
        for pokemon in POKEMON:
            if "dialga" in pokemon.lower():
                df = set_pokemon(
                    df,
                    pokemon,
                    ability="Filter",
                    stats={
                        "base_stats.HP": 200,
                        "base_stats.ATK": 90,
                        "base_stats.DEF": 130,
                        "base_stats.SPA": 150,
                        "base_stats.SPD": 120,
                        "base_stats.SPE": 90,
                    },
                )
        # Palkia
        for pokemon in POKEMON:
            if "palkia" in pokemon.lower():
                df = set_pokemon(
                    df,
                    pokemon,
                    ability="Filter",
                    stats={
                        "base_stats.HP": 190,
                        "base_stats.ATK": 90,
                        "base_stats.DEF": 100,
                        "base_stats.SPA": 150,
                        "base_stats.SPD": 130,
                        "base_stats.SPE": 120,
                    },
                )
        # Giratina
        df = set_pokemon(
            df,
            "Giratina",
            ability="Filter",
            stats={
                "base_stats.HP": 250,
                "base_stats.ATK": 100,
                "base_stats.DEF": 120,
                "base_stats.SPA": 100,
                "base_stats.SPD": 120,
                "base_stats.SPE": 90,
            },
        )
        df = set_pokemon(
            df,
            "Origin Giratina",
            stats={
                "base_stats.HP": 250,
                "base_stats.ATK": 120,
                "base_stats.DEF": 100,
                "base_stats.SPA": 120,
                "base_stats.SPD": 100,
                "base_stats.SPE": 90,
            },
        )
        # Arceus
        for pokemon in POKEMON:
            if "arceus" in pokemon.lower():
                df = set_pokemon(
                    df,
                    pokemon,
                    stats={
                        "base_stats.HP": 220,
                        "base_stats.ATK": 220,
                        "base_stats.DEF": 220,
                        "base_stats.SPA": 220,
                        "base_stats.SPD": 220,
                        "base_stats.SPE": 220,
                    },
                )

        return df
