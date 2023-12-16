__all__ = [
    "set_pokemon",
    "set_type",
    "set_stats",
    "set_ability",
    "add_move_raw",
    "add_move",
]

from loguru import logger
from typing import Union, Sequence, Any, List, Dict, Tuple
import pandas as pd

from skypy.const.abilities import ABILITIES
from skypy.const.types import TYPES
from skypy.const.schema import STATS_COLUMNS
from skypy.const.waza import MOVES
from .getters import (
    get_pokemon,
    get_pokemon_loc,
    get_stats_from_pkmn,
    get_learnset,
    get_learnset_raw,
    LVLUP_MOVE_TYPE,
)


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
    _check_moves_are_there(move, learnset_raw)
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
    loc = get_pokemon_loc(df, pokemon)
    pkmn = get_pokemon(df, pokemon).copy()
    learnset_raw = add_move_raw(df, pokemon, move, readable=False)
    _check_moves_are_there(move, learnset_raw)
    levelup_moves = pkmn["levelup_moves"]
    logger.trace(f"pkmn ({levelup_moves.shape}): {levelup_moves.values}")
    levelup_moves.at[int(levelup_moves.index.item())] = learnset_raw  # type: ignore
    logger.trace(f"pkmn ({levelup_moves.shape}): {levelup_moves.values}")
    pkmn["levelup_moves"] = levelup_moves
    df.loc[loc] = pkmn
    return df
