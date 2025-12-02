__all__ = [
    "ZATrainerDataArray",
    "ZATrainerData",
    "ZAEffortTalentValues",
    "ZAWazaData",
    "ZAPokemonData",
]


import json
import os
import subprocess

import pydantic
from loguru import logger
from pydantic.alias_generators import to_camel as alias_generator

from skypy import settings
from skypy.types import (
    FormID,
    RareType,
    Sex,
    Tokusei,
    ZABallID,
    ZADevID,
    ZAItemID,
    ZARank,
    ZASeikaku,
    ZAWazaID,
)

COMMON_MODEL_CFG = pydantic.ConfigDict(
    extra="forbid",
    validate_assignment=True,
    populate_by_name=True,
    arbitrary_types_allowed=True,
    validate_default=True,
    alias_generator=alias_generator,
)


def get_key_by_value(
    mapping: dict[str, int],
    value: int,
    default: str | None = None,
) -> str:
    """Get the key by value from a mapping."""
    try:
        return next(key for key, val in mapping.items() if val == value)
    except StopIteration:
        default = default or list(mapping.keys())[0]
        return default


class ZAEffortTalentValues(pydantic.BaseModel):
    """Talent values.

    Example:
    ```json
    {"hp": 0, "atk": 0, "def": 0, "spAtk": 0, "spDef": 0, "agi": 0}
    ```
    """

    model_config = COMMON_MODEL_CFG

    HP: int = pydantic.Field(
        0,
        description="HP.",
        ge=0,
        le=255,
        alias="hp",
        serialization_alias="hp",
    )
    ATK: int = pydantic.Field(
        0,
        description="Attack.",
        ge=0,
        le=255,
        alias="atk",
        serialization_alias="atk",
    )
    DEF: int = pydantic.Field(
        0,
        description="Defense.",
        ge=0,
        le=255,
        alias="def",
        serialization_alias="def",
    )
    SPA: int = pydantic.Field(
        0,
        description="Special attack.",
        ge=0,
        le=255,
        alias="spAtk",
        serialization_alias="spAtk",
    )
    SPD: int = pydantic.Field(
        0,
        description="Special defense.",
        ge=0,
        le=255,
        alias="spDef",
        serialization_alias="spDef",
    )
    SPE: int = pydantic.Field(
        0,
        description="Agility.",
        ge=0,
        le=255,
        alias="agi",
        serialization_alias="agi",
    )


class ZAWazaData(pydantic.BaseModel):
    """Waza data."""

    model_config = COMMON_MODEL_CFG

    waza_id: ZAWazaID = pydantic.Field(
        0,
        description="Waza ID.",
    )
    is_plus_waza: bool = pydantic.Field(
        False,
        description="Is plus waza.",
    )

    @property
    def waza_id_english(self) -> str:
        """Get the English name of the Waza."""
        return settings.za_waza_table[self.waza_id]

    @pydantic.field_serializer("waza_id", when_used="json")
    def serialize_waza_id(self, v: int) -> str:
        """Serialize the Waza ID to the string representation."""
        return get_key_by_value(settings.za_waza_mappings, v)

    @pydantic.field_validator("waza_id", mode="before")
    @classmethod
    def validate_waza_id(cls, v: str | int) -> int:
        """Validate the Waza ID. If `str`, convert to `int` using the mappings."""
        if isinstance(v, str):
            return settings.za_waza_mappings[v]
        return v


