__all__ = [
    "get_pokemon_loc",
    "get_pokemon",
    "resume_pokemon",
    "resume_waza",
    "get_stats_from_pkmn",
    "get_stats",
    "get_type",
    "get_ability",
    "get_learnset_raw",
    "get_learnset",
    "get_waza",
    "get_pkmn_id",
    "get_evo_data",
]

from loguru import logger
from typing import Union, Sequence, Any, List, Dict, Tuple
import pandas as pd
from itertools import compress

from skypy.const.pkmn import POKEMON
from skypy.const.abilities import ABILITIES
from skypy.const.types import TYPES
from skypy.const.schema import STATS_COLUMNS
from skypy.const.waza import MOVES


LVLUP_MOVE_TYPE = Dict[str, Union[int, str]]


def get_evo_data(df: pd.DataFrame, pokemon: str) -> List[Dict[str, int]]:
    """Get evo data."""
    pkmn = get_pokemon(df, pokemon)
    evo_data: List[Dict[str, int]] = pkmn["evo_data"].values[0]
    return evo_data


def get_pokemon_loc(df: pd.DataFrame, name: str) -> List[bool]:
    """Get data for specified Pokemon."""
    tmp = df.copy()
    logger.trace(f"{tmp.shape}|len of POKEMON={len(POKEMON)}")
    tmp["name"] = [n.lower() for n in POKEMON]
    return (tmp["name"] == name.lower()).to_list()


def get_pokemon(
    df: pd.DataFrame,
    name: str,
) -> pd.DataFrame:
    """Get dat for specified Pokemon."""
    loc = get_pokemon_loc(df, name)
    pkmn = df.loc[loc]
    return pkmn


def get_waza(
    df: pd.DataFrame,
    name: str,
    return_idx: bool = False,
) -> Union[pd.DataFrame, Tuple[pd.DataFrame, List[bool]]]:
    """Get Waza."""
    tmp = df.copy()
    tmp["name"] = [n.lower() for n in MOVES]
    idx = (tmp["name"] == name.lower()).to_list()
    waza = df.loc[idx, :]
    if return_idx:
        return waza, idx
    return waza


def resume_waza(
    df: pd.DataFrame,
    name: str,
) -> pd.DataFrame:
    """Resume Waza."""
    waza = get_waza(df, name)
    assert isinstance(waza, pd.DataFrame)
    waza["name"] = name.lower()
    waza["type"] = waza["type"].apply(lambda x: TYPES[x]).astype("string")
    return waza


def get_pkmn_id(
    df: pd.DataFrame,
    name: str,
) -> int:
    """Get Pokemon's ID."""
    loc = get_pokemon_loc(df, name)
    ID = list(compress(range(len(loc)), loc))[0]
    return ID


def resume_pokemon(
    df: pd.DataFrame,
    name: str,
) -> Dict[str, Any]:
    """Resume Pokemon."""
    ID = get_pkmn_id(df, name)
    types = get_type(df, name)
    stats = get_stats(df, name)
    abilities = get_ability(df, name)
    p = is_present(df, name)
    resume = {"is_present": p, "ID": ID, "name": POKEMON[ID], "type": types, "abilities": abilities}
    resume.update(stats)  # type: ignore
    return resume


def is_present(
    df: pd.DataFrame,
    name: str,
) -> bool:
    """Is it present?"""
    pkmn = get_pokemon(df, name)
    is_p: pd.Series = pkmn["is_present"]
    return bool(is_p.values[0])


def get_stats_from_pkmn(pkmn: pd.DataFrame) -> Dict[str, int]:
    """Get Pokemon's stats."""
    stats_raw: List[int] = pkmn[STATS_COLUMNS].values.tolist()[0]
    stats = {}
    for key, val in zip(STATS_COLUMNS, stats_raw):
        stats[key] = val
    stats["base_stats.TOT"] = sum(stats_raw)
    return stats


def get_stats(
    df: pd.DataFrame,
    name: str,
) -> Dict[str, int]:
    """Get Pokemon's stats."""
    pkmn = get_pokemon(df, name)
    stats = get_stats_from_pkmn(pkmn)
    return stats


def get_type(
    df: pd.DataFrame,
    name: str,
) -> List[str]:
    """Get Pokemon's type(s)."""
    row = get_pokemon(df, name)
    logger.debug(row[["type_1", "type_2"]])
    types_raw = row[["type_1", "type_2"]].values.tolist()[0]
    logger.debug(f"types_raw: {types_raw}")
    types = []
    for i in types_raw:
        _type = TYPES[i]
        types.append(_type)
    return types


def get_ability(df: pd.DataFrame, name: str) -> List[str]:
    """Get Pokemon's abilities."""
    pkmn = get_pokemon(df, name)
    abilities = pkmn[["ability_1", "ability_2", "ability_hidden"]].values.tolist()[0]
    return [ABILITIES[int(i)] for i in abilities]


def get_learnset_raw(
    df: pd.DataFrame,
    name: str,
    readable: bool = False,
) -> List[LVLUP_MOVE_TYPE]:
    """Get Pokemon's learnset (raw)."""
    pkmn = get_pokemon(df, name)
    return get_learnset_raw_pkmn(pkmn, readable)


def get_learnset_raw_pkmn(
    pkmn: pd.DataFrame,
    readable: bool = False,
) -> List[LVLUP_MOVE_TYPE]:
    """Get Pokemon's learnset (raw)."""
    levelup_moves_raw: List[Dict[str, int]] = pkmn["levelup_moves"].values[0]
    # 'move': 403, 'level': 253
    levelup_moves: List[LVLUP_MOVE_TYPE] = []
    for lvl_up_m in levelup_moves_raw:
        move_id = lvl_up_m["move"]
        add_move: LVLUP_MOVE_TYPE = dict(
            move=MOVES[move_id] if readable else move_id,
            level=lvl_up_m["level"],
        )
        levelup_moves.append(add_move)
    return levelup_moves


def get_learnset(
    df: pd.DataFrame,
    name: str,
    readable: bool = False,
) -> pd.DataFrame:
    """Get Pokemon's learnset."""
    levelup_moves = get_learnset_raw(df, name, readable)
    learnset = pd.DataFrame(levelup_moves).sort_values("level").reset_index(drop=True)
    return learnset
