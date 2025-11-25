import pytest
from loguru import logger

from skypy.schemas import ZAPokemonData


@pytest.mark.parametrize(
    "pkdata",
    [
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
    ],
)
def test_effort_values(pkdata: dict[str, int]) -> None:
    """Test effort values."""
    data = ZAPokemonData(**pkdata)
    logger.info(data)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