class ZAPokemonData(pydantic.BaseModel):
    """Pokemon data."""

    model_config = COMMON_MODEL_CFG

    dev_id: ZADevID = pydantic.Field(
        0,
        description="Species ID.",
    )
    form_id: FormID = pydantic.Field(
        0,
        description="Form ID.",
    )
    sex: Sex = pydantic.Field(
        0,
        description="Sex.",
    )
    item: ZAItemID = pydantic.Field(
        0,
        description="Item.",
    )
    level: int = pydantic.Field(
        10,
        description="Level.",
        examples=[10],
        ge=0,
        le=100,
    )
    ball_id: ZABallID = pydantic.Field(
        4,
        description="Ball ID.",
    )
    seikaku: ZASeikaku = pydantic.Field(
        1,
        description="Seikaku.",
    )
    tokusei: Tokusei = pydantic.Field(
        0,
        description="Tokusei.",
    )
    talent_value: ZAEffortTalentValues = pydantic.Field(
        ZAEffortTalentValues(),
        description="Talent value.",
    )
    effort_value: ZAEffortTalentValues = pydantic.Field(
        ZAEffortTalentValues(),
        description="Effort value.",
    )
    rare_type: RareType = pydantic.Field(
        1,
        description="Rare type.",
    )
    scale_value: int = pydantic.Field(
        128,
        description="Scale value.",
        examples=[128],
        ge=1,
        le=255,
    )
    waza_1: ZAWazaData = pydantic.Field(
        ZAWazaData(),
        description="Waza 1.",
    )
    waza_2: ZAWazaData = pydantic.Field(
        ZAWazaData(),
        description="Waza 2.",
    )
    waza_3: ZAWazaData = pydantic.Field(
        ZAWazaData(),
        description="Waza 3.",
    )
    waza_4: ZAWazaData = pydantic.Field(
        ZAWazaData(),
        description="Waza 4.",
    )

    @property
    def dev_id_english(self) -> str:
        """Get the English name of the Pokemon."""
        return settings.za_species_table[self.dev_id]

    @property
    def ball_id_english(self) -> str:
        """Get the English name of the Ball."""
        return settings.za_items_table[self.ball_id]

    @property
    def item_english(self) -> str:
        """Get the English name of the Item."""
        return settings.za_items_table[self.item]

    @pydantic.field_validator("dev_id", mode="before")
    @classmethod
    def validate_dev_id(cls, v: str | int) -> int:
        """Validate the Dev ID. If `str`, convert to `int` using the mappings."""
        if isinstance(v, str):
            return settings.za_species_mappings[v]
        return v

    @pydantic.field_serializer("dev_id", when_used="json")
    def serialize_dev_id(self, v: int) -> str:
        """Serialize the Dev ID to the string representation."""
        return get_key_by_value(settings.za_species_mappings, v)

    @pydantic.field_validator("ball_id", mode="before")
    @classmethod
    def validate_ball_id(cls, v: str | int) -> int:
        """Validate the Ball ID. If `str`, convert to `int` using the mappings."""
        if isinstance(v, str):
            return settings.za_ball_mappings[v]
        return v

    @pydantic.field_serializer("ball_id", when_used="json")
    def serialize_ball_id(self, v: int) -> str:
        """Serialize the Ball ID to the string representation."""
        return get_key_by_value(settings.za_ball_mappings, v)

    @pydantic.field_validator("seikaku", mode="before")
    @classmethod
    def validate_seikaku(cls, v: str | int) -> int:
        """Validate the Seikaku. If `str`, convert to `int` using the mappings."""
        if isinstance(v, str):
            return settings.za_seikaku_mappings[v]
        return v

    @pydantic.field_serializer("seikaku", when_used="json")
    def serialize_seikaku(self, v: int) -> str:
        """Serialize the Seikaku to the string representation."""
        return get_key_by_value(settings.za_seikaku_mappings, v)

    @pydantic.field_validator("rare_type", mode="before")
    @classmethod
    def validate_rare_type(cls, v: str | int) -> int:
        """Validate the Rare type. If `str`, convert to `int` using the mappings."""
        if isinstance(v, str):
            return settings.za_rare_type_mappings[v]
        return v

    @pydantic.field_serializer("rare_type", when_used="json")
    def serialize_rare_type(self, v: int) -> str:
        """Serialize the Rare type to the string representation."""
        return get_key_by_value(settings.za_rare_type_mappings, v)

    @pydantic.field_validator("item", mode="before")
    @classmethod
    def validate_item(cls, v: str | int) -> int:
        """Validate the Item. If `str`, convert to `int` using the mappings."""
        if isinstance(v, str):
            return settings.za_item_mappings[v]
        return v

    @pydantic.field_serializer("item", when_used="json")
    def serialize_item(self, v: int) -> str:
        """Serialize the Item to the string representation."""
        return get_key_by_value(settings.za_item_mappings, v)

    @pydantic.field_validator("sex", mode="before")
    @classmethod
    def validate_sex(cls, v: str | int) -> int:
        """Validate the Sex. If `str`, convert to `int` using the mappings."""
        if isinstance(v, str):
            return settings.za_sex_mappings[v]
        return v

    @pydantic.field_serializer("sex", when_used="json")
    def serialize_sex(self, v: int) -> str:
        """Serialize the Sex to the string representation."""
        return get_key_by_value(settings.za_sex_mappings, v)

    @pydantic.field_validator("tokusei", mode="before")
    @classmethod
    def validate_tokusei(cls, v: str | int) -> int:
        """Validate the Tokusei. If `str`, convert to `int` using the mappings."""
        if isinstance(v, str):
            return settings.za_tokusei_mappings[v]
        return v

    @pydantic.field_serializer("tokusei", when_used="json")
    def serialize_tokusei(self, v: int) -> str:
        """Serialize the Tokusei to the string representation."""
        return get_key_by_value(settings.za_tokusei_mappings, v)


