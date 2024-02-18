__all__ = ["HisuiEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops.setters import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class HisuiEditor(PersonalEditor):
    """Edit Hisui."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Hisuian Decidueye
        pokemon = "Hisuian Decidueye"
        df = set_pokemon(
            df,
            pokemon,
            ability="Scrappy",
            stats={
                "base_stats.HP": 78,
                "base_stats.ATK": 127,
                "base_stats.DEF": 80,
                "base_stats.SPA": 55,
                "base_stats.SPD": 80,
                "base_stats.SPE": 110,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "bulk up"})
        df = add_move(df, pokemon, {"level": 1, "move": "jungle healing"})
        df = add_move(df, pokemon, {"level": 1, "move": "Spirit Shackle"})
        # Hisuian Typhlosion
        df = add_evo(df, "Quilava", level=32, into="Hisuian Typhlosion")
        pokemon = "Hisuian Typhlosion"
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
        df = add_move(df, "Hisuian Typhlosion", {"level": 25, "move": "scorching sands"})
        # Hisuian Samurott
        df = add_evo(df, "Dewott", level=35, into="Hisuian Samurott")
        pokemon = "Hisuian Samurott"
        df = set_pokemon(
            df,
            pokemon,
            ability="Sharpness",
            stats={
                "base_stats.HP": 90,
                "base_stats.ATK": 118,
                "base_stats.DEF": 80,
                "base_stats.SPA": 65,
                "base_stats.SPD": 80,
                "base_stats.SPE": 95,
            },
        )
        df = add_move(df, pokemon, move={"level": 38, "move": "smart strike"})
        df = add_move(df, pokemon, move={"level": 38, "move": "liquidation"})
        df = add_move(df, pokemon, move={"level": 38, "move": "poison jab"})
        # Braviary
        df = add_evo(df, "Rufflet", level=30, into="Hisuian Braviary")
        # Wyrdeer
        df = add_evo(df, "Stantler", level=40, into="Wyrdeer")
        # Hisuian Zoroark
        pokemon = "Hisuian Zoroark"
        df = set_pokemon(
            df,
            pokemon,
            stats={
                "base_stats.HP": 75,
                "base_stats.ATK": 60,
                "base_stats.DEF": 70,
                "base_stats.SPA": 125,
                "base_stats.SPD": 70,
                "base_stats.SPE": 110,
            },
        )
        df = add_move(
            df,
            pokemon,
            [
                {"level": 36, "move": "mystical fire"},
                {"level": 37, "move": "calm mind"},
                {"level": 42, "move": "sludge bomb"},
                {"level": 43, "move": "tri attack"},
            ],
        )
        # Sneasler
        df = add_evo(df, "Hisuian Sneasel", level=42, into="Sneasler")
        pokemon = "Sneasler"
        df = set_pokemon(
            df,
            pokemon,
            ability="Tough Claws",
        )
        df = add_move(
            df,
            pokemon,
            [
                {"level": 36, "move": "iron head"},
                {"level": 37, "move": "bulk up"},
                {"level": 42, "move": "drain punch"},
            ],
        )
        # Hisuian Electrode
        pokemon = "Hisuian Electrode"
        df = set_pokemon(
            df,
            pokemon,
            ability=["Soundproof", "Static", "Aftermath"],
            stats={
                "base_stats.HP": 60,
                "base_stats.ATK": 30,
                "base_stats.DEF": 70,
                "base_stats.SPA": 100,
                "base_stats.SPD": 80,
                "base_stats.SPE": 150,
            },
        )
        # Hisuian Avalugg
        df = add_evo(df, "Bergmite", level=33, into="Hisuian Avalugg")
        pokemon = "Hisuian Avalugg"
        df = set_pokemon(
            df,
            pokemon,
            ability=["Strong Jaw", "Ice Body", "Sturdy"],
            stats={
                "base_stats.HP": 95,
                "base_stats.ATK": 127,
                "base_stats.DEF": 184,
                "base_stats.SPA": 5,
                "base_stats.SPD": 95,
                "base_stats.SPE": 28,
            },
        )
        df = add_move(df, pokemon, {"level": 36, "move": "stone axe"})
        df = add_move(df, pokemon, {"level": 37, "move": "ice fang"})
        df = add_move(df, pokemon, {"level": 38, "move": "bulk up"})
        df = add_move(df, pokemon, {"level": 39, "move": "recover"})
        # Hisuian Goodra
        df = add_evo(df, "Hisuian Sliggoo", level=50, into="Hisuian Goodra")
        pokemon = "Hisuian Goodra"
        df = set_pokemon(
            df,
            pokemon,
            ability=["Sap Sipper", "Shell Armor", "Gooey"],
            stats={
                "base_stats.HP": 90,
                "base_stats.ATK": 70,
                "base_stats.DEF": 130,
                "base_stats.SPA": 110,
                "base_stats.SPD": 150,
                "base_stats.SPE": 50,
            },
        )
        df = add_move(df, pokemon, {"level": 36, "move": "flash cannon"})
        return df
