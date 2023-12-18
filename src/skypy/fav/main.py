import sys
from loguru import logger

from skypy.ops import write_df_to_json, write_waza_to_json
from skypy.fav.waza import waza
from skypy.fav.mons import mons


def main() -> None:
    """Run."""
    # Waza
    waza_df = waza(anew=True)
    write_waza_to_json(waza_df)
    # Mons
    personal_df = mons(anew=True)
    write_df_to_json(personal_df)


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
    main()
