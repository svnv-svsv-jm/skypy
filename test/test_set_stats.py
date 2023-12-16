import pytest, sys
from typing import Union, Sequence, Dict
from loguru import logger

from skypy.ops import get_stats, set_pokemon, read_data


@pytest.mark.parametrize(
    "pokemon, stats_to_give",
    [
        ("deino", [1] * 6),
        ("mew", (1, 2, 3, 4, 5, 6)),
        (
            "pikachu",
            {
                "base_stats.HP": 200,
                "base_stats.ATK": 1,
                "base_stats.DEF": 1,
                "base_stats.SPA": 1,
                "base_stats.SPD": 1,
                "base_stats.SPE": 1,
            },
        ),
    ],
)
def test_set_ability(
    pokemon: str,
    stats_to_give: Union[Sequence[int], Dict[str, int]],
) -> None:
    """Test we can set a pokemon's ability."""
    # Get database
    df = read_data()
    # Print current types
    stats = get_stats(df, pokemon)
    logger.info(f"Original stats: {stats}")
    # Change stats
    df = set_pokemon(df, pokemon, stats=stats_to_give)
    # Test change happened
    stats = get_stats(df, pokemon)
    logger.info(f"New stats: {stats}")
    if isinstance(stats_to_give, dict):
        stats_to_give = list(stats_to_give.values())
    for t, xt in zip(list(stats.values()), stats_to_give):
        assert t == xt


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    pytest.main([__file__, "-x", "-s"])
