__all__ = ["pkmn_to_int"]

from skypy.const.pkmn import POKEMON


def int_to_pkmn(i: int) -> str:
    """Maps ID to its Pokemon."""
    n = len(POKEMON)
    assert 0 < i < n, f"Invalid value, must be between 0 and {n}."
    return POKEMON[i]


def pkmn_to_int(name: str) -> int:
    """Maps Pokemon name to its ID."""
    return POKEMON.index(name)
