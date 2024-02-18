__all__ = ["PaldeaEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops.setters import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class PaldeaEditor(PersonalEditor):
    """Paldea."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Tinkaton
        p = "Tinkaton"
        df = set_pokemon(
            df,
            p,
            stats={
                "base_stats.HP": 85,
                "base_stats.ATK": 85,
                "base_stats.DEF": 94,
                "base_stats.SPA": 50,
                "base_stats.SPD": 105,
                "base_stats.SPE": 87,
            },
        )
        df = add_move(df, p, {"level": 40, "move": "iron defense"})
        df = add_move(df, p, {"level": 40, "move": "swords dance"})
        # Farigiraf
        p = "Farigiraf"
        df = set_pokemon(
            df,
            p,
            stats={
                "base_stats.HP": 120,
                "base_stats.ATK": 40,
                "base_stats.DEF": 90,
                "base_stats.SPA": 110,
                "base_stats.SPD": 80,
                "base_stats.SPE": 70,
            },
        )
        df = add_move(df, p, {"level": 40, "move": "psyshock"})
        df = add_move(df, p, {"level": 40, "move": "shadow ball"})
        df = add_move(df, p, {"level": 40, "move": "tri attack"})
        df = add_move(df, p, {"level": 40, "move": "calm mind"})
        # Dudunsparce
        for p in POKEMON:
            if "dudunsparce" in p.lower():
                df = set_pokemon(
                    df,
                    p,
                    ability=["Serene Grace", "Serene Grace", "Serene Grace"],
                    stats={
                        "base_stats.HP": 125,
                        "base_stats.ATK": 100,
                        "base_stats.DEF": 80,
                        "base_stats.SPA": 55,
                        "base_stats.SPD": 85,
                        "base_stats.SPE": 75,
                    },
                )
                df = add_move(df, p, {"level": 40, "move": "dragon dance"})
                df = add_move(df, p, {"level": 42, "move": "play rough"})
                df = add_move(df, p, {"level": 43, "move": "iron tail"})
                df = add_move(df, p, {"level": 46, "move": "poison tail"})
                df = add_move(df, p, {"level": 48, "move": "earthquake"})
                df = add_move(df, p, {"level": 1, "move": "roost"})
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
                "base_stats.HP": 123,
                "base_stats.ATK": 45,
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
