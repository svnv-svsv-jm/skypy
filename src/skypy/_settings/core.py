__all__ = ["Settings", "settings"]

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

    @pydantic.computed_field(repr=False)  # type: ignore
    @property
    def waza_docs_file(self) -> str:
        """Waza docs file location."""
        f = os.path.join(self.docs_loc, self.waza_docs)
        return f

    @pydantic.computed_field(repr=False)  # type: ignore
    @property
    def personal_docs_file(self) -> str:
        """Personal docs file location."""
        f = os.path.join(self.docs_loc, self.personal_docs)
        return f


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

    @pydantic.computed_field()  # type: ignore
    @property
    def input_folder(self) -> str:
        """Input folder."""
        return os.path.join(self.root, self.input_folder_name)

    @pydantic.computed_field()  # type: ignore
    @property
    def output_folder(self) -> str:
        """Output folder."""
        return os.path.join(self.root, self.output_folder_name)

    @pydantic.computed_field()  # type: ignore
    @property
    def json_folder(self) -> str:
        """JSON folder."""
        return os.path.join(self.assets, "json")

    @pydantic.computed_field()  # type: ignore
    @property
    def schema_folder(self) -> str:
        """Schema folder."""
        return os.path.join(self.assets, "schema")

    @pydantic.computed_field()  # type: ignore
    @property
    def waza_schema(self) -> str:
        """Waza schema file."""
        return os.path.join(self.schema_folder, self.waza_array)

    @pydantic.computed_field()  # type: ignore
    @property
    def file_trainer_data(self) -> str:
        """Full path to trainer data file."""
        return os.path.join(self.json_folder, self.trainer_data)

    @pydantic.computed_field()  # type: ignore
    @property
    def file_personal(self) -> str:
        """Full path to personal file."""
        return os.path.join(self.json_folder, self.personal)

    @pydantic.computed_field()  # type: ignore
    @property
    def file_waza(self) -> str:
        """Full path to waza file."""
        return os.path.join(self.json_folder, self.waza)

    @pydantic.computed_field()  # type: ignore
    @property
    def file_devid(self) -> str:
        """Full path to devid file."""
        return os.path.join(self.json_folder, self.devid)

    @pydantic.computed_field()  # type: ignore
    @property
    def file_itemid(self) -> str:
        """Full path to devid file."""
        return os.path.join(self.json_folder, self.itemid)

    @pydantic.computed_field()  # type: ignore
    @property
    def file_trdevid(self) -> str:
        """Full path to devid file."""
        return os.path.join(self.json_folder, self.trdevid)


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
        "INFO",
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


settings = Settings()
