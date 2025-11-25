__all__ = [
    "ZATrainerDataArray",
    "ZATrainerData",
    "ZAEffortTalentValues",
    "ZAWazaData",
    "ZAPokemonData",
]


import json

import pydantic

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
    ZAWaza,
)
from skypy.types.mappers import dev_translation, item_translation, waza_translation


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
        extra="forbid",
    )

    hp: int = pydantic.Field(
        0,
        description="HP.",
        examples=[0],
        ge=0,
        le=255,
    )
    attack: int = pydantic.Field(
        0,
        description="Attack.",
        examples=[0],
        ge=0,
        le=255,
        alias="atk",
        serialization_alias="atk",
    )
    defense: int = pydantic.Field(
        0,
        description="Defense.",
        examples=[0],
        ge=0,
        le=255,
        alias="def",
        serialization_alias="def",
    )
    special_attack: int = pydantic.Field(
        0,
        description="Special attack.",
        examples=[0],
        ge=0,
        le=255,
        alias="spAtk",
        serialization_alias="spAtk",
    )
    special_defense: int = pydantic.Field(
        0,
        description="Special defense.",
        examples=[0],
        ge=0,
        le=255,
        alias="spDef",
        serialization_alias="spDef",
    )
    speed: int = pydantic.Field(
        0,
        description="Agility.",
        examples=[0],
        ge=0,
        le=255,
        alias="agi",
        serialization_alias="agi",
    )

    @pydantic.field_validator(
        "hp",
        "attack",
        "defense",
        "special_attack",
        "special_defense",
        "speed",
        mode="before",
    )
    @classmethod
    def validate_int(cls, v: int) -> int:
        """Validate the integer."""
        if v > 255:
            return 255
        if v < 0:
            return 0
        return v


class ZAWazaData(pydantic.BaseModel):
    """Waza data."""

    model_config = pydantic.ConfigDict(
        validate_default=True,
        validate_assignment=True,
        extra="forbid",
    )

    waza_id: ZAWaza = pydantic.Field(
        "WAZA_NULL",
        description="Waza ID.",
        examples=["WAZA_NULL"],
        serialization_alias="wazaId",
        alias="wazaId",
    )
    is_plus_waza: bool = pydantic.Field(
        False,
        description="Is plus waza.",
        examples=[False],
        serialization_alias="isPlusWaza",
        alias="isPlusWaza",
    )

    @property
    def waza_id_english(self) -> str:
        """Get the translated Waza ID."""
        return waza_translation.get(self.waza_id, self.waza_id)


