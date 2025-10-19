__all__ = ["ItemId", "ItemIdList"]

from pydantic import BaseModel, Field


class ItemId(BaseModel):
    """Item IDs."""

    devname: str = Field(
        alias="devName",
        description="Dev name for the species.",
    )
    id: int = Field(
        description="ID of the species.",
    )
    name: str = Field(
        description="Name of the species.",
    )


class ItemIdList(BaseModel):
    """Content of the `item_list.json` file."""

    items: list[ItemId] = Field(description="List of DevId's.")
