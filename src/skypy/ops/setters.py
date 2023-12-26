__all__ = [
    "set_pokemon",
    "set_type",
    "set_stats",
    "set_ability",
    "add_move_raw",
    "add_move",
    "set_waza",
    "add_evo",
]

from loguru import logger
from typing import Union, Sequence, Any, List, Dict, Tuple
import pandas as pd

from skypy.const.abilities import ABILITIES
from skypy.const.types import TYPES
from skypy.const.schema import STATS_COLUMNS
from skypy.const.waza import MOVES, INFLICT
from .getters import (
    get_pokemon,
    get_pokemon_loc,
    get_stats_from_pkmn,
    get_learnset_raw,
    LVLUP_MOVE_TYPE,
    get_waza,
    get_pkmn_id,
    get_evo_data,
)

EVO_DATA = {
    "level": 16,
    "condition": 4,
    "parameter": 0,
    "reserved3": 0,
    "reserved4": 0,
    "reserved5": 0,
    "species": 8,
    "form": 0,
}


def add_evo(
    df: pd.DataFrame,
    pokemon: str,
    level: int,
    into: str,
) -> pd.DataFrame:
    """Adds evolution method."""
    pkmn = get_pokemon(df, pokemon)
    evo_data = get_evo_data(df, pokemon)
    logger.trace(evo_data)
    new_evo_data = EVO_DATA.copy()
    new_evo_data["level"] = level
    into = into.strip().lower()
    if "hisuian" in into:
        t = into.replace("hisuian", "")
        ID = get_pkmn_id(df, t.strip().lower())
        new_evo_data["form"] = 1
    else:
        ID = get_pkmn_id(df, into)
    new_evo_data["species"] = ID
    evo_data.append(new_evo_data)
    logger.trace(evo_data)
    # Set
    pkmn["evo_data"].values[0] = evo_data
    logger.trace(pkmn["evo_data"])
    pkmn_idx = get_pokemon_loc(df, pokemon)
    df.loc[pkmn_idx, :] = pkmn
    return df


def set_waza(
    df: pd.DataFrame,
    waza: str,
    waza_type: str = None,
    accuracy: int = None,
    power: int = None,
    inflicts: str = None,
    inflict_chance: int = None,
    edits: Dict[str, Any] = None,
) -> pd.DataFrame:
    """Change waza's data.

    Example of waza's data ("Drill Run"):

    ```json
        'move_id': {529: 'WAZA_DORIRURAINAA'},
        'can_use_move': {529: True},
        'type': {529: 'Ground'},
        'quality': {529: 0},
        'category': {529: 1},
        'power': {529: 80},
        'accuracy': {529: 100},
        'pp': {529: 10},
        'priority': {529: 0},
        'hit_max': {529: 0},
        'hit_min': {529: 0},
        'crit_stage': {529: 1},
        'flinch': {529: 0},
        'effect_sequence': {529: 43},
        'recoil': {529: 0},
        'raw_healing': {529: 0},
        'raw_target': {529: 0},
        'affinity': {529: 'Attack'},
        'flag_makes_contact': {529: True},
        'flag_charge': {529: False},
        'flag_rechargeg': {529: False},
        'flag_protect': {529: True},
        'flag_reflectable': {529: False},
        'flag_snatch': {529: False},
        'flag_mirror': {529: True},
        'flag_punch': {529: False},
        'flag_sound': {529: False},
        'flag_dance': {529: False},
        'flag_gravity': {529: False},
        'flag_defrost': {529: False},
        'flag_distance_triple': {529: False},
        'flag_heal': {529: False},
        'flag_ignore_substitute': {529: False},
        'flag_fail_sky_battle': {529: False},
        'flag_animate_ally': {529: False},
        'flag_metronome': {529: True},
        'flag_fail_encore': {529: False},
        'flag_fail_me_first': {529: False},
        'flag_future_attack': {529: False},
        'flag_pressure': {529: False},
        'flag_combo': {529: False},
        'flag_no_sleep_talk': {529: False},
        'flag_no_assist': {529: False},
        'flag_fail_copy_cat': {529: False},
        'flag_fail_mimic': {529: False},
        'flag_fail_instruct': {529: False},
        'flag_powder': {529: False},
        'flag_bite': {529: False},
        'flag_bullet': {529: False},
        'flag_no_multi_hit': {529: False},
        'flag_no_effectiveness': {529: False},
        'flag_sheer_force': {529: False},
        'flag_slicing': {529: False},
        'flag_wind': {529: False},
        'unknown56': {529: False},
        'unknown57': {529: False},
        'unknown58': {529: False},
        'unknown59': {529: False},
        'unknown60': {529: False},
        'unused61': {529: False},
        'unused62': {529: False},
        'unused63': {529: False},
        'unused64': {529: False},
        'unused65': {529: False},
        'unused66': {529: False},
        'unused67': {529: False},
        'unused68': {529: False},
        'unused69': {529: False},
        'unused70': {529: False},
        'flag_cant_use_twice': {529: False},
        'inflict.value': {529: 0},
        'inflict.chance': {529: 0},
        'inflict.turn1': {529: 0},
        'inflict.turn2': {529: 0},
        'inflict.turn3': {529: 0},
        'stat_amps.fstat1': {529: 0},
        'stat_amps.fstat2': {529: 0},
        'stat_amps.fstat3': {529: 0},
        'stat_amps.fstat1_stage': {529: 0},
        'stat_amps.fstat2_state': {529: 0},
        'stat_amps.fstat3_stage': {529: 0},
        'stat_amps.fstat1_percent': {529: 0},
        'stat_amps.fstat2_percent': {529: 0},
        'stat_amps.fstat3_percent': {529: 0}
    ```
    """
    waza_df, waza_idx = get_waza(df, waza.lower(), return_idx=True)
    assert isinstance(waza_df, pd.DataFrame)
    logger.trace(waza_df)
    # Type
    if waza_type is not None:
        for i, val in TYPES.items():
            if waza_type.lower() == val.lower():
                move_id = i
                break
        logger.trace(waza_df["type"])
        waza_df["type"] = move_id
        logger.trace(waza_df["type"])
        if isinstance(waza_idx, int):
            tmp = [False] * df.shape[0]
            tmp[waza_idx] = True
            waza_idx = tmp
    # Accuracy
    if accuracy is not None:
        waza_df["accuracy"] = accuracy
    # Power
    if power is not None:
        waza_df["power"] = power
    # Status
    if inflicts is not None:
        waza_df["inflict.value"] = INFLICT[inflicts.lower()]
        if inflict_chance is not None:
            waza_df["inflict.chance"] = inflict_chance
    # Free form: all the others
    if edits is not None:
        for key, val in edits.items():
            waza_df[key] = val
    # Set
    df.loc[waza_idx, :] = waza_df  # type: ignore
    return df


