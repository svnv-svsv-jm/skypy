from skypy.ops import (
    get_pokemon,
    add_move,
    get_learnset,
    read_data,
    resume_pokemon,
    write_df_to_json,
    set_pokemon,
    read_waza,
    resume_waza,
    write_waza_to_json,
    get_waza,
    set_waza,
)
from .waza import waza
from .mons import mons


def main() -> None:
    """Run."""
    waza()
    mons()


if __name__ == "__main__":
    main()
