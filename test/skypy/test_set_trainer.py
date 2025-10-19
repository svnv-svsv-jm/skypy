import pytest, sys, os, typing as ty
from loguru import logger
import json

import pandas as pd

from skypy.schemas import TrainerPokemonSchema, TrainerSchema
from skypy.ops.getters import get_trainer
from skypy.ops.setters import set_trainer
from skypy.ops import read_trainer, read_trdevid, read_trainer_map


def test_trainer_schema() -> None:
    """."""
    df = read_trainer()
    devid = read_trdevid()
    logger.info(devid.head())
    schema = TrainerPokemonSchema(level=12, devId="DEV_HUSIGIDANE")
    logger.info(schema)
    with pytest.raises(ValueError):
        schema = TrainerPokemonSchema(level=12, devId="asfafasf")
        logger.info(schema)
    with pytest.raises(ValueError):
        schema = TrainerPokemonSchema(level=-1, devId="DEV_HUSIGIDANE")
        logger.info(schema)
    trainerschema = TrainerSchema()
    trainer_dict = trainerschema.to_dict()
    logger.info(json.dumps(trainer_dict, indent=2))
    for c in df.columns:
        assert c in trainer_dict


def test_set_trainer() -> None:
    """Test."""
    # Get database
    df = read_trainer()
    logger.info(f"df:\n{df.loc[1]}")
    # Get mapping
    tr_map = read_trainer_map()
    logger.info(f"tr_map:\n{tr_map.loc[1]}")
    # Get data
    trdevid = "area01_trainer_cleaning"
    trainer_data = get_trainer(df, trdevid=trdevid)
    logger.info(f"trainer_data:\n{trainer_data}")
    # Change trainer
    moneyRate = 16
    df = set_trainer(df, trdevid, edits={"moneyRate": moneyRate})
    trainer_data = get_trainer(df, trdevid=trdevid)
    assert isinstance(trainer_data, pd.DataFrame)
    val = trainer_data["moneyRate"].values[0]
    logger.info(f"moneyRate: {val}")
    assert val == moneyRate


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    pytest.main([__file__, "-x", "-s"])
