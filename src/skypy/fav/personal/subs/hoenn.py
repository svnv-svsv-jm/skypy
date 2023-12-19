__all__ = ["HoennEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class HoennEditor(PersonalEditor):
    """Hoenn."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Metagross
        df = set_pokemon(df, "Beldum", ability="Levitate")
        df = add_move(df, "Beldum", {"level": 1, "move": "iron head"})
        df = add_move(df, "Beldum", {"level": 1, "move": "zen headbutt"})
        df = set_pokemon(df, "Metang", ability="Levitate")
        df = add_move(df, "Metang", {"level": 1, "move": "iron head"})
        df = add_move(df, "Metang", {"level": 1, "move": "zen headbutt"})
        pokemon = "Metagross"
        df = set_pokemon(
            df,
            pokemon,
            ability="Levitate",
            stats={
                "base_stats.HP": 100,
                "base_stats.ATK": 135,
                "base_stats.DEF": 130,
                "base_stats.SPA": 80,
                "base_stats.SPD": 110,
                "base_stats.SPE": 110,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "iron head"})
        df = add_move(df, pokemon, {"level": 1, "move": "smart strike"})
        df = add_move(df, pokemon, {"level": 38, "move": "zen headbutt"})
        df = add_move(df, pokemon, {"level": 40, "move": "recover"})
        df = add_move(df, pokemon, {"level": 42, "move": "bulk up"})
        df = add_move(df, pokemon, {"level": 41, "move": "drain punch"})
        # Kyogre
        df = set_pokemon(
            df,
            "Kyogre",
            ability="Primordial Sea",
            stats={
                "base_stats.HP": 100,
                "base_stats.ATK": 150,
                "base_stats.DEF": 90,
                "base_stats.SPA": 180,
                "base_stats.SPD": 160,
                "base_stats.SPE": 90,
            },
        )
        # Groudon
        df = set_pokemon(
            df,
            "Kyogre",
            types=("Ground", "Fire"),
            ability="Desolate Land",
            stats={
                "base_stats.HP": 100,
                "base_stats.ATK": 180,
                "base_stats.DEF": 160,
                "base_stats.SPA": 150,
                "base_stats.SPD": 90,
                "base_stats.SPE": 90,
            },
        )
        # Rayquaza
        df = set_pokemon(
            df,
            "Rayquaza",
            ability="Delta Stream",
            stats={
                "base_stats.HP": 105,
                "base_stats.ATK": 180,
                "base_stats.DEF": 100,
                "base_stats.SPA": 180,
                "base_stats.SPD": 100,
                "base_stats.SPE": 115,
            },
        )
        return df
