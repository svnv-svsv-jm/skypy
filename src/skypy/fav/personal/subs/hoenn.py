__all__ = ["HoennEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops.setters import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class HoennEditor(PersonalEditor):
    """Hoenn."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Sceptile
        pokemon = "Sceptile"
        df = set_pokemon(
            df,
            pokemon,
            types=("Grass", "Dragon"),
            ability="Filter",
            stats={
                "base_stats.HP": 70,
                "base_stats.ATK": 60,
                "base_stats.DEF": 85,
                "base_stats.SPA": 110,
                "base_stats.SPD": 85,
                "base_stats.SPE": 125,
            },
        )
        df = add_move(df, pokemon, move=[{"level": 1, "move": "frenzy plant"}])
        df = add_move(df, pokemon, {"level": 1, "move": "jungle healing"})
        df = add_move(df, pokemon, {"level": 1, "move": "dragon pulse"})
        df = add_move(df, pokemon, {"level": 1, "move": "dragon dance"})
        # Cacturne
        pokemon = "Cacturne"
        df = set_pokemon(
            df,
            pokemon,
            stats={
                "base_stats.HP": 70,
                "base_stats.ATK": 115,
                "base_stats.DEF": 110,
                "base_stats.SPA": 50,
                "base_stats.SPD": 70,
                "base_stats.SPE": 70,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "sucker punch"})
        # Altaria
        pokemon = "Altaria"
        df = set_pokemon(
            df,
            pokemon,
            types=("Dragon", "Fairy"),
            ability="Levitate",
        )
        df = add_move(df, pokemon, {"level": 1, "move": "moonblast"})
        df = add_move(df, pokemon, {"level": 1, "move": "play rough"})
        # Glalie
        pokemon = "Glalie"
        df = set_pokemon(
            df,
            pokemon,
            types=("Ice", "Ghost"),
            ability="Levitate",
            stats={
                "base_stats.HP": 90,
                "base_stats.ATK": 40,
                "base_stats.DEF": 80,
                "base_stats.SPA": 100,
                "base_stats.SPD": 80,
                "base_stats.SPE": 90,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "shadow ball"})
        df = add_move(df, pokemon, {"level": 1, "move": "hex"})
        df = add_move(df, pokemon, {"level": 1, "move": "Will-O-Wisp"})
        # Seviper
        pokemon = "Seviper"
        df = set_pokemon(
            df,
            pokemon,
            types=("Poison", "Dragon"),
            ability=["Shed Skin", "Shed Skin", "Infiltrator"],
            stats={
                "base_stats.HP": 73,
                "base_stats.ATK": 100,
                "base_stats.DEF": 80,
                "base_stats.SPA": 50,
                "base_stats.SPD": 70,
                "base_stats.SPE": 95,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "dragon dance"})
        df = add_move(df, pokemon, {"level": 1, "move": "dragon pulse"})
        df = add_move(df, pokemon, {"level": 1, "move": "dragon claw"})
        df = add_move(df, pokemon, {"level": 1, "move": "dragon tail"})
        df = add_move(df, pokemon, {"level": 1, "move": "poison fang"})
        df = add_move(df, pokemon, {"level": 1, "move": "poison tail"})
        df = add_move(df, pokemon, {"level": 1, "move": "fire fang"})
        df = add_move(df, pokemon, {"level": 1, "move": "iron tail"})
        # Dusclops
        p = "Dusclops"
        df = add_evo(df, p, level=48, into="Dusknoir")
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
                "base_stats.DEF": 120,
                "base_stats.SPA": 70,
                "base_stats.SPD": 100,
                "base_stats.SPE": 110,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "iron head"})
        df = add_move(df, pokemon, {"level": 1, "move": "smart strike"})
        df = add_move(df, pokemon, {"level": 38, "move": "zen headbutt"})
        df = add_move(df, pokemon, {"level": 40, "move": "recover"})
        df = add_move(df, pokemon, {"level": 42, "move": "bulk up"})
        df = add_move(df, pokemon, {"level": 41, "move": "drain punch"})
        # Deoxys-2
        pokemon = "Deoxys-2"
        df = set_pokemon(
            df,
            pokemon,
            ability="Filter",
            stats={
                "base_stats.HP": 110,
                "base_stats.ATK": 40,
                "base_stats.DEF": 160,
                "base_stats.SPA": 70,
                "base_stats.SPD": 160,
                "base_stats.SPE": 60,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "shelter"})
        df = add_move(df, pokemon, {"level": 1, "move": "calm mind"})
        # Deoxys-3
        pokemon = "Deoxys-3"
        df = set_pokemon(
            df,
            pokemon,
            ability="Filter",
            stats={
                "base_stats.HP": 65,
                "base_stats.ATK": 40,
                "base_stats.DEF": 95,
                "base_stats.SPA": 100,
                "base_stats.SPD": 95,
                "base_stats.SPE": 205,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "calm mind"})
        # Kyogre
        pokemon = "Kyogre"
        df = set_pokemon(
            df,
            pokemon,
            ability="Primordial Sea",
            stats={
                "base_stats.HP": 100,
                "base_stats.ATK": 90,
                "base_stats.DEF": 150,
                "base_stats.SPA": 180,
                "base_stats.SPD": 160,
                "base_stats.SPE": 90,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "freeze-dry"})
        df = add_move(df, pokemon, {"level": 1, "move": "scald"})
        df = add_move(df, pokemon, {"level": 1, "move": "calm mind"})
        # Groudon
        pokemon = "Groudon"
        df = set_pokemon(
            df,
            pokemon,
            types=("Ground", "Fire"),
            ability="Desolate Land",
            stats={
                "base_stats.HP": 100,
                "base_stats.ATK": 180,
                "base_stats.DEF": 160,
                "base_stats.SPA": 90,
                "base_stats.SPD": 150,
                "base_stats.SPE": 90,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "bulk up"})
        df = add_move(df, pokemon, {"level": 1, "move": "fire punch"})
        df = add_move(df, pokemon, {"level": 1, "move": "rock slide"})
        # Rayquaza
        pokemon = "Rayquaza"
        df = set_pokemon(
            df,
            pokemon,
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
        df = add_move(df, pokemon, {"level": 1, "move": "rock slide"})
        df = add_move(df, pokemon, {"level": 1, "move": "blast burn"})
        return df
