import pytest

from skypy import settings
from skypy.schemas import ZAWazaData


@pytest.mark.parametrize("waza_id", range(1, 5))
def test_waza_data_to_eng(waza_id: int) -> None:
    """Test `ZAWazaData` class English name conversion."""
    data = ZAWazaData(waza_id=waza_id, is_plus_waza=False)
    assert data.waza_id_english == settings.za_waza_table[waza_id]


def test_waza_from_str() -> None:
    """Test we can create a `ZAWazaData` object from the Trainder Data string representation, not only from the `int` version."""
    data = ZAWazaData(waza_id="WAZA_HONOONOPANTI")  # type: ignore
    assert data.waza_id == 7
    assert data.waza_id_english == settings.za_waza_table[7]


def test_waza_data_to_str() -> None:
    """Test we can dump a `ZAWazaData` object to the string representation."""
    data = ZAWazaData(waza_id=7, is_plus_waza=False)
    raw = data.model_dump(mode="json")
    assert raw == {"waza_id": "WAZA_HONOONOPANTI", "is_plus_waza": False}


def test_waza_data_null_dump() -> None:
    """Test we can dump a `ZAWazaData` object to the string representation when it is null."""
    data = ZAWazaData()
    raw = data.model_dump(mode="json", exclude_unset=True)
    assert raw == {}


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-s"])
