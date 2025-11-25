import pytest
from loguru import logger

from skypy.schemas import ZAEffortTalentValues


@pytest.mark.parametrize(
    "ev",
    [
        {"hp": 0, "atk": 0, "def": 0, "spAtk": 0, "spDef": 0, "agi": 0},
        {"hp": 1, "atk": 1, "def": 1, "spAtk": 1, "spDef": 1, "agi": 1},
        {"hp": 255, "atk": 255, "def": 255, "spAtk": 255, "spDef": 255, "agi": 255},
    ],
)
def test_effort_values(ev: dict[str, int]) -> None:
    """Test effort values."""
    data = ZAEffortTalentValues(**ev)
    logger.info(data)
    assert data.hp == ev["hp"]
    assert data.attack == ev["atk"]
    assert data.defense == ev["def"]
    assert data.special_attack == ev["spAtk"]
    assert data.special_defense == ev["spDef"]
    assert data.speed == ev["agi"]
    assert data.model_dump(by_alias=True) == ev


@pytest.mark.parametrize(
    "ev",
    [
        {"hp": -1, "atk": -1, "def": -1, "spAtk": 333, "spDef": 444, "agi": 1000},
    ],
)
def test_sanitization(ev: dict[str, int]) -> None:
    """Test sanitization."""
    data = ZAEffortTalentValues(**ev)
    logger.info(data)
    for key, val in data.model_dump().items():
        assert 0 <= val <= 255


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
