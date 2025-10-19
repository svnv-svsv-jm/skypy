__all__ = ["DevId", "DevIdList"]

from pydantic import BaseModel, Field


class DevId(BaseModel):
    """Devid.

    Example:
    ```json
    {
        "devName": "DEV_NULL",
        "id": 0,
        "name": "Egg",
        "forms": 1
    }
    ```
    """

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
    forms: int = Field(
        description="Number of forms.",
    )


class DevIdList(BaseModel):
    """Content of the `devid_list.json` file."""

    values: list[DevId] = Field(description="List of DevId's.")
