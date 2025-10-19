__all__ = ["TrDevId", "TrDevIdList"]

from pydantic import BaseModel, Field


class TrDevId(BaseModel):
    """Item IDs."""

    dev_id: str = Field(description="Trainer ID.")
    name: str = Field(description="Trainer name.")


class TrDevIdList(BaseModel):
    """Content of the `trdev_id.json` file."""

    trainers: list[TrDevId] = Field(description="List of trainers.")
