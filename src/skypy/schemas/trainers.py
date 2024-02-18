# pylint: disable=no-self-argument
from __future__ import annotations

__all__ = ["TrainerSchema", "TrainerPokemonSchema"]

import typing as ty
from pydantic import validator

from skypy.ops.core import read_devid, read_itemid, read_waza, read_trainer
from skypy.const import BALLIDS, GEMTYPE
from ._base import BaseSchema

ITEMID: ty.List[str] = read_itemid()["devName"].to_list()
SEIKAIKU = [
    "DEFAULT",
    "GANBARIYA",
    "HIKAEME",
    "IJIPPARI",
    "YOUKI",
    "OKUBYOU",
    "WANPAKU",
    "ODAYAKA",
    "SINNTYOU",
    "ZUBUTOI",
    "NAMAIKI",
]
SEX = ["DEFAULT", "MALE", "FEMALE"]
TALENT_TYPE = ["RANDOM", "VALUE"]
ABILITY = ["RANDOM_12", "SET_3", "SET_1", "SET_2"]
WAZAID: ty.List[str] = read_waza()["move_id"].to_list()
WAZATYPE = ["DEFAULT", "MANUAL"]
BATTLETYPES = ["_1vs1", "_2vs2"]
TRAINERNAMELABEL: ty.List[str] = read_trainer()["trNameLabel"].to_list()
TRAINERTYPE: ty.List[str] = read_trainer()["trainerType"].to_list()
TRAINERID: ty.List[str] = read_trainer()["trid"].to_list()


def validate_item_in_list(
    value: ty.Any, allowed: ty.List[ty.Any], default: ty.Any = None
) -> ty.Any:
    """Validate item is in list."""
    if value not in allowed:
        if default is None:
            raise ValueError(f"Invalid. Allowed are {allowed}")
        else:
            return default
    return value


class TrainerPokemonSchema(BaseSchema):
    """Schema for a trainer's Pokemon data."""

    ballId: str = BALLIDS[0]
    devId: str
    effortValue___agi: int = 0
    effortValue___atk: int = 0
    effortValue___def: int = 0
    effortValue___hp: int = 0
    effortValue___spAtk: int = 0
    effortValue___spDef: int = 0
    formId: int = 0
    gemType: str = GEMTYPE[0]
    item: str = ITEMID[0]
    level: int
    rareType: str = "DEFAULT"
    scaleType: str = "VALUE"
    scaleValue: int = 175
    seikaku: str = SEIKAIKU[0]
    sex: str = SEX[0]
    talentType: str = TALENT_TYPE[0]
    talentValue___agi: int = 0
    talentValue___atk: int = 0
    talentValue___def: int = 0
    talentValue___hp: int = 0
    talentValue___spAtk: int = 0
    talentValue___spDef: int = 0
    talentVnum: int = 20
    tokusei: str = ABILITY[0]
    waza1___pointUp: int = 0
    waza1___wazaId: str = WAZAID[0]
    waza2___pointUp: int = 0
    waza2___wazaId: str = WAZAID[0]
    waza3___pointUp: int = 0
    waza3___wazaId: str = WAZAID[0]
    waza4___pointUp: int = 0
    waza4___wazaId: str = WAZAID[0]
    wazaType: str = WAZATYPE[0]

    @validator("level")
    def _level(cls, value: int) -> int:
        """Make sure it is one of these items."""
        if value < 0 or value > 100:
            raise ValueError(f"Level must be between 1 and 100 but is {value}.")
        return value

    @validator("wazaType")
    def _wazaType(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, WAZATYPE, WAZATYPE[0])
        return value

    @validator("waza1___wazaId")
    def _waza1___wazaId(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, WAZAID, WAZAID[0])
        return value

    @validator("waza2___wazaId")
    def _waza2___wazaId(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, WAZAID, WAZAID[0])
        return value

    @validator("waza3___wazaId")
    def _waza3___wazaId(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, WAZAID, WAZAID[0])
        return value

    @validator("waza4___wazaId")
    def _waza4___wazaId(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, WAZAID, WAZAID[0])
        return value

    @validator("tokusei")
    def _tokusei(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, ABILITY, ABILITY[0])
        return value

    @validator("talentType")
    def _talentType(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, TALENT_TYPE, TALENT_TYPE[0])
        return value

    @validator("ballId")
    def _ballId(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, BALLIDS, BALLIDS[0])
        return value

    @validator("devId")
    def _devId(cls, value: str) -> str:
        """Make sure it is one of these items."""
        devid = read_devid()["devName"].to_list()
        value = validate_item_in_list(value, devid)
        return value

    @validator("gemType")
    def validate_gemType(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, GEMTYPE, GEMTYPE[0])
        return value

    @validator("item")
    def validate_item(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, ITEMID, ITEMID[0])
        return value

    @validator("rareType")
    def validate_rareType(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, ["NO_RARE", "DEFAULT"], "DEFAULT")
        return value

    @validator("scaleType")
    def validate_scaleType(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, ["VALUE", "XL"], "VALUE")
        return value

    @validator("seikaku")
    def validate_seikaku(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, SEIKAIKU, SEIKAIKU[0])
        return value

    @validator("sex")
    def validate_sex(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, SEX, SEX[0])
        return value


class TrainerSchema(BaseSchema):
    """Schema for Trainer data."""

    aiBasic: bool = True
    aiChange: bool = True
    aiDouble: bool = False
    aiExpert: bool = True
    aiHigh: bool = True
    aiItem: bool = True
    aiRaid: bool = False
    aiWeak: bool = False
    battleType: str = BATTLETYPES[0]
    changeGem: bool = False
    dataType: str = "NORMAL"  # ['NORMAL', 'WAZA']
    isStrong: bool = True
    moneyRate: int = 15
    popupLabelNormal1: str = ""
    popupLabelNormal2: str = ""
    popupLabelPinch1: str = ""
    popupLabelPinch2: str = ""
    trNameLabel: str = TRAINERNAMELABEL[0]
    trainerType: str = TRAINERTYPE[0]
    trid: str = TRAINERID[0]
    poke1: TrainerPokemonSchema = TrainerPokemonSchema(ballId="NONE", devId="DEV_NULL", level=0)
    poke2: TrainerPokemonSchema = TrainerPokemonSchema(ballId="NONE", devId="DEV_NULL", level=0)
    poke3: TrainerPokemonSchema = TrainerPokemonSchema(ballId="NONE", devId="DEV_NULL", level=0)
    poke4: TrainerPokemonSchema = TrainerPokemonSchema(ballId="NONE", devId="DEV_NULL", level=0)
    poke5: TrainerPokemonSchema = TrainerPokemonSchema(ballId="NONE", devId="DEV_NULL", level=0)
    poke6: TrainerPokemonSchema = TrainerPokemonSchema(ballId="NONE", devId="DEV_NULL", level=0)

    @validator("trid")
    def _trid(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, TRAINERID, TRAINERID[0])
        return value

    @validator("trainerType")
    def _trainerType(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, TRAINERTYPE, TRAINERTYPE[0])
        return value

    @validator("trNameLabel")
    def _trNameLabel(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, TRAINERNAMELABEL, TRAINERNAMELABEL[0])
        return value

    @validator("dataType")
    def _dataType(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, ["NORMAL", "WAZA"], "NORMAL")
        return value

    @validator("battleType")
    def _battleType(cls, value: str) -> str:
        """Make sure it is one of these items."""
        value = validate_item_in_list(value, BATTLETYPES, BATTLETYPES[0])
        return value
