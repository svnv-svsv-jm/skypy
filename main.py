import os
from pathlib import Path

from skypy.ops import write_df_to_json, write_waza_to_json, write_trainer_to_json
from skypy.fav.waza import waza
from skypy.fav.mons import mons
from skypy.fav.trainer import trainer
from skypy.utils.nb import nb_init, pretty_waza, pretty_df

DOCS_LOC = "docs"
WAZA_DOCS = os.path.join(DOCS_LOC, "waza.xlsx")
PERSONAL_DOCS = os.path.join(DOCS_LOC, "personal.xlsx")


def main() -> None:
    """Run."""
    Path(DOCS_LOC).mkdir(parents=True, exist_ok=True)
    # Waza
    waza_df = waza(anew=True)
    write_waza_to_json(waza_df)
    pretty_waza(waza_df).to_excel(WAZA_DOCS, header=True)
    # Mons
    personal_df = mons(anew=True)
    write_df_to_json(personal_df)
    pretty_df(personal_df).to_excel(PERSONAL_DOCS, header=True)
    # Trainers
    trainer_df = trainer(anew=True)
    write_trainer_to_json(trainer_df)


if __name__ == "__main__":
    nb_init(logger_level="DEBUG")
    main()