def set_pokemon(
    df: pd.DataFrame,
    name: str,
    ability: Union[str, Sequence[str]] = None,
    ability_index: Union[int, Sequence[int]] = None,
    types: Tuple[str, str] = None,
    stats: Union[Sequence[int], Dict[str, int]] = None,
    add_to_stats: Union[Sequence[int], Dict[str, int]] = None,
) -> pd.DataFrame:
    """Set attributes for a Pokemon."""
    logger.debug(f"Setting attributes for {name.upper()}")
    # Get data
    pkmn = get_pokemon(df, name)
    # Change stats
    if stats is not None or add_to_stats is not None:
        pkmn = set_stats(pkmn, stats, add_to_stats)
        loc = get_pokemon_loc(df, name)
        df.loc[loc] = pkmn
    # Change ability
    if ability is not None:
        pkmn = set_ability(pkmn, ability, index=ability_index)
        loc = get_pokemon_loc(df, name)
        df.loc[loc] = pkmn
    # Change types
    if types is not None:
        pkmn = set_type(pkmn, types)
        loc = get_pokemon_loc(df, name)
        df.loc[loc] = pkmn
    return df


def set_type(
    pkmn: pd.DataFrame,
    types: Tuple[str, str],
) -> pd.DataFrame:
    """Set Pokemon's type(s)."""
    # Get ID of Types
    type_names = [x.lower() for x in list(TYPES.values())]
    type_1_id = type_names.index(types[0].lower())
    type_2_id = type_names.index(types[1].lower())
    pkmn["type_1"] = int(type_1_id)
    pkmn["type_2"] = int(type_2_id)
    return pkmn


