from skypy.ops import (
    get_pokemon,
    add_move,
    get_learnset,
    read_data,
    resume_pokemon,
    write_df_to_json,
    set_pokemon,
    add_evo,
)
from skypy.const.pkmn import POKEMON


def mons() -> None:
    """Mons."""
    df = read_data()
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
    for pkmn in POKEMON:
        if "pikachu-" in pkmn.lower():
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
    pokemon = "Hisuian Typhlosion"
    df = set_pokemon(
        df,
        pokemon,
        ability="flash fire",
        stats={
            "base_stats.HP": 73,
            "base_stats.ATK": 78,
            "base_stats.DEF": 84,
            "base_stats.SPA": 120,
            "base_stats.SPD": 85,
            "base_stats.SPE": 95,
        },
    )
    df = add_move(df, "Hisuian Typhlosion", {"level": 25, "move": "earth power"})
    # Feraligatr
    pokemon = "Feraligatr"
    df = set_pokemon(
        df,
        pokemon,
        ability=["Tough Claws", "Tough Claws", "Sheer Force"],
        stats={
            "base_stats.HP": 90,
            "base_stats.ATK": 105,
            "base_stats.DEF": 107,
            "base_stats.SPA": 70,
            "base_stats.SPD": 85,
            "base_stats.SPE": 78,
        },
    )
    df = add_move(df, "Feraligatr", {"level": 36, "move": "ice punch"})
    df = add_move(df, "Feraligatr", {"level": 25, "move": "waterfall"})
    df = add_move(df, "Feraligatr", {"level": 28, "move": "liquidation"})
    # Meganium
    df = set_pokemon(
        df,
        "Meganium",
        types=("grass", "fairy"),
        ability=["Grassy Surge", "Grassy Surge", "Magic Bounce"],
        stats={
            "base_stats.HP": 95,
            "base_stats.ATK": 62,
            "base_stats.DEF": 100,
            "base_stats.SPA": 103,
            "base_stats.SPD": 100,
            "base_stats.SPE": 80,
        },
    )
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
    # Tyranitar
    df = set_pokemon(
        df,
        "Tyranitar",
        ability="Sand Stream",
        stats={
            "base_stats.HP": 130,
            "base_stats.ATK": 134,
            "base_stats.DEF": 150,
            "base_stats.SPA": 95,
            "base_stats.SPD": 120,
            "base_stats.SPE": 71,
        },
    )
    df = add_move(df, "Tyranitar", {"level": 38, "move": "stone axe"})
    df = add_move(df, "Tyranitar", {"level": 40, "move": "dragon dance"})
    # Metagross
    df = set_pokemon(df, "Beldum", ability="Levitate")
    df = add_move(df, "Beldum", {"level": 1, "move": "iron head"})
    df = add_move(df, "Beldum", {"level": 1, "move": "zen headbutt"})
    df = set_pokemon(df, "Metang", ability="Levitate")
    df = set_pokemon(
        df,
        "Metagross",
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
    df = add_move(df, "Metagross", {"level": 38, "move": "zen headbutt"})
    df = add_move(df, "Metagross", {"level": 40, "move": "recover"})
    df = add_move(df, "Metagross", {"level": 42, "move": "bulk up"})
    df = add_move(df, "Metagross", {"level": 41, "move": "drain punch"})
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
    # Darkrai
    pokemon = "Darkrai"
    df = set_pokemon(
        df,
        pokemon,
        types=("dark", "ghost"),
        stats={
            "base_stats.HP": 72,
            "base_stats.ATK": 50,
            "base_stats.DEF": 78,
            "base_stats.SPA": 123,
            "base_stats.SPD": 85,
            "base_stats.SPE": 132,
        },
    )
    df = add_move(df, "Darkrai", {"level": 22, "move": "shadow ball"})
    df = add_move(df, "Darkrai", {"level": 40, "move": "psyshock"})
    df = add_move(df, "Darkrai", {"level": 44, "move": "mystical fire"})
    # Dialga
    for pkmn in POKEMON:
        if "Dialga" in pkmn.lower():
            df = set_pokemon(
                df,
                pokemon,
                stats={
                    "base_stats.HP": 200,
                    "base_stats.ATK": 100,
                    "base_stats.DEF": 120,
                    "base_stats.SPA": 150,
                    "base_stats.SPD": 120,
                    "base_stats.SPE": 90,
                },
            )
    # Palkia
    for pkmn in POKEMON:
        if "Palkia" in pkmn.lower():
            df = set_pokemon(
                df,
                pokemon,
                stats={
                    "base_stats.HP": 190,
                    "base_stats.ATK": 100,
                    "base_stats.DEF": 100,
                    "base_stats.SPA": 150,
                    "base_stats.SPD": 120,
                    "base_stats.SPE": 120,
                },
            )
    # Giratina
    df = set_pokemon(
        df,
        "Giratina",
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
        "origin Giratina",
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
    for pkmn in POKEMON:
        if "arceus" in pkmn.lower():
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
    df = add_move(
        df,
        "Sneasler",
        [
            {"level": 36, "move": "iron head"},
            {"level": 37, "move": "bulk up"},
            {"level": 42, "move": "drain punch"},
        ],
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
    write_df_to_json(df)
