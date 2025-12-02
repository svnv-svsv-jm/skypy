__all__ = ["Settings", "settings"]

import json
import os
import typing as ty

import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppliedChanges(pydantic.BaseModel):
    """Settings for applied changes."""

    docs_loc: str = pydantic.Field(
        "docs",
        description="Location for documentation of applied changes.",
    )
    waza_docs: str = pydantic.Field(
        "waza.xlsx",
        description="Name (with extension) of the file where we store the docs for the applied changes to waza.",
    )
    personal_docs: str = pydantic.Field(
        "personal.xlsx",
        description="Name (with extension) of the file where we store the docs for the applied changes to personal.",
    )


class Files(pydantic.BaseModel):
    """Settings for locations and files."""

    root: str = pydantic.Field(
        ".",
        description="Root folder.",
    )
    assets: str = pydantic.Field(
        os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets")),
        description="Directory for assets.",
    )
    za_assets: str = pydantic.Field(
        os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets", "za")),
        description="Directory for assets.",
    )
    trainer_data: str = pydantic.Field(
        "trdata_array.json",
        description="File name for the trainer data.",
    )
    waza: str = pydantic.Field(
        "waza_array.json",
        description="File name for the waza data.",
    )
    personal: str = pydantic.Field(
        "personal_array.json",
        description="File name for the personal data.",
    )
    trdevid: str = pydantic.Field(
        "trdev_id.json",
        description="File name for the trainer dev data.",
    )
    devid: str = pydantic.Field(
        "devid_list.json",
        description="File name for the dev IDs data.",
    )
    itemid: str = pydantic.Field(
        "item_list.json",
        description="List of all items.",
    )
    input_folder_name: str = pydantic.Field(
        "input",
        description="Folder where to place input files.",
    )
    output_folder_name: str = pydantic.Field(
        "output",
        description="Folder where to generate output files.",
    )
    bin_folder_name: str = pydantic.Field(
        "bin",
        description="Folder where to generate bin files.",
    )
    waza_array: str = pydantic.Field(
        "waza_array.fbs",
        description="File name for the waza array.",
    )
    za_trainers_bfbs_file: str = pydantic.Field(
        os.path.join("sandbox", "trdata_array.bfbs"),
        description="File name for the ZA trainers binary file.",
    )

    @pydantic.computed_field()  # type: ignore
    @property
    def file_trainer_data(self) -> str:
        """Full path to trainer data file."""
        return os.path.join(self.assets, "za", self.trainer_data)


class Settings(BaseSettings):
    """App settings."""

    # Settings configuration
    model_config = SettingsConfigDict(
        env_prefix="SKYPY_",
        env_nested_delimiter="__",
        case_sensitive=False,  # from the environment
    )

    # Settings
    test_mode: bool = pydantic.Field(
        False,
        description="If `True`, verbosity and strictness on errors are increased.",
    )
    log_level: ty.Literal["TRACE", "DEBUG", "INFO"] = pydantic.Field(
        "TRACE",
        description="Logging level.",
    )
    applied_changes: AppliedChanges = pydantic.Field(
        AppliedChanges(),
        description="Applied changes.",
    )
    files: Files = pydantic.Field(
        Files(),
        description="Files.",
    )

    @property
    def za_species_table_file(self) -> str:
        """ZA species table file."""
        return os.path.join(self.files.assets, "za", "species.txt")

    @property
    def za_species_table(self) -> list[str]:
        """ZA species table."""
        with open(self.za_species_table_file, encoding="utf-8") as f:
            species_list = [line.strip() for line in f if line.strip()]
        return species_list

    @property
    def za_waza_table_file(self) -> str:
        """ZA waza table file."""
        return os.path.join(self.files.assets, "za", "moves.txt")

    @property
    def za_waza_table(self) -> list[str]:
        """ZA waza table."""
        with open(self.za_waza_table_file, encoding="utf-8") as f:
            waza_list = [line.strip() for line in f if line.strip()]
        return waza_list

    @property
    def za_items_table_file(self) -> str:
        """ZA items table file."""
        return os.path.join(self.files.assets, "za", "items.txt")

    @property
    def za_items_table(self) -> list[str]:
        """ZA items table."""
        with open(self.za_items_table_file, encoding="utf-8") as f:
            items_list = [line.strip() for line in f if line.strip()]
        return items_list

    @property
    def za_mappings_location(self) -> str:
        """ZA waza mappings directory."""
        return os.path.join(self.files.assets, "za", "mappings")

    @property
    def za_waza_mappings_file(self) -> str:
        """ZA waza mappings file."""
        return os.path.join(self.za_mappings_location, "wazaId.json")

    @property
    def za_waza_mappings(self) -> dict[str, int]:
        """ZA waza mappings."""
        return _get_mappings(self.za_waza_mappings_file)

    @property
    def za_species_mappings_file(self) -> str:
        """ZA species mappings file."""
        return os.path.join(self.za_mappings_location, "devId.json")

    @property
    def za_species_mappings(self) -> dict[str, int]:
        """ZA species mappings."""
        return _get_mappings(self.za_species_mappings_file)

    @property
    def za_ball_mappings_file(self) -> str:
        """ZA ball mappings file."""
        return os.path.join(self.za_mappings_location, "ballId.json")

    @property
    def za_ball_mappings(self) -> dict[str, int]:
        """ZA ball mappings."""
        return _get_mappings(self.za_ball_mappings_file)

    @property
    def za_seikaku_mappings_file(self) -> str:
        """ZA seikaku mappings file."""
        return os.path.join(self.za_mappings_location, "seikaku.json")

    @property
    def za_seikaku_mappings(self) -> dict[str, int]:
        """ZA seikaku mappings."""
        return _get_mappings(self.za_seikaku_mappings_file)

    @property
    def za_rare_type_mappings_file(self) -> str:
        """ZA rare type mappings file."""
        return os.path.join(self.za_mappings_location, "rareType.json")

    @property
    def za_rare_type_mappings(self) -> dict[str, int]:
        """ZA rare type mappings."""
        return _get_mappings(self.za_rare_type_mappings_file)

    @property
    def za_rank_mappings_file(self) -> str:
        """ZA rank mappings file."""
        return os.path.join(self.za_mappings_location, "rank.json")

    @property
    def za_rank_mappings(self) -> dict[str, int]:
        """ZA rank mappings."""
        return _get_mappings(self.za_rank_mappings_file)

    @property
    def za_item_mappings_file(self) -> str:
        """ZA item mappings file."""
        return os.path.join(self.za_mappings_location, "item.json")

    @property
    def za_item_mappings(self) -> dict[str, int]:
        """ZA item mappings."""
        return _get_mappings(self.za_item_mappings_file)

    @property
    def za_sex_mappings_file(self) -> str:
        """ZA sex mappings file."""
        return os.path.join(self.za_mappings_location, "sex.json")

    @property
    def za_sex_mappings(self) -> dict[str, int]:
        """ZA sex mappings."""
        return _get_mappings(self.za_sex_mappings_file)

    @property
    def za_tokusei_mappings_file(self) -> str:
        """ZA tokusei mappings file."""
        return os.path.join(self.za_mappings_location, "tokusei.json")

    @property
    def za_tokusei_mappings(self) -> dict[str, int]:
        """ZA tokusei mappings."""
        return _get_mappings(self.za_tokusei_mappings_file)


def _get_mappings(filename: str) -> dict[str, int]:
    """Get mappings from a file."""
    with open(filename, encoding="utf-8") as f:
        mappings: dict[str, int] = json.load(f)
    return mappings


settings = Settings()
