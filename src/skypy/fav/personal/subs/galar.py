__all__ = ["GalarEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops.setters import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class GalarEditor(PersonalEditor):
    """Galar."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Rillaboom
        p = "Rillaboom"
        df = set_pokemon(
            df,
            p,
            ability="Grassy Surge",
            stats={
                "base_stats.HP": 100,
                "base_stats.ATK": 125,
                "base_stats.DEF": 90,
                "base_stats.SPA": 50,
                "base_stats.SPD": 80,
                "base_stats.SPE": 85,
            },
        )
        df = add_move(df, p, {"level": 36, "move": "knock off"})
        df = add_move(df, p, {"level": 36, "move": "earthquake"})
        df = add_move(df, p, {"level": 36, "move": "drain punch"})
        df = add_move(df, p, {"level": 36, "move": "bulk up"})
        df = add_move(df, p, {"level": 36, "move": "jungle healing"})
        # Cinderace
        p = "cinderace"
        df = set_pokemon(
            df,
            p,
            ability=["Blaze", "Blaze", "Libero"],
            stats={
                "base_stats.HP": 70,
                "base_stats.ATK": 106,
                "base_stats.DEF": 75,
                "base_stats.SPA": 65,
                "base_stats.SPD": 75,
                "base_stats.SPE": 109,
            },
        )
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
        # Galarian Slowking
        pokemon = "Galarian Slowking"
        df = set_pokemon(
            df,
            pokemon,
            ability="Regenerator",
            stats={
                "base_stats.HP": 135,
                "base_stats.ATK": 20,
                "base_stats.DEF": 105,
                "base_stats.SPA": 100,
                "base_stats.SPD": 110,
                "base_stats.SPE": 20,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "scald"})
        df = add_move(df, pokemon, {"level": 1, "move": "flamethrower"})
        df = add_move(df, pokemon, {"level": 1, "move": "eerie spell"})
        # Dreepy
        df = add_evo(df, "Dreepy", level=25, into="Drakloak")
        df = add_evo(df, "Drakloak", level=45, into="Dragapult")
        # Urshifu
        df = add_evo(df, "Kubfu", level=42, into="Urshifu")
        for pokemon in ["Urshifu", "Urshifu-1"]:
            df = set_pokemon(
                df,
                pokemon,
                stats={
                    "base_stats.HP": 110,
                    "base_stats.ATK": 135,
                    "base_stats.DEF": 105,
                    "base_stats.SPA": 10,
                    "base_stats.SPD": 93,
                    "base_stats.SPE": 97,
                },
            )
            df = add_move(df, pokemon, {"level": 1, "move": "poison jab"})
            df = add_move(df, pokemon, {"level": 1, "move": "iron head"})
            df = add_move(df, pokemon, {"level": 1, "move": "drain punch"})
            df = add_move(df, pokemon, {"level": 1, "move": "bulk up"})
        # Zarude
        for pokemon in ["Zarude", "Zarude-Dada"]:
            df = set_pokemon(
                df,
                pokemon,
                ability="tough claws",
                stats={
                    "base_stats.HP": 105,
                    "base_stats.ATK": 130,
                    "base_stats.DEF": 105,
                    "base_stats.SPA": 50,
                    "base_stats.SPD": 95,
                    "base_stats.SPE": 115,
                },
            )
            df = add_move(df, pokemon, {"level": 1, "move": "crunch"})
            df = add_move(df, pokemon, {"level": 1, "move": "bulk up"})
            df = add_move(df, pokemon, {"level": 1, "move": "power whip"})
            df = add_move(df, pokemon, {"level": 1, "move": "drain punch"})
            df = add_move(df, pokemon, {"level": 1, "move": "rock slide"})
        return df
