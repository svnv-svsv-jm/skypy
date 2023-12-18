from skypy.ops import write_df_to_json, write_waza_to_json, write_trainer_to_json
from skypy.fav.waza import waza
from skypy.fav.mons import mons
from skypy.fav.trainer import trainer
from skypy.utils.nb import nb_init


def main() -> None:
    """Run."""
    # Waza
    waza_df = waza(anew=True)
    write_waza_to_json(waza_df)
    # Mons
    personal_df = mons(anew=True)
    write_df_to_json(personal_df)
    # Trainers
    trainer_df = trainer(anew=True)
    write_trainer_to_json(trainer_df)


if __name__ == "__main__":
    nb_init(logger_level="DEBUG")
    main()
