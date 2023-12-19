__all__ = ["JohtoEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from .base import PersonalEditor


class JohtoEditor(PersonalEditor):
    """Edit Johto."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Meganium
        df = set_pokemon(
            df,
            "Meganium",
            types=("grass", "fairy"),
            ability=["Grassy Surge", "Grassy Surge", "Magic Bounce"],
            stats={
                "base_stats.HP": 97,
                "base_stats.ATK": 20,
                "base_stats.DEF": 105,
                "base_stats.SPA": 113,
                "base_stats.SPD": 105,
                "base_stats.SPE": 95,
            },
        )
        df = add_move(df, "Meganium", {"level": 44, "move": "jungle healing"})
        df = add_move(df, "Meganium", {"level": 44, "move": "calm mind"})
        df = add_move(df, "Meganium", {"level": 36, "move": "energy ball"})
        df = add_move(df, "Meganium", {"level": 36, "move": "giga drain"})
        df = add_move(df, "Meganium", {"level": 36, "move": "moonblast"})
        df = add_move(df, "Meganium", {"level": 38, "move": "draining kiss"})
        # Typhlosion
        pokemon = "Typhlosion"
        df = set_pokemon(
            df,
            pokemon,
            ability="flash fire",
            stats={
                "base_stats.HP": 78,
                "base_stats.ATK": 65,
                "base_stats.DEF": 84,
                "base_stats.SPA": 128,
                "base_stats.SPD": 85,
                "base_stats.SPE": 95,
            },
        )
        df = add_move(df, "Typhlosion", {"level": 25, "move": "scorching sands"})
        # Feraligatr
        pokemon = "Feraligatr"
        df = set_pokemon(
            df,
            pokemon,
            ability=["Tough Claws", "Tough Claws", "Sheer Force"],
            stats={
                "base_stats.HP": 90,
                "base_stats.ATK": 110,
                "base_stats.DEF": 107,
                "base_stats.SPA": 65,
                "base_stats.SPD": 78,
                "base_stats.SPE": 85,
            },
        )
        df = add_move(df, "Feraligatr", {"level": 36, "move": "ice punch"})
        df = add_move(df, "Feraligatr", {"level": 25, "move": "waterfall"})
        df = add_move(df, "Feraligatr", {"level": 28, "move": "liquidation"})
        df = add_move(df, "Feraligatr", {"level": 33, "move": "dragon dance"})
        # Umbreon
        df = set_pokemon(
            df,
            "Umbreon",
            stats={
                "base_stats.HP": 95,
                "base_stats.ATK": 50,
                "base_stats.DEF": 110,
                "base_stats.SPA": 80,
                "base_stats.SPD": 130,
                "base_stats.SPE": 60,
            },
        )
        df = add_move(df, "Umbreon", {"level": 36, "move": "psyshock"})
        df = add_move(df, "Umbreon", {"level": 38, "move": "sludge bomb"})
        df = add_move(df, "Umbreon", {"level": 42, "move": "calm mind"})
        # Houndoom
        df = set_pokemon(
            df,
            "Houndoom",
            ability="Flash Fire",
            stats={
                "base_stats.HP": 90,
                "base_stats.ATK": 80,
                "base_stats.DEF": 80,
                "base_stats.SPA": 130,
                "base_stats.SPD": 80,
                "base_stats.SPE": 95,
            },
        )
        df = add_move(df, "Houndoom", {"level": 38, "move": "sludge bomb"})
        # Ursaring
        df = add_evo(df, "Ursaring", level=42, into="Ursaluna")
        # Steelix
        df = add_evo(df, "Onix", level=42, into="Steelix")
        pokemon = "Steelix"
        df = set_pokemon(
            df,
            pokemon,
            ability=["Rock Head", "Sturdy", "Sheer Force"],
            stats={
                "base_stats.HP": 75,
                "base_stats.ATK": 85,
                "base_stats.DEF": 200,
                "base_stats.SPA": 55,
                "base_stats.SPD": 65,
                "base_stats.SPE": 30,
            },
        )
        df = add_move(df, pokemon, {"level": 38, "move": "stone axe"})
        df = add_move(df, pokemon, {"level": 40, "move": "bulk up"})
        df = add_move(df, pokemon, {"level": 40, "move": "dragon dance"})
        # Tyranitar
        pokemon = "Tyranitar"
        df = set_pokemon(
            df,
            pokemon,
            ability="Sand Stream",
            stats={
                "base_stats.HP": 130,
                "base_stats.ATK": 134,
                "base_stats.DEF": 150,
                "base_stats.SPA": 71,
                "base_stats.SPD": 120,
                "base_stats.SPE": 95,
            },
        )
        df = add_move(df, pokemon, {"level": 38, "move": "stone axe"})
        df = add_move(df, pokemon, {"level": 40, "move": "dragon dance"})
        # Raikou
        pokemon = "Raikou"
        df = set_pokemon(
            df,
            pokemon,
            ability="Volt Absorb",
            stats={
                "base_stats.HP": 100,
                "base_stats.ATK": 60,
                "base_stats.DEF": 80,
                "base_stats.SPA": 125,
                "base_stats.SPD": 80,
                "base_stats.SPE": 135,
            },
        )
        df = add_move(df, pokemon, {"level": 35, "move": "Shadow Ball"})
        df = add_move(df, pokemon, {"level": 44, "move": "Dark Pulse"})
        # Entei
        pokemon = "Entei"
        df = set_pokemon(
            df,
            pokemon,
            ability="Flash Fire",
            stats={
                "base_stats.HP": 100,
                "base_stats.ATK": 130,
                "base_stats.DEF": 90,
                "base_stats.SPA": 60,
                "base_stats.SPD": 90,
                "base_stats.SPE": 110,
            },
        )
        df = add_move(df, pokemon, {"level": 33, "move": "Dragon Dance"})
        df = add_move(df, pokemon, {"level": 44, "move": "Sacred Fire"})
        df = add_move(df, pokemon, {"level": 22, "move": "Flare Blitz"})
        # Suicune
        pokemon = "Suicune"
        df = set_pokemon(
            df,
            pokemon,
            ability="Water Absorb",
            stats={
                "base_stats.HP": 100,
                "base_stats.ATK": 60,
                "base_stats.DEF": 120,
                "base_stats.SPA": 85,
                "base_stats.SPD": 120,
                "base_stats.SPE": 95,
            },
        )
        df = add_move(df, pokemon, {"level": 35, "move": "Scald"})
        df = add_move(df, pokemon, {"level": 38, "move": "Freeze-Dry"})
        df = add_move(df, pokemon, {"level": 40, "move": "Hydro Steam"})
        # Ho-Oh
        pokemon = "Ho-Oh"
        df = set_pokemon(
            df,
            pokemon,
            ability=["Flash Fire", "Flash Fire", "Regenerator"],
            stats={
                "base_stats.HP": 106,
                "base_stats.ATK": 130,
                "base_stats.DEF": 120,
                "base_stats.SPA": 80,
                "base_stats.SPD": 154,
                "base_stats.SPE": 110,
            },
        )
        df = add_move(df, pokemon, {"level": 35, "move": "Earthquake"})
        # Lugia
        pokemon = "Lugia"
        df = set_pokemon(
            df,
            pokemon,
            ability=["Water Absorb", "Water Absorb", "Multiscale"],
            stats={
                "base_stats.HP": 136,
                "base_stats.ATK": 70,
                "base_stats.DEF": 130,
                "base_stats.SPA": 90,
                "base_stats.SPD": 154,
                "base_stats.SPE": 120,
            },
        )
        df = add_move(df, pokemon, {"level": 35, "move": "Hydro Steam"})
        df = add_move(df, pokemon, {"level": 33, "move": "Scald"})
        df = add_move(df, pokemon, {"level": 44, "move": "Scorching Sands"})
        # Celebi
        pokemon = "Celebi"
        df = set_pokemon(
            df,
            pokemon,
            ability=["Filter", "Filter", "Natural Cure"],
            stats={
                "base_stats.HP": 150,
                "base_stats.ATK": 30,
                "base_stats.DEF": 100,
                "base_stats.SPA": 100,
                "base_stats.SPD": 100,
                "base_stats.SPE": 120,
            },
        )
        df = add_move(df, pokemon, {"level": 31, "move": "Quiver Dance"})
        df = add_move(df, pokemon, {"level": 32, "move": "Jungle Healing"})
        df = add_move(df, pokemon, {"level": 35, "move": "Seed Flare"})
        df = add_move(df, pokemon, {"level": 36, "move": "Psyshock"})
        # Return
        return df
