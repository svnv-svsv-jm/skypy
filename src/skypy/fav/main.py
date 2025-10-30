__all__ = ["main"]

from pathlib import Path

from skypy.fav.mons import mons
from skypy.fav.trainer import trainer
from skypy.fav.waza import waza
from skypy.ops import write_df_to_json, write_trainer_to_json, write_waza_to_json
from skypy.settings import settings
from skypy.utils.nb import pretty_df, pretty_waza


def main() -> None:
    """Run conversion."""
    Path(settings.applied_changes.docs_loc).mkdir(parents=True, exist_ok=True)
    # Waza
    waza_df = waza(anew=True)
    write_waza_to_json(waza_df)
    pretty_waza(waza_df).to_excel(settings.applied_changes.waza_docs_file, header=True)
    # Mons
    personal_df = mons(anew=True)
    write_df_to_json(personal_df)
    pretty_df(personal_df).to_excel(
        settings.applied_changes.personal_docs_file, header=True
    )
    # Trainers
    trainer_df = trainer(anew=True)
    write_trainer_to_json(trainer_df)