def set_stats(
    pkmn: pd.DataFrame,
    stats: Union[Sequence[int], Dict[str, int]] = None,
    add_to_stats: Union[Sequence[int], Dict[str, int]] = None,
) -> pd.DataFrame:
    """Set Pokemon's stats."""
    logger.debug("Setting stats...")
    if add_to_stats is not None:
        stats = get_stats_from_pkmn(pkmn)
        stats = list(stats.values())[0:6]
        if isinstance(add_to_stats, dict):
            add_to_stats = list(add_to_stats.values())
            add_to_stats = add_to_stats[0:6]
        for i, val in enumerate(add_to_stats):
            stats[i] = stats[i] + val
    assert stats is not None
    # Make sure we have a sequence of 6 int's
    if isinstance(stats, dict):
        stats_list = []
        for k in STATS_COLUMNS:
            stats_list.append(stats[k])
    else:
        stats_list = stats  # type: ignore
    assert len(stats_list) == 6, f"{len(stats_list)} != 6"
    # Now set the stats!
    for i, stat in enumerate(stats_list):
        pkmn[STATS_COLUMNS[i]] = stat
    return pkmn


def set_ability(
    pkmn: pd.DataFrame,
    ability: Union[str, Sequence[str]],
    index: Union[int, Sequence[int]] = None,
) -> pd.DataFrame:
    """Sets ability."""
    if isinstance(ability, (list, tuple)):
        for i, a in enumerate(ability):
            pkmn = set_ability(pkmn, a, index=i)
        return pkmn
    # Choose ability's index
    if index is None:
        index = [0, 1, 2]  # 1st, 2nd and hidden
    elif isinstance(index, (int, float)):
        index = [int(index)]
    else:
        index = [int(x) for x in index]
    # Create list of abilities and get ID
    abilities = [n.lower() for n in ABILITIES]
    assert isinstance(ability, str)
    i = abilities.index(ability.lower())
    # Set them
    for idx in index:
        if idx == 0:
            pkmn["ability_1"] = int(i)
        elif idx == 1:
            pkmn["ability_2"] = int(i)
        else:
            pkmn["ability_hidden"] = int(i)
    return pkmn


def add_move_raw(
    df: pd.DataFrame,
    pokemon: str,
    move: Union[LVLUP_MOVE_TYPE, Sequence[LVLUP_MOVE_TYPE]],
    readable: bool = False,
) -> Sequence[LVLUP_MOVE_TYPE]:
    """Add move to Pokemon's learnset (raw)."""
    learnset_raw = get_learnset_raw(df, pokemon, readable)
    if isinstance(move, dict):
        move = [move]
    move_db = [m.lower() for m in MOVES]
    for m in move:
        lvl = m["level"]
        move_ = m["move"]
        if isinstance(move_, str):
            move_name = move_
            move_id = move_db.index(move_name.lower())
        else:
            move_id = move_
            move_name = move_db[move_id]
        to_add: LVLUP_MOVE_TYPE = {"level": lvl, "move": move_name if readable else move_id}
        learnset_raw.append(to_add)
        _check_moves_are_there(m, learnset_raw)
    return learnset_raw


def _check_moves_are_there(
    move_to_add: Union[LVLUP_MOVE_TYPE, Sequence[LVLUP_MOVE_TYPE]],
    learnset_new_raw: Sequence[LVLUP_MOVE_TYPE],
) -> None:
    """Raises an error if moves that were to be added are not found."""
    if isinstance(move_to_add, dict):
        move_to_add = [move_to_add]
    for i, m in enumerate(move_to_add):
        added_move = learnset_new_raw[-(1 - i)]
        for key, val in added_move.items():
            ex = m[key]
            if isinstance(ex, str):
                ex = ex.upper()
            else:
                ex = MOVES[ex].upper()
            got = val
            if isinstance(got, str):
                got = got.upper()
            else:
                got = MOVES[got].upper()
            assert ex == got, f"expected {ex} but got {got}."


def add_move(
    df: pd.DataFrame,
    pokemon: str,
    move: Union[LVLUP_MOVE_TYPE, Sequence[LVLUP_MOVE_TYPE]],
) -> pd.DataFrame:
    """Add move to Pokemon's learnset (raw)."""
    logger.debug(f"Adding {move} to {pokemon.upper()}'s learnset...")
    loc = get_pokemon_loc(df, pokemon)
    pkmn = get_pokemon(df, pokemon).copy()
    learnset_raw = add_move_raw(df, pokemon, move, readable=False)
    levelup_moves = pkmn["levelup_moves"]
    logger.trace(f"pkmn ({levelup_moves.shape}): {levelup_moves.values}")
    levelup_moves.at[int(levelup_moves.index.item())] = learnset_raw  # type: ignore
    logger.trace(f"pkmn ({levelup_moves.shape}): {levelup_moves.values}")
    pkmn["levelup_moves"] = levelup_moves
    df.loc[loc] = pkmn
    return df
