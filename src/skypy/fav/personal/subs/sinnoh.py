__all__ = ["SinnohEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class SinnohEditor(PersonalEditor):
    """Sinnoh."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Empoleon
        pokemon = "Empoleon"
        df = set_pokemon(
            df,
            pokemon,
            ability="Competitive",
            stats={
                "base_stats.HP": 94,
                "base_stats.ATK": 70,
                "base_stats.DEF": 88,
                "base_stats.SPA": 116,
                "base_stats.SPD": 107,
                "base_stats.SPE": 60,
            },
        )
        df = add_move(df, pokemon, {"level": 1, "move": "hydro cannon"})
        df = add_move(df, pokemon, {"level": 40, "move": "freeze-dry"})
        df = add_move(df, pokemon, {"level": 38, "move": "air slash"})
        # Luxray
        pokemon = "Luxray"
        df = set_pokemon(
            df,
            pokemon,
            types=("electric", "dark"),
            ability="Intimidate",
            stats={
                "base_stats.HP": 80,
                "base_stats.ATK": 120,
                "base_stats.DEF": 89,
                "base_stats.SPA": 60,
                "base_stats.SPD": 79,
                "base_stats.SPE": 95,
            },
        )
        df = add_move(df, pokemon, {"level": 38, "move": "crunch"})
        df = add_move(df, pokemon, {"level": 38, "move": "thunder fang"})
        df = add_move(df, pokemon, {"level": 38, "move": "ice fang"})
        df = add_move(df, pokemon, {"level": 38, "move": "fire fang"})
        df = add_move(df, pokemon, {"level": 38, "move": "iron tail"})
        # Spiritomb
        pokemon = "Spiritomb"
        df = set_pokemon(
            df,
            pokemon,
            ability=["Pressure", "Pressure", "Infiltrator"],
            stats={
                "base_stats.HP": 90,
                "base_stats.ATK": 52,
                "base_stats.DEF": 108,
                "base_stats.SPA": 92,
                "base_stats.SPD": 108,
                "base_stats.SPE": 35,
            },
        )
        df = add_move(df, pokemon, {"level": 38, "move": "calm mind"})
        # Magnezone
        pokemon = "Magnezone"
        df = set_pokemon(df, pokemon, ability="Levitate")
        # Yanmega
        pokemon = "Yanmega"
        df = set_pokemon(
            df,
            pokemon,
            types=("Bug", "Dragon"),
            ability="Levitate",
            stats={
                "base_stats.HP": 86,
                "base_stats.ATK": 56,
                "base_stats.DEF": 86,
                "base_stats.SPA": 116,
                "base_stats.SPD": 76,
                "base_stats.SPE": 95,
            },
        )
        df = add_move(df, pokemon, {"level": 38, "move": "quiver dance"})
        df = add_move(df, pokemon, {"level": 38, "move": "dragon pulse"})
        # Dusknoir
        pokemon = "Dusknoir"
        df = set_pokemon(
            df,
            pokemon,
            ability="Levitate",
            stats={
                "base_stats.HP": 70,
                "base_stats.ATK": 100,
                "base_stats.DEF": 165,
                "base_stats.SPA": 45,
                "base_stats.SPD": 165,
                "base_stats.SPE": 45,
            },
        )
        df = add_move(df, pokemon, {"level": 38, "move": "bulk up"})
        df = add_move(df, pokemon, {"level": 38, "move": "drain punch"})
        # Darkrai
        df = set_pokemon(
            df,
            "Darkrai",
            types=("dark", "ghost"),
            stats={
                "base_stats.HP": 92,
                "base_stats.ATK": 50,
                "base_stats.DEF": 78,
                "base_stats.SPA": 143,
                "base_stats.SPD": 95,
                "base_stats.SPE": 142,
            },
        )
        df = add_move(df, "Darkrai", {"level": 22, "move": "shadow ball"})
        df = add_move(df, "Darkrai", {"level": 40, "move": "psyshock"})
        df = add_move(df, "Darkrai", {"level": 44, "move": "mystical fire"})
        # Cresselia
        p = "Cresselia"
        df = set_pokemon(
            df,
            p,
            stats={
                "base_stats.HP": 140,
                "base_stats.ATK": 40,
                "base_stats.DEF": 110,
                "base_stats.SPA": 85,
                "base_stats.SPD": 120,
                "base_stats.SPE": 85,
            },
        )
        df = add_move(df, p, {"level": 1, "move": "psyshock"})
        df = add_move(df, p, {"level": 1, "move": "moonblast"})
        # Regigigas
        p = "Regigigas"
        df = set_pokemon(
            df,
            p,
            ability=["Slow Start", "Slow Start", "Mind's Eye"],
            stats={
                "base_stats.HP": 150,
                "base_stats.ATK": 160,
                "base_stats.DEF": 110,
                "base_stats.SPA": 30,
                "base_stats.SPD": 110,
                "base_stats.SPE": 110,
            },
        )
        df = add_move(df, p, {"level": 1, "move": "mega punch"})
        df = add_move(df, p, {"level": 1, "move": "mega kick"})
        df = add_move(df, p, {"level": 1, "move": "bulk up"})
        return df
