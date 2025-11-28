__all__ = ["create_trdata_mod", "apply_trdata_mod"]

from loguru import logger

from skypy.schemas import ZATrainerDataArray


def create_trdata_mod(zatrdata: ZATrainerDataArray, path: str) -> None:
    """Create the `trdata` mod."""
    apply_trdata_mod(zatrdata)
    # Finally
    logger.trace(f"Dumping data to {path}...")
    zatrdata.dump(path)
    logger.trace(f"Data dumped to {path}.")


def apply_trdata_mod(zatrdata: ZATrainerDataArray) -> None:
    """Apply the `trdata` mod."""
    logger.trace("Applying `trdata` mod...")

    # Edit trainer
    name = "00_test_data"
    trainer = zatrdata.get_trainer(name)
    trainer.poke_1.level = 100
    zatrdata.set_trainer(name, trainer)

    logger.trace("`trdata` mod applied.")
