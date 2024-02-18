__all__ = ["JohtoEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops.setters import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class JohtoEditor(PersonalEditor):
    """Edit Johto."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Meganium
        pokemon = "Meganium"
        df = set_pokemon(
            df,
            pokemon,
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
        df = add_move(df, pokemon, move=[{"level": 1, "move": "frenzy plant"}])
        df = add_move(df, pokemon, {"level": 44, "move": "jungle healing"})
        df = add_move(df, pokemon, {"level": 44, "move": "calm mind"})
        df = add_move(df, pokemon, {"level": 36, "move": "energy ball"})
        df = add_move(df, pokemon, {"level": 36, "move": "giga drain"})
        df = add_move(df, pokemon, {"level": 36, "move": "moonblast"})
        df = add_move(df, pokemon, {"level": 38, "move": "draining kiss"})
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
        df = add_move(df, pokemon, move=[{"level": 1, "move": "blast burn"}])
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
        df = add_move(df, pokemon, move=[{"level": 1, "move": "hydro cannon"}])
        df = add_move(df, pokemon, {"level": 36, "move": "ice punch"})
        df = add_move(df, pokemon, {"level": 25, "move": "waterfall"})
        df = add_move(df, pokemon, {"level": 28, "move": "liquidation"})
        df = add_move(df, pokemon, {"level": 33, "move": "dragon dance"})
        # Ariados
        p = "Ariados"
        df = set_pokemon(
            df,
            p,
            ability=["Swarm", "Insomnia", "Sniper"],
            stats={
                "base_stats.HP": 70,
                "base_stats.ATK": 95,
                "base_stats.DEF": 70,
                "base_stats.SPA": 35,
                "base_stats.SPD": 70,
                "base_stats.SPE": 60,
            },
        )
        df = add_move(df, p, {"level": 1, "move": "cross poison"})
        df = add_move(df, p, {"level": 1, "move": "x-scissor"})
        df = add_move(df, p, {"level": 1, "move": "swords dance"})
        # Noctowl
        p = "Noctowl"
        df = set_pokemon(
            df,
            p,
            ability=["Insomnia", "Insomnia", "Tinted Lens"],
            stats={
                "base_stats.HP": 100,
                "base_stats.ATK": 50,
                "base_stats.DEF": 70,
                "base_stats.SPA": 86,
                "base_stats.SPD": 96,
                "base_stats.SPE": 80,
            },
        )
        df = add_move(df, p, {"level": 1, "move": "tri attack"})
        df = add_move(df, p, {"level": 1, "move": "shadow ball"})
        df = add_move(df, p, {"level": 1, "move": "psyshock"})
        df = add_move(df, p, {"level": 1, "move": "calm mind"})
        # Ampharos
        p = "Ampharos"
        df = set_pokemon(
            df,
            p,
            types=("Electric", "Dragon"),
            ability=["Static", "Static", "Mold Breaker"],
            stats={
                "base_stats.HP": 95,
                "base_stats.ATK": 65,
                "base_stats.DEF": 90,
                "base_stats.SPA": 115,
                "base_stats.SPD": 95,
                "base_stats.SPE": 75,
            },
        )
        df = add_move(df, p, {"level": 1, "move": "dragon pulse"})
        df = add_move(df, p, {"level": 1, "move": "nasty plot"})
        df = add_move(df, p, {"level": 1, "move": "earth power"})
        # Bellossom
        p = "Bellossom"
        df = set_pokemon(
            df,
            p,
            types=("Grass", "Grass"),
            ability="Shed Skin",
            stats={
                "base_stats.HP": 85,
                "base_stats.ATK": 30,
                "base_stats.DEF": 95,
                "base_stats.SPA": 100,
                "base_stats.SPD": 120,
                "base_stats.SPE": 60,
            },
        )
        df = add_move(df, p, {"level": 1, "move": "calm mind"})
        df = add_move(df, p, {"level": 1, "move": "giga drain"})
        df = add_move(df, p, {"level": 1, "move": "power gem"})
        df = add_move(df, p, {"level": 1, "move": "shadow ball"})
        df = add_move(df, p, {"level": 1, "move": "moonblast"})
        # Politoed
        p = "Politoed"
        df = set_pokemon(
            df,
            p,
            ability="Drizzle",
            stats={
                "base_stats.HP": 90,
                "base_stats.ATK": 50,
                "base_stats.DEF": 95,
                "base_stats.SPA": 95,
                "base_stats.SPD": 100,
                "base_stats.SPE": 70,
            },
        )
        df = add_move(df, p, {"level": 1, "move": "calm mind"})
        df = add_move(df, p, {"level": 1, "move": "water pulse"})
        df = add_move(df, p, {"level": 1, "move": "ice beam"})
        df = add_move(df, p, {"level": 1, "move": "psyshock"})
        # Jumpluff
        p = "Jumpluff"
        df = set_pokemon(
            df,
            p,
            ability=["Chlorophyll", "Leaf Guard", "Infiltrator"],
            stats={
                "base_stats.HP": 75,
                "base_stats.ATK": 50,
                "base_stats.DEF": 70,
                "base_stats.SPA": 75,
                "base_stats.SPD": 95,
                "base_stats.SPE": 110,
            },
        )
        df = add_move(df, p, {"level": 1, "move": "calm mind"})
        df = add_move(df, p, {"level": 1, "move": "giga drain"})
        df = add_move(df, p, {"level": 1, "move": "air slash"})
        df = add_move(df, p, {"level": 1, "move": "Vacuum Wave"})
        df = add_move(df, p, {"level": 1, "move": "bug buzz"})
        # Gligar
        p = "Gligar"
        df = add_evo(df, p, level=42, into="Gliscor")
        # Yanma
        p = "Yanma"
        df = add_evo(df, p, level=33, into="Yanmega")
        # Granbull
        p = "Granbull"
        df = set_pokemon(
            df,
            p,
            types=("Fairy", "Ground"),
            ability=["Intimidate", "Intimidate", "Strong Jaw"],
            stats={
                "base_stats.HP": 90,
                "base_stats.ATK": 120,
                "base_stats.DEF": 75,
                "base_stats.SPA": 40,
                "base_stats.SPD": 65,
                "base_stats.SPE": 65,
            },
        )
        df = add_move(df, p, {"level": 1, "move": "bulk up"})
        df = add_move(df, p, {"level": 1, "move": "drain punch"})
        df = add_move(df, p, {"level": 1, "move": "earthquake"})
        df = add_move(df, p, {"level": 1, "move": "psychic fangs"})
        df = add_move(df, p, {"level": 1, "move": "fire fang"})
        df = add_move(df, p, {"level": 1, "move": "ice fang"})
        df = add_move(df, p, {"level": 1, "move": "crunch"})
        df = add_move(df, p, {"level": 1, "move": "play rough"})
        # Quagsire
        p = "Quagsire"
        df = set_pokemon(
            df,
            p,
            ability="Water Absorb",
            stats={
                "base_stats.HP": 95,
                "base_stats.ATK": 95,
                "base_stats.DEF": 95,
                "base_stats.SPA": 35,
                "base_stats.SPD": 85,
                "base_stats.SPE": 30,
            },
        )
        df = add_move(df, p, {"level": 1, "move": "liquidation"})
        df = add_move(df, p, {"level": 1, "move": "earthquake"})
        df = add_move(df, p, {"level": 1, "move": "recover"})
        df = add_move(df, p, {"level": 1, "move": "bulk up"})
        df = add_move(df, p, {"level": 1, "move": "ice punch"})
        # Magcargo
        p = "Magcargo"
        df = set_pokemon(
            df,
            p,
            ability=["Magma Armor", "Flame Body", "Solid Rock"],
            stats={
                "base_stats.HP": 80,
                "base_stats.ATK": 20,
                "base_stats.DEF": 120,
                "base_stats.SPA": 90,
                "base_stats.SPD": 100,
                "base_stats.SPE": 20,
            },
        )
        df = add_move(df, p, {"level": 1, "move": "magma storm"})
        df = add_move(df, p, {"level": 1, "move": "power gem"})
        # Skarmory
        p = "Skarmory"
        df = set_pokemon(
            df,
            p,
            ability=["Sturdy", "Sturdy", "Sturdy"],
            stats={
                "base_stats.HP": 75,
                "base_stats.ATK": 80,
                "base_stats.DEF": 140,
                "base_stats.SPA": 30,
                "base_stats.SPD": 80,
                "base_stats.SPE": 90,
            },
        )
        df = add_move(df, p, {"level": 1, "move": "iron head"})
        df = add_move(df, p, {"level": 1, "move": "dual wingbeat"})
        df = add_move(df, p, {"level": 1, "move": "bulk up"})
        df = add_move(df, p, {"level": 1, "move": "night slash"})
        df = add_move(df, p, {"level": 1, "move": "drill peck"})
        df = add_move(df, p, {"level": 1, "move": "drill run"})
        # Donphan
        pokemon = "Donphan"
        df = set_pokemon(
            df,
            pokemon,
            ability=["Sturdy", "Sturdy", "Sand Stream"],
            stats={
                "base_stats.HP": 115,
                "base_stats.ATK": 111,
                "base_stats.DEF": 111,
                "base_stats.SPA": 38,
                "base_stats.SPD": 88,
                "base_stats.SPE": 67,
            },
        )
        df = add_move(df, pokemon, {"level": 33, "move": "iron head"})
        df = add_move(df, pokemon, {"level": 33, "move": "rock slide"})
        df = add_move(df, pokemon, {"level": 33, "move": "crunch"})
        # Umbreon
        pokemon = "Umbreon"
        df = set_pokemon(
            df,
            pokemon,
            ability="Shed Skin",
            stats={
                "base_stats.HP": 95,
                "base_stats.ATK": 30,
                "base_stats.DEF": 110,
                "base_stats.SPA": 100,
                "base_stats.SPD": 130,
                "base_stats.SPE": 60,
            },
        )
        df = add_move(df, pokemon, {"level": 36, "move": "recover"})
        df = add_move(df, pokemon, {"level": 36, "move": "psyshock"})
        df = add_move(df, pokemon, {"level": 38, "move": "sludge bomb"})
        df = add_move(df, pokemon, {"level": 42, "move": "calm mind"})
        # Espeon
        pokemon = "Espeon"
        df = set_pokemon(
            df,
            pokemon,
            ability="Magic Bounce",
            stats={
                "base_stats.HP": 95,
                "base_stats.ATK": 30,
                "base_stats.DEF": 75,
                "base_stats.SPA": 130,
                "base_stats.SPD": 85,
                "base_stats.SPE": 110,
            },
        )
        df = add_move(df, pokemon, {"level": 36, "move": "recover"})
        df = add_move(df, pokemon, {"level": 36, "move": "psyshock"})
        df = add_move(df, pokemon, {"level": 38, "move": "shadow ball"})
        df = add_move(df, pokemon, {"level": 42, "move": "calm mind"})
        # Mismagius
        pokemon = "Mismagius"
        df = set_pokemon(
            df,
            pokemon,
            types=("Ghost", "Fairy"),
            stats={
                "base_stats.HP": 80,
                "base_stats.ATK": 35,
                "base_stats.DEF": 80,
                "base_stats.SPA": 105,
                "base_stats.SPD": 105,
                "base_stats.SPE": 105,
            },
        )
        df = add_move(df, pokemon, move=[{"level": 1, "move": "moonblast"}])
        # Houndoom
        pokemon = "Houndoom"
        df = set_pokemon(
            df,
            pokemon,
            ability="Flash Fire",
            stats={
                "base_stats.HP": 90,
                "base_stats.ATK": 70,
                "base_stats.DEF": 80,
                "base_stats.SPA": 130,
                "base_stats.SPD": 90,
                "base_stats.SPE": 95,
            },
        )
        df = add_move(df, pokemon, move=[{"level": 1, "move": "blast burn"}])
        df = add_move(df, pokemon, {"level": 38, "move": "sludge bomb"})
        # Slowking
        pokemon = "Slowking"
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
        df = add_move(df, pokemon, {"level": 1, "move": "freeze-dry"})
        df = add_move(df, pokemon, {"level": 1, "move": "eerie spell"})
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
                "base_stats.DEF": 140,
                "base_stats.SPA": 61,
                "base_stats.SPD": 110,
                "base_stats.SPE": 75,
            },
        )
        df = add_move(df, pokemon, {"level": 38, "move": "stone axe"})
        df = add_move(df, pokemon, {"level": 38, "move": "fire punch"})
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
