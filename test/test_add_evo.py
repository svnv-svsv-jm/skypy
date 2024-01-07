import pytest
import sys
import typing as ty
from loguru import logger

from skypy.const.pkmn import POKEMON
from skypy.const.waza import MOVES
from skypy.ops import get_pokemon, read_data, add_evo, get_evo_data


@pytest.mark.parametrize("pokemon", ["Pikachu", "Squirtle", "Mewtwo"])
def test_get_evo_data(pokemon: str) -> None:
    """Resume Pokemon."""
    # Get pokemon
    df = read_data(anew=True)
    evo_data = get_evo_data(df, pokemon, readable=True)
    _show_evos(evo_data)


@pytest.mark.parametrize(
    "pokemon, level, into",
    [
        ("dewott", 32, "hisuian samurott"),
        ("Dusclops", 50, "Dusknoir"),
        ("Drakloak", 50, "Dragapult"),
    ],
)
def test_edit_evo(pokemon: str, level: int, into: str) -> None:
    """Resume Pokemon."""
    # Get pokemon
    df = read_data(anew=True)
    evo_data = get_evo_data(df, pokemon, readable=True)
    _show_evos(evo_data)
    df = add_evo(df, pokemon, level=level, into=into)
    evo_data = get_evo_data(df, pokemon, readable=True)
    _show_evos(evo_data)
    # Test evo is correct
    found = False
    for evo in evo_data:
        name: str = evo["species"]  # type: ignore
        form: int = evo["form"]
        if form == 0:
            if name.lower() == into.lower():
                found = True
                break
        else:
            if name.lower() in into.lower():
                found = True
                break
    assert found, f"No evolution {into} for species {name}."


def _show_evos(evo_data: ty.List[ty.Dict[str, int]]) -> None:
    """Show evos information."""
    for evo in evo_data:
        species = evo["species"]
        lvl = evo["level"]
        form = evo["form"]
        logger.info(f"Evolving into {species} ({form}) at level {lvl}")


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    pytest.main([__file__, "-x", "-s"])