class ZAPokemonData(pydantic.BaseModel):
    """Pokemon data.

    Example:
    ```json
    {
        "devId": "DEV_MEGANIUMU",
        "formId": 0,
        "sex": "DEFAULT",
        "item": "ITEMID_NONE",
        "level": 10,
        "ballId": "MONSUTAABOORU",
        "waza1": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
        "waza2": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
        "waza3": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
        "waza4": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
        "seikaku": "GANBARIYA",
        "tokusei": "RANDOM_12",
        "talentValue": {
            "hp": 0,
            "atk": 0,
            "def": 0,
            "spAtk": 0,
            "spDef": 0,
            "agi": 0,
        },
        "effortValue": {
            "hp": 0,
            "atk": 0,
            "def": 0,
            "spAtk": 0,
            "spDef": 0,
            "agi": 0,
        },
        "rareType": "NO_RARE",
        "scaleValue": 128,
    }
    ```
    """

    model_config = pydantic.ConfigDict(
        validate_default=True,
        validate_assignment=True,
        extra="forbid",
    )

    dev_id: ZADevID = pydantic.Field(
        description="Developer ID.",
        examples=["DEV_MEGANIUMU"],
        serialization_alias="devId",
        alias="devId",
    )
    form_id: FormID = pydantic.Field(
        0,
        description="Form ID.",
        examples=[0],
        serialization_alias="formId",
        alias="formId",
    )
    sex: Sex = pydantic.Field(
        "DEFAULT",
        description="Sex.",
        examples=["DEFAULT", "MALE", "FEMALE"],
    )
    item: ZAItemID = pydantic.Field(
        "ITEMID_NONE",
        description="Item.",
        examples=["ITEMID_NONE"],
    )
    level: int = pydantic.Field(
        10,
        description="Level.",
        examples=[10],
        ge=0,
        le=100,
    )
    ball_id: ZABallID = pydantic.Field(
        "MONSUTAABOORU",
        description="Ball ID.",
        examples=["MONSUTAABOORU"],
        serialization_alias="ballId",
        alias="ballId",
    )
    seikaku: ZASeikaku = pydantic.Field(
        "GANBARIYA",
        description="Seikaku.",
        examples=["GANBARIYA"],
    )
    tokusei: Tokusei = pydantic.Field(
        "RANDOM_12",
        description="Tokusei.",
        examples=["RANDOM_12"],
    )
    talent_value: ZAEffortTalentValues = pydantic.Field(
        ZAEffortTalentValues(),
        description="Talent value.",
        examples=[{"hp": 0, "atk": 0, "def": 0, "spAtk": 0, "spDef": 0, "agi": 0}],
        serialization_alias="talentValue",
        alias="talentValue",
    )
    effort_value: ZAEffortTalentValues = pydantic.Field(
        ZAEffortTalentValues(),
        description="Effort value.",
        examples=[{"hp": 0, "atk": 0, "def": 0, "spAtk": 0, "spDef": 0, "agi": 0}],
        serialization_alias="effortValue",
        alias="effortValue",
    )
    rare_type: RareType = pydantic.Field(
        "NO_RARE",
        description="Rare type.",
        examples=["NO_RARE"],
        serialization_alias="rareType",
        alias="rareType",
    )
    scale_value: int = pydantic.Field(
        128,
        description="Scale value.",
        examples=[128],
        ge=1,
        le=255,
        serialization_alias="scaleValue",
        alias="scaleValue",
    )
    waza1: ZAWazaData = pydantic.Field(
        ZAWazaData(),
        description="Waza 1.",
        examples=[{"wazaId": "WAZA_NULL", "isPlusWaza": False}],
    )
    waza2: ZAWazaData = pydantic.Field(
        ZAWazaData(),
        description="Waza 2.",
        examples=[{"wazaId": "WAZA_NULL", "isPlusWaza": False}],
    )
    waza3: ZAWazaData = pydantic.Field(
        ZAWazaData(),
        description="Waza 3.",
        examples=[{"wazaId": "WAZA_NULL", "isPlusWaza": False}],
    )
    waza4: ZAWazaData = pydantic.Field(
        ZAWazaData(),
        description="Waza 4.",
        examples=[{"wazaId": "WAZA_NULL", "isPlusWaza": False}],
    )

    @property
    def dev_id_english(self) -> str:
        """Get the translated Dev ID."""
        return dev_translation.get(self.dev_id, self.dev_id)

    @property
    def item_english(self) -> str:
        """Get the translated Item ID."""
        return item_translation.get(self.item, self.item)


