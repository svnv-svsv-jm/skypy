from skypy.ops import (
    get_pokemon,
    add_move,
    get_learnset,
    read_data,
    resume_pokemon,
    write_df_to_json,
    set_pokemon,
    read_waza,
    resume_waza,
    write_waza_to_json,
    get_waza,
    set_waza,
)


def waza() -> None:
    """Waza."""
    waza_df = read_waza()
    waza_df = set_waza(waza_df, waza="dark void", accuracy=100)
    waza_df = set_waza(waza_df, waza="diamond storm", accuracy=100)
    waza_df = set_waza(waza_df, waza="rock slide", accuracy=100)
    waza_df = set_waza(waza_df, waza="stone axe", accuracy=100)
    waza_df = set_waza(waza_df, waza="Ceaseless Edge", power=75, accuracy=100)
    waza_df = set_waza(waza_df, waza="infernal parade", power=80)
    waza_df = set_waza(
        waza_df,
        waza="Judgment",
        power=180,
        accuracy=101,
        inflicts="confusion",
        inflict_chance=25,
        edits={"flinch": 30},
    )
    waza_df = set_waza(waza_df, waza="meteor mash", accuracy=100)
    waza_df = set_waza(waza_df, waza="zen headbutt", accuracy=100)
    waza_df = set_waza(waza_df, waza="play rough", accuracy=100)
    waza_df = set_waza(waza_df, waza="rock tomb", accuracy=100)
    waza_df = set_waza(waza_df, waza="air slash", accuracy=100)
    waza_df = set_waza(waza_df, waza="psystrike", power=120)
    waza_df = set_waza(waza_df, waza="shadow punch", power=75)
    waza_df = set_waza(waza_df, waza="water pulse", power=75)
    waza_df = set_waza(waza_df, waza="gigaton hammer", edits={"flag_cant_use_twice": False})
    waza_df = set_waza(waza_df, waza="night daze", accuracy=100)
    waza_df = set_waza(waza_df, waza="iron tail", accuracy=100)
    write_waza_to_json(waza_df)
