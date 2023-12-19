from typing import Any
import pandas as pd

from skypy.ops import add_move, read_data, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON


def mons(df: pd.DataFrame = None, **kwargs: Any) -> pd.DataFrame:
    """Mons."""
    if df is None:
        df = read_data(**kwargs)
    # Venusaur
    pokemon = "Venusaur"
    df = set_pokemon(
        df,
        pokemon,
        ability=["thick fat", "thick fat", "thick fat"],
        stats={
            "base_stats.HP": 90,
            "base_stats.ATK": 72,
            "base_stats.DEF": 93,
            "base_stats.SPA": 100,
            "base_stats.SPD": 100,
            "base_stats.SPE": 80,
        },
    )
    # Blastoise
    pokemon = "Blastoise"
    df = set_pokemon(
        df,
        pokemon,
        ability=["mega launcher", "mega launcher", "mega launcher"],
        stats={
            "base_stats.HP": 79,
            "base_stats.ATK": 70,
            "base_stats.DEF": 103,
            "base_stats.SPA": 100,
            "base_stats.SPD": 105,
            "base_stats.SPE": 78,
        },
    )
    df = add_move(df, pokemon, move=[{"level": 36, "move": "ice beam"}])
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
                    "base_stats.DEF": 55,
                    "base_stats.SPA": 90,
                    "base_stats.SPD": 50,
                    "base_stats.SPE": 100,
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
    df = add_move(df, "articuno", {"level": 36, "move": "water pulse"})
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
    # Braviary
    df = add_evo(df, "Rufflet", level=30, into="Hisuian Braviary")
    # Wyrdeer
    df = add_evo(df, "Stantler", level=40, into="Wyrdeer")
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
            "base_stats.DEF": 79,
            "base_stats.SPA": 70,
            "base_stats.SPD": 79,
            "base_stats.SPE": 95,
        },
    )
    df = add_move(df, pokemon, {"level": 38, "move": "crunch"})
    df = add_move(df, pokemon, {"level": 38, "move": "thunder fang"})
    df = add_move(df, pokemon, {"level": 38, "move": "ice fang"})
    df = add_move(df, pokemon, {"level": 38, "move": "fire fang"})
    df = add_move(df, pokemon, {"level": 38, "move": "iron tail"})
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
    # Dialga
    for pokemon in POKEMON:
        if "dialga" in pokemon.lower():
            df = set_pokemon(
                df,
                pokemon,
                ability="Filter",
                stats={
                    "base_stats.HP": 200,
                    "base_stats.ATK": 90,
                    "base_stats.DEF": 130,
                    "base_stats.SPA": 150,
                    "base_stats.SPD": 120,
                    "base_stats.SPE": 90,
                },
            )
    # Palkia
    for pokemon in POKEMON:
        if "palkia" in pokemon.lower():
            df = set_pokemon(
                df,
                pokemon,
                ability="Filter",
                stats={
                    "base_stats.HP": 190,
                    "base_stats.ATK": 90,
                    "base_stats.DEF": 100,
                    "base_stats.SPA": 150,
                    "base_stats.SPD": 130,
                    "base_stats.SPE": 120,
                },
            )
    # Giratina
    df = set_pokemon(
        df,
        "Giratina",
        ability="Filter",
        stats={
            "base_stats.HP": 250,
            "base_stats.ATK": 100,
            "base_stats.DEF": 120,
            "base_stats.SPA": 100,
            "base_stats.SPD": 120,
            "base_stats.SPE": 90,
        },
    )
    df = set_pokemon(
        df,
        "Origin Giratina",
        stats={
            "base_stats.HP": 250,
            "base_stats.ATK": 120,
            "base_stats.DEF": 100,
            "base_stats.SPA": 120,
            "base_stats.SPD": 100,
            "base_stats.SPE": 90,
        },
    )
    # Arceus
    for pokemon in POKEMON:
        if "arceus" in pokemon.lower():
            df = set_pokemon(
                df,
                pokemon,
                stats={
                    "base_stats.HP": 220,
                    "base_stats.ATK": 220,
                    "base_stats.DEF": 220,
                    "base_stats.SPA": 220,
                    "base_stats.SPD": 220,
                    "base_stats.SPE": 220,
                },
            )
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
    # Zoroark
    pokemon = "Zoroark"
    df = set_pokemon(
        df,
        pokemon,
        stats={
            "base_stats.HP": 75,
            "base_stats.ATK": 60,
            "base_stats.DEF": 65,
            "base_stats.SPA": 130,
            "base_stats.SPD": 65,
            "base_stats.SPE": 115,
        },
    )
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
        ],
    )
    # Bisharp
    df = add_evo(df, "Bisharp", level=50, into="Kingambit")
    # Hydreigon
    df = set_pokemon(df, "deino", ability="shed skin")
    df = add_evo(df, "deino", level=30, into="Zweilous")
    df = set_pokemon(df, "Zweilous", ability="shed skin")
    df = add_evo(df, "Zweilous", level=50, into="Hydreigon")
    df = set_pokemon(
        df,
        "Hydreigon",
        stats={
            "base_stats.HP": 92,
            "base_stats.ATK": 80,
            "base_stats.DEF": 90,
            "base_stats.SPA": 130,
            "base_stats.SPD": 90,
            "base_stats.SPE": 118,
        },
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
    # Goodra
    df = add_evo(df, "Goomy", level=25, into="Hisuian Sliggoo")
    pokemon = "Goodra"
    df = set_pokemon(
        df,
        pokemon,
        ability=["Sap Sipper", "Hydration", "Gooey"],
        stats={
            "base_stats.HP": 90,
            "base_stats.ATK": 70,
            "base_stats.DEF": 100,
            "base_stats.SPA": 110,
            "base_stats.SPD": 150,
            "base_stats.SPE": 80,
        },
    )
    df = add_move(df, pokemon, {"level": 36, "move": "sludge bomb"})
    df = add_move(df, pokemon, {"level": 33, "move": "ice beam"})
    df = add_move(df, pokemon, {"level": 33, "move": "water pulse"})
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
    # Lycanroc-1
    df = set_pokemon(
        df,
        "Lycanroc-1",
        types=("rock", "ghost"),
        ability=("No Guard", "No Guard", "No Guard"),
        stats={
            "base_stats.HP": 85,
            "base_stats.ATK": 115,
            "base_stats.DEF": 75,
            "base_stats.SPA": 55,
            "base_stats.SPD": 75,
            "base_stats.SPE": 82,
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
    # Urshifu
    df = add_evo(df, "Kubfu", level=42, into="Urshifu")
    df = add_move(df, "Urshifu", {"level": 1, "move": "wicked blow"})
    df = add_move(df, "Urshifu", {"level": 1, "move": "iron head"})
    df = add_move(df, "Urshifu", {"level": 1, "move": "drain punch"})
    df = add_move(df, "Urshifu", {"level": 1, "move": "bulk up"})
    # Sneasler
    df = add_evo(df, "Hisuian Sneasel", level=42, into="Sneasler")
    pokemon = "Sneasler"
    df = set_pokemon(
        df,
        pokemon,
        ability="Poison Touch",
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
    # Garganacl
    df = set_pokemon(
        df,
        "Garganacl",
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
            "base_stats.HP": 113,
            "base_stats.ATK": 55,
            "base_stats.DEF": 80,
            "base_stats.SPA": 130,
            "base_stats.SPD": 81,
            "base_stats.SPE": 96,
        },
    )
    # Exit
    return df