class ZATrainerData(pydantic.BaseModel):
    """Trainer data.

    Example:
    ```json
    {
        "trid": "00_test_data",
        "trtype": 1048451227980125490,
        "trtype2": 1048451227980125490,
        "zaRank": "NONE",
        "moneyRate": 12,
        "megEvolution": False,
        "lastHand": False,
        "poke1": {...},
        "poke2": {...},
        ...,
        "aiBasic": True,
        "aiHigh": False,
        "aiExpert": False,
        "aiDouble": False,
        "aiRaid": False,
        "aiWeak": False,
        "aiItem": False,
        "aiChange": False,
        "viewHorizontalAngle": 30.0,
        "viewVerticalAngle": 50.0,
        "viewRange": 17.0,
        "hearingRange": 17.0,
    }
    ```
    """

    model_config = pydantic.ConfigDict(
        validate_default=True,
        validate_assignment=True,
        extra="forbid",
    )

    trid: str = pydantic.Field(
        description="Trainer ID.",
        examples=["00_test_data"],
    )
    trtype: int = pydantic.Field(
        description="Trainer type.",
        examples=[1048451227980125490],
    )
    trtype2: int = pydantic.Field(
        description="Trainer type 2.",
        examples=[1048451227980125490],
    )
    za_rank: ZARank = pydantic.Field(
        description="ZA rank.",
        examples=["NONE"],
        alias="zaRank",
        serialization_alias="zaRank",
    )
    money_rate: int = pydantic.Field(
        description="Money rate.",
        examples=[12],
        ge=0,
        le=20,
        alias="moneyRate",
        serialization_alias="moneyRate",
    )
    meg_evolution: bool = pydantic.Field(
        description="Meg evolution.",
        examples=[False],
        alias="megEvolution",
        serialization_alias="megEvolution",
    )
    last_hand: bool = pydantic.Field(
        description="Last hand.",
        examples=[False],
        alias="lastHand",
        serialization_alias="lastHand",
    )
    ai_basic: bool = pydantic.Field(
        description="AI basic.",
        examples=[True],
        alias="aiBasic",
        serialization_alias="aiBasic",
    )
    ai_high: bool = pydantic.Field(
        description="AI high.",
        examples=[False],
        alias="aiHigh",
        serialization_alias="aiHigh",
    )
    ai_expert: bool = pydantic.Field(
        description="AI expert.",
        examples=[False],
        alias="aiExpert",
        serialization_alias="aiExpert",
    )
    ai_double: bool = pydantic.Field(
        description="AI double.",
        examples=[False],
        alias="aiDouble",
        serialization_alias="aiDouble",
    )
    ai_raid: bool = pydantic.Field(
        description="AI raid.",
        examples=[False],
        alias="aiRaid",
        serialization_alias="aiRaid",
    )
    ai_weak: bool = pydantic.Field(
        description="AI weak.",
        examples=[False],
        alias="aiWeak",
        serialization_alias="aiWeak",
    )
    ai_item: bool = pydantic.Field(
        description="AI item.",
        examples=[False],
        alias="aiItem",
        serialization_alias="aiItem",
    )
    ai_change: bool = pydantic.Field(
        description="AI change.",
        examples=[False],
        alias="aiChange",
        serialization_alias="aiChange",
    )
    view_horizontal_angle: float = pydantic.Field(
        description="View horizontal angle.",
        examples=[30.0],
        alias="viewHorizontalAngle",
        serialization_alias="viewHorizontalAngle",
    )
    view_vertical_angle: float = pydantic.Field(
        description="View vertical angle.",
        examples=[50.0],
        alias="viewVerticalAngle",
        serialization_alias="viewVerticalAngle",
    )
    view_range: float = pydantic.Field(
        description="View range.",
        examples=[17.0],
        alias="viewRange",
        serialization_alias="viewRange",
    )
    hearing_range: float = pydantic.Field(
        description="Hearing range.",
        examples=[17.0],
        alias="hearingRange",
        serialization_alias="hearingRange",
    )
    poke1: ZAPokemonData = pydantic.Field(
        description="Pokemon.",
    )
    poke2: ZAPokemonData = pydantic.Field(
        description="Pokemon.",
    )
    poke3: ZAPokemonData = pydantic.Field(
        description="Pokemon.",
    )
    poke4: ZAPokemonData = pydantic.Field(
        description="Pokemon.",
    )
    poke5: ZAPokemonData = pydantic.Field(
        description="Pokemon.",
    )
    poke6: ZAPokemonData = pydantic.Field(
        description="Pokemon.",
    )


class ZATrainerDataArray(pydantic.BaseModel):
    """Trainer data array."""

    model_config = pydantic.ConfigDict(
        validate_default=True,
        validate_assignment=True,
        extra="forbid",
    )

    values: list[ZATrainerData] = pydantic.Field(
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
