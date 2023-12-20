__all__ = ["KantoStarterEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class KantoStarterEditor(PersonalEditor):
    """Edit Kanto starters."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Venusaur
        pokemon = "Venusaur"
        df = set_pokemon(
            df,
            pokemon,
            ability=["thick fat", "thick fat", "thick fat"],
            stats={
                "base_stats.HP": 95,
                "base_stats.ATK": 52,
                "base_stats.DEF": 93,
                "base_stats.SPA": 110,
                "base_stats.SPD": 110,
                "base_stats.SPE": 80,
            },
        )
        df = add_move(df, pokemon, move=[{"level": 36, "move": "earth power"}])
        df = add_move(df, pokemon, move=[{"level": 38, "move": "giga drain"}])
        df = add_move(df, pokemon, move=[{"level": 38, "move": "jungle healing"}])
        df = add_move(df, pokemon, move=[{"level": 1, "move": "frenzy plant"}])
        # Charizard
        pokemon = "Charizard"
        df = set_pokemon(
            df,
            pokemon,
            ability="Drought",
            stats={
                "base_stats.HP": 78,
                "base_stats.ATK": 84,
                "base_stats.DEF": 78,
                "base_stats.SPA": 109,
                "base_stats.SPD": 85,
                "base_stats.SPE": 100,
            },
        )
        df = add_move(df, pokemon, move=[{"level": 36, "move": "dragon pulse"}])
        df = add_move(df, pokemon, move=[{"level": 38, "move": "dragon dance"}])
        df = add_move(df, pokemon, move=[{"level": 39, "move": "scorching sands"}])
        df = add_move(df, pokemon, move=[{"level": 1, "move": "blast burn"}])
        # Blastoise
        pokemon = "Blastoise"
        df = set_pokemon(
            df,
            pokemon,
            ability=["mega launcher", "mega launcher", "mega launcher"],
            stats={
                "base_stats.HP": 99,
                "base_stats.ATK": 60,
                "base_stats.DEF": 103,
                "base_stats.SPA": 100,
                "base_stats.SPD": 105,
                "base_stats.SPE": 68,
            },
        )
        df = add_move(df, pokemon, move=[{"level": 36, "move": "ice beam"}])
        df = add_move(df, pokemon, move=[{"level": 38, "move": "freeze-dry"}])
        df = add_move(df, pokemon, move=[{"level": 1, "move": "hydro cannon"}])
        # Pikachu
        for pokemon in POKEMON:
            if "pikachu-" in pokemon.lower():
                df = set_pokemon(
                    df,
                    pokemon,
                    ability=["static", "static", "static"],
                    stats={
                        "base_stats.HP": 85,
                        "base_stats.ATK": 50,
                        "base_stats.DEF": 70,
                        "base_stats.SPA": 94,
                        "base_stats.SPD": 75,
                        "base_stats.SPE": 110,
                    },
                )
                df = add_move(
                    df,
                    pokemon,
                    move=[
                        {"level": 36, "move": "surf"},
                        {"level": 38, "move": "flash cannon"},
                        {"level": 38, "move": "air slash"},
                    ],
                )
        # Partner Eeveee: stronger
        pokemon = "Eevee-1"
        df = set_pokemon(
            df,
            pokemon,
            ability=["Adaptability", "Adaptability", "Libero"],
            stats={
                "base_stats.HP": 65,
                "base_stats.ATK": 95,
                "base_stats.DEF": 80,
                "base_stats.SPA": 95,
                "base_stats.SPD": 90,
                "base_stats.SPE": 99,
            },
        )
        df = add_move(
            df,
            pokemon,
            move=[
                {"level": 1, "move": "extreme speed"},
                {"level": 2, "move": "swift"},
                {"level": 3, "move": "recover"},
                # vaporeon
                {"level": 5, "move": "water pulse"},
                {"level": 5, "move": "liquidation"},
                # flareon
                {"level": 8, "move": "flamethrower"},
                {"level": 8, "move": "fire fang"},
                # umbreon
                {"level": 9, "move": "dark pulse"},
                {"level": 9, "move": "crunch"},
                # jolteon
                {"level": 12, "move": "thunderbolt"},
                {"level": 12, "move": "thunder fang"},
                # glaceon
                {"level": 18, "move": "freeze-dry"},
                {"level": 18, "move": "ice fang"},
                # espeon
                {"level": 19, "move": "psyshock"},
                {"level": 19, "move": "zen headbutt"},
                # leafeon
                {"level": 22, "move": "razor leaf"},
                {"level": 23, "move": "energy ball"},
                # sylveon
                {"level": 24, "move": "moonblast"},
                {"level": 25, "move": "play rough"},
            ],
        )
        return df
