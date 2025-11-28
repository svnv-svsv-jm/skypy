__all__ = [
    "ZATrainerDataArray",
    "ZATrainerData",
    "ZAEffortTalentValues",
    "ZAWazaData",
    "ZAPokemonData",
]


import json

import pydantic
from pydantic.alias_generators import to_pascal

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

from ._base import _ByAliasInitializer, _ByAliasSerializer


class ZAEffortTalentValues(pydantic.BaseModel):
    """Talent values.

    Example:
    ```json
    {"hp": 0, "atk": 0, "def": 0, "spAtk": 0, "spDef": 0, "agi": 0}
    ```
    """

    model_config = pydantic.ConfigDict(
        validate_default=True,
        validate_assignment=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        extra="forbid",
    )

    HP: int = pydantic.Field(
        0,
        description="HP.",
        ge=0,
        le=255,
    )
    ATK: int = pydantic.Field(
        0,
        description="Attack.",
        ge=0,
        le=255,
    )
    DEF: int = pydantic.Field(
        0,
        description="Defense.",
        ge=0,
        le=255,
        alias="Def",
        serialization_alias="Def",
    )
    SPA: int = pydantic.Field(
        0,
        description="Special attack.",
        ge=0,
        le=255,
    )
    SPD: int = pydantic.Field(
        0,
        description="Special defense.",
        ge=0,
        le=255,
    )
    SPE: int = pydantic.Field(
        0,
        description="Agility.",
        ge=0,
        le=255,
    )


class ZAWazaData(pydantic.BaseModel):
    """Waza data."""

    model_config = pydantic.ConfigDict(
        validate_default=True,
        validate_assignment=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        alias_generator=to_pascal,
        extra="forbid",
    )

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


class ZAPokemonData(pydantic.BaseModel):
    """Pokemon data."""

    model_config = pydantic.ConfigDict(
        extra="forbid",
        validate_assignment=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_default=True,
        alias_generator=to_pascal,
    )

    dev_id: ZADevID = pydantic.Field(
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


class ZATrainerData(_ByAliasInitializer, _ByAliasSerializer, pydantic.BaseModel):
    """Trainer data."""

    model_config = pydantic.ConfigDict(
        extra="forbid",
        validate_assignment=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_default=True,
        alias_generator=to_pascal,
    )

    tr_id: str = pydantic.Field(
        description="Trainer ID.",
        examples=["00_test_data"],
    )
    tr_type: int = pydantic.Field(
        description="Trainer type.",
        examples=[1048451227980125490],
    )
    tr_type_2: int = pydantic.Field(
        description="Trainer type 2.",
        examples=[1048451227980125490],
    )
    za_rank: ZARank = pydantic.Field(
        description="ZA rank.",
        examples=["NONE"],
        alias="ZARank",
        serialization_alias="ZARank",
    )
    money_rate: int = pydantic.Field(
        description="Money rate.",
        examples=[12],
        ge=0,
        le=20,
    )
    meg_evolution: bool = pydantic.Field(
        description="Meg evolution.",
        examples=[False],
    )
    last_hand_mega: bool = pydantic.Field(
        description="Last hand.",
        examples=[False],
    )
    ai_basic: bool = pydantic.Field(
        description="AI basic.",
        examples=[True],
    )
    ai_high: bool = pydantic.Field(
        description="AI high.",
        examples=[False],
    )
    ai_expert: bool = pydantic.Field(
        description="AI expert.",
        examples=[False],
    )
    ai_double: bool = pydantic.Field(
        description="AI double.",
        examples=[False],
    )
    ai_raid: bool = pydantic.Field(
        description="AI raid.",
        examples=[False],
    )
    ai_weak: bool = pydantic.Field(
        description="AI weak.",
        examples=[False],
    )
    ai_item: bool = pydantic.Field(
        description="AI item.",
        examples=[False],
    )
    ai_change: bool = pydantic.Field(
        description="AI change.",
        examples=[False],
    )
    view_horizontal_angle: float = pydantic.Field(
        description="View horizontal angle.",
        examples=[30.0],
    )
    view_vertical_angle: float = pydantic.Field(
        description="View vertical angle.",
        examples=[50.0],
    )
    view_range: float = pydantic.Field(
        description="View range.",
        examples=[17.0],
    )
    hearing_range: float = pydantic.Field(
        description="Hearing range.",
        examples=[17.0],
    )
    poke_1: ZAPokemonData = pydantic.Field(
        description="Pokemon.",
    )
    poke_2: ZAPokemonData = pydantic.Field(
        description="Pokemon.",
    )
    poke_3: ZAPokemonData = pydantic.Field(
        description="Pokemon.",
    )
    poke_4: ZAPokemonData = pydantic.Field(
        description="Pokemon.",
    )
    poke_5: ZAPokemonData = pydantic.Field(
        description="Pokemon.",
    )
    poke_6: ZAPokemonData = pydantic.Field(
        description="Pokemon.",
    )


class ZATrainerDataArray(pydantic.BaseModel):
    """Trainer data array."""

    model_config = pydantic.ConfigDict(
        extra="forbid",
        validate_assignment=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_default=True,
        alias_generator=to_pascal,
    )

    table: list[ZATrainerData] = pydantic.Field(
        description="Values.",
    )

    def get_trainer(self, trid: str) -> ZATrainerData:
        """Get a trainer by ID."""
        for trainer in self.values:
            if trainer.trid == trid:
                return trainer
        raise ValueError(f"Trainer with ID {trid} not found.")

    def set_trainer(self, trid: str, trainer: ZATrainerData) -> None:
        """Set a trainer by ID."""
        for i, t in enumerate(self.values):
            if t.trid == trid:
                self.values[i] = trainer
                return
        raise ValueError(f"Trainer with ID {trid} not found.")

    def dump(self, path: str) -> None:
        """Dump the data to a JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.model_dump(by_alias=True), f, indent=2, ensure_ascii=False)
