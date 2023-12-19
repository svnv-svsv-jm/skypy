__all__ = ["KantoEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class KantoEditor(PersonalEditor):
    """Edit Kanto."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Gengar
        pokemon = "gengar"
        df = set_pokemon(
            df,
            pokemon,
            ability=["levitate", "levitate", "levitate"],
            stats={
                "base_stats.HP": 72,
                "base_stats.ATK": 67,
                "base_stats.DEF": 71,
                "base_stats.SPA": 123,
                "base_stats.SPD": 75,
                "base_stats.SPE": 132,
            },
        )
        df = add_move(df, pokemon, {"level": 33, "move": "sludge bomb"})
        df = add_move(df, pokemon, {"level": 36, "move": "energy ball"})
        df = add_move(df, pokemon, {"level": 42, "move": "psychic"})
        df = add_move(df, pokemon, {"level": 52, "move": "thunderbolt"})
        # Articuno
        pokemon = "Articuno"
        df = set_pokemon(
            df,
            pokemon,
            ability="snow warning",
            stats={
                "base_stats.HP": 95,
                "base_stats.ATK": 10,
                "base_stats.DEF": 80,
                "base_stats.SPA": 140,
                "base_stats.SPD": 125,
                "base_stats.SPE": 130,
            },
        )
        df = add_move(
            df,
            pokemon,
            [
                {"level": 36, "move": "water pulse"},
                {"level": 36, "move": "freeze-dry"},
            ],
        )
        # Mewtwo
        pokemon = "Mewtwo"
        df = set_pokemon(
            df,
            pokemon,
            ability="magic bounce",
            stats={
                "base_stats.HP": 156,
                "base_stats.ATK": 110,
                "base_stats.DEF": 90,
                "base_stats.SPA": 154,
                "base_stats.SPD": 120,
                "base_stats.SPE": 150,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "recover"})
        df = add_move(df, pokemon, {"level": 33, "move": "ice beam"})
        df = add_move(df, pokemon, {"level": 36, "move": "aura sphere"})
        df = add_move(df, pokemon, {"level": 40, "move": "psystrike"})
        df = add_move(df, pokemon, {"level": 44, "move": "moonblast"})
        df = add_move(df, pokemon, {"level": 52, "move": "thunderbolt"})
        return df
