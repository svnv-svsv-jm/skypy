__all__ = ["EvoData"]

from pydantic.dataclasses import dataclass


@dataclass
class EvoData:
    """Evolution data.

    Attributes:
        level (int):
            TODO: add info.
    """

    level: int
    species: int
    condition: int = 16
    form: int = 0
    parameter: int = 0
    reserved3: int = 0
    reserved4: int = 0
    reserved5: int = 0