class ZATrainerData(pydantic.BaseModel):
    """Trainer data."""

    model_config = COMMON_MODEL_CFG

    tr_id: str = pydantic.Field(
        description="Trainer ID.",
        examples=["00_test_data"],
        alias="trid",
        serialization_alias="trid",
    )
    tr_type: int = pydantic.Field(
        description="Trainer type.",
        examples=[1048451227980125490],
        alias="trtype",
        serialization_alias="trtype",
    )
    tr_type_2: int = pydantic.Field(
        description="Trainer type 2.",
        examples=[1048451227980125490],
        alias="trtype2",
        serialization_alias="trtype2",
    )
    za_rank: ZARank = pydantic.Field(
        0,
        description="ZA rank.",
    )
    money_rate: int = pydantic.Field(
        12,
        description="Money rate.",
        examples=[12],
        ge=0,
        le=20,
    )
    meg_evolution: bool = pydantic.Field(
        False,
        description="Meg evolution.",
        examples=[False],
    )
    last_hand: bool = pydantic.Field(
        False,
        description="Last hand Mega Evolution.",
        examples=[False],
    )
    ai_basic: bool = pydantic.Field(
        True,
        description="AI basic.",
        examples=[True],
    )
    ai_high: bool = pydantic.Field(
        True,
        description="AI high.",
        examples=[False],
    )
    ai_expert: bool = pydantic.Field(
        True,
        description="AI expert.",
        examples=[False],
    )
    ai_double: bool = pydantic.Field(
        False,
        description="AI double.",
        examples=[False],
    )
    ai_raid: bool = pydantic.Field(
        False,
        description="AI raid.",
        examples=[False],
    )
    ai_weak: bool = pydantic.Field(
        False,
        description="AI weak.",
        examples=[False],
    )
    ai_item: bool = pydantic.Field(
        False,
        description="AI item.",
        examples=[False],
    )
    ai_change: bool = pydantic.Field(
        True,
        description="AI change.",
        examples=[False],
    )
    view_horizontal_angle: float = pydantic.Field(
        description="View horizontal angle.",
        examples=[30.0],
    )
    view_vertical_angle: float = pydantic.Field(
        50.0,
        description="View vertical angle.",
        examples=[50.0],
    )
    view_range: float = pydantic.Field(
        17.0,
        description="View range.",
        examples=[17.0],
    )
    hearing_range: float = pydantic.Field(
        17.0,
        description="Hearing range.",
        examples=[17.0],
    )
    poke_1: ZAPokemonData = pydantic.Field(
        ZAPokemonData(),
        description="Pokemon.",
    )
    poke_2: ZAPokemonData = pydantic.Field(
        ZAPokemonData(),
        description="Pokemon.",
    )
    poke_3: ZAPokemonData = pydantic.Field(
        ZAPokemonData(),
        description="Pokemon.",
    )
    poke_4: ZAPokemonData = pydantic.Field(
        ZAPokemonData(),
        description="Pokemon.",
    )
    poke_5: ZAPokemonData = pydantic.Field(
        ZAPokemonData(),
        description="Pokemon.",
    )
    poke_6: ZAPokemonData = pydantic.Field(
        ZAPokemonData(),
        description="Pokemon.",
    )

    @pydantic.field_validator("za_rank", mode="before")
    @classmethod
    def validate_za_rank(cls, v: str | int) -> int:
        """Validate the ZA rank. If `str`, convert to `int` using the mappings."""
        if isinstance(v, str):
            return settings.za_rank_mappings[v]
        return v

    @pydantic.field_serializer("za_rank", when_used="json")
    def serialize_za_rank(self, v: int) -> str:
        """Serialize the ZA rank to the string representation."""
        return get_key_by_value(settings.za_rank_mappings, v)


class ZATrainerDataArray(pydantic.BaseModel):
    """Trainer data array."""

    model_config = COMMON_MODEL_CFG

    values: list[ZATrainerData] = pydantic.Field(
        description="Table of trainer data.",
        alias="Table",
        serialization_alias="Table",
    )

    @property
    def table(self) -> list[ZATrainerData]:
        """Get the table of trainers."""
        return self.values

    def get_trainer(self, trid: str) -> ZATrainerData:
        """Get a trainer by ID."""
        for trainer in self.table:
            if trainer.tr_id == trid:
                return trainer
        raise ValueError(f"Trainer with ID {trid} not found.")

    def set_trainer(self, trid: str, trainer: ZATrainerData) -> None:
        """Set a trainer by ID."""
        for i, t in enumerate(self.table):
            if t.tr_id == trid:
                self.table[i] = trainer
                break

    def dump(
        self,
        path: str,
        bfbs_file: str | None = None,
        create_binaries: bool = False,
    ) -> None:
        """Dump the data to a JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            data = self.model_dump(mode="json", by_alias=True, exclude_unset=True)
            json.dump(data, f, indent=2, ensure_ascii=False)
            logger.trace(f"Dumped data to {path}: {data}")

        if create_binaries:
            bfbs_file = bfbs_file or settings.files.za_trainers_bfbs_file
            if os.path.exists(bfbs_file):
                logger.trace(f"Creating binary for {path}...")
                dirname = os.path.dirname(path)
                subprocess.run(["flatc", "-b", "-o", dirname, bfbs_file, path])
