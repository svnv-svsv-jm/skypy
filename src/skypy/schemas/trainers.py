from __future__ import annotations

__all__ = ["TrainerSchema", "TrainerPokemonSchema"]

import typing as ty
from pydantic import field_validator, Field

from skypy.const import BallIDs
from ._base import BaseSchema


class TrainerPokemonSchema(BaseSchema):
    """Schema for a trainer's Pokemon data."""

    ballId: BallIDs = Field(
        "MONSUTAABOORU",
        description="Pokeball type.",
    )
    devId: str = Field(description="")
    effortValue___agi: int = Field(
        0,
        description="Effort value for speed.",
        alias="effortValue.agi",
    )
    effortValue___atk: int = Field(
        0,
        description="Effort value for attack.",
        alias="effortValue.atk",
    )
    effortValue___def: int = Field(
        0,
        description="Effort value for defense.",
        alias="effortValue.def",
    )
    effortValue___hp: int = Field(
        0,
        description="Effort value for HP.",
        alias="effortValue.hp",
    )
    effortValue___spAtk: int = Field(
        0,
        description="Effort value for special attack.",
        alias="effortValue.spAtk",
    )
    effortValue___spDef: int = Field(
        0,
        description="Effort value for special defense.",
        alias="effortValue.spDef",
    )
    formId: int = Field(
        0,
        description="Form Id.",
    )
    gemType: ty.Literal[
        "DEFAULT",
        "DRAGON",
        "HAGANE",
        "HIKOU",
        "JIMEN",
        "DENKI",
        "ESPER",
        "KOORI",
        "KUSA",
        "MIZU",
        "MUSHI",
        "NORMAL",
        "KAKUTOU",
        "HONOO",
        "GHOST",
        "AKU",
        "FAIRY",
        "IWA",
        "DOKU",
    ] = "DEFAULT"
    item: str = "ITEMID_NONE"
    level: int = Field(ge=0, le=100, description="Level.")
    rareType: ty.Literal["NO_RARE", "DEFAULT"] = Field(
        "DEFAULT",
        description="",
    )
    scaleType: ty.Literal["VALUE", "XL"] = "VALUE"
    scaleValue: int = 175
    seikaku: ty.Literal[
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
    ] = Field("DEFAULT")
    sex: ty.Literal["DEFAULT", "MALE", "FEMALE"] = Field("DEFAULT")
    talentType: ty.Literal["RANDOM", "VALUE"] = Field("RANDOM")
    talentValue___agi: int = 0
    talentValue___atk: int = 0
    talentValue___def: int = 0
    talentValue___hp: int = 0
    talentValue___spAtk: int = 0
    talentValue___spDef: int = 0
    talentVnum: int = 20
    tokusei: ty.Literal["RANDOM_12", "SET_3", "SET_1", "SET_2"] = Field(
        "RANDOM_12",
        description="Ability.",
    )
    waza1___pointUp: int = 0
    waza1___wazaId: str = "WAZA_NULL"
    waza2___pointUp: int = 0
    waza2___wazaId: str = "WAZA_NULL"
    waza3___pointUp: int = 0
    waza3___wazaId: str = "WAZA_NULL"
    waza4___pointUp: int = 0
    waza4___wazaId: str = "WAZA_NULL"
    wazaType: ty.Literal["DEFAULT", "MANUAL"] = Field(
        "DEFAULT",
        description="Whether moves are chosen automatically or manually.",
    )


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
    battleType: ty.Literal["_1vs1", "_2vs2"] = "_1vs1"
    changeGem: bool = False
    dataType: str = "NORMAL"  # ['NORMAL', 'WAZA']
    isStrong: bool = True
    moneyRate: int = 15
    popupLabelNormal1: str = ""
    popupLabelNormal2: str = ""
    popupLabelPinch1: str = ""
    popupLabelPinch2: str = ""
    trNameLabel: str = ""
    trainerType: str = "karate"
    trid: str = "00_test_data"
    poke1: TrainerPokemonSchema = TrainerPokemonSchema(ballId="NONE", devId="DEV_NULL", level=0)
    poke2: TrainerPokemonSchema = TrainerPokemonSchema(ballId="NONE", devId="DEV_NULL", level=0)
    poke3: TrainerPokemonSchema = TrainerPokemonSchema(ballId="NONE", devId="DEV_NULL", level=0)
    poke4: TrainerPokemonSchema = TrainerPokemonSchema(ballId="NONE", devId="DEV_NULL", level=0)
    poke5: TrainerPokemonSchema = TrainerPokemonSchema(ballId="NONE", devId="DEV_NULL", level=0)
    poke6: TrainerPokemonSchema = TrainerPokemonSchema(ballId="NONE", devId="DEV_NULL", level=0)
