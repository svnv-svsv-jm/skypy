from typing import Any
from loguru import logger

import pandas as pd

from skypy.ops import read_waza
from skypy.ops.setters import set_waza


class WazaEditor:
    """Implements changes."""

    def __init__(
        self,
        waza_df: pd.DataFrame = None,
        runnable_prefix: str = "edit_moves_",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            waza_df (pd.DataFrame):
                Waza table.
            runnable_prefix (str):
                Prefix of methods to be run.
                Methods must return a `pd.DataFrame` and take the Waza table as input.
        """
        if waza_df is None:
            waza_df = read_waza(**kwargs)
        self.waza_df = waza_df
        self.runnable_prefix = runnable_prefix

    def run(self) -> pd.DataFrame:
        """Run all."""
        df: pd.DataFrame = self.waza_df
        # Get all attributes of the object
        all_attributes = dir(self)
        # Filter attributes starting with "foo"
        foo_attributes = [attr for attr in all_attributes if attr.startswith(self.runnable_prefix)]
        # Execute each method starting with "foo"
        for foo_attr in foo_attributes:
            foo_method = getattr(self, foo_attr)
            if callable(foo_method):
                df = foo_method(df)
        # Return
        return df

    def edit_moves_example(self, waza_df: pd.DataFrame) -> pd.DataFrame:
        """Example."""
        logger.debug("Running...")
        return waza_df

    def edit_moves_starters(self, waza_df: pd.DataFrame) -> pd.DataFrame:
        """Example."""
        logger.debug("Running...")
        waza_df = set_waza(
            waza_df, waza="Rock Wrecker", accuracy=100, edits={"flag_rechargeg": False}
        )
        waza_df = set_waza(
            waza_df, waza="blast burn", accuracy=100, edits={"flag_rechargeg": False}
        )
        waza_df = set_waza(
            waza_df, waza="hydro cannon", accuracy=100, edits={"flag_rechargeg": False}
        )
        waza_df = set_waza(
            waza_df, waza="frenzy plant", accuracy=100, edits={"flag_rechargeg": False}
        )
        waza_df = set_waza(waza_df, waza="hydro pump", power=110, accuracy=90)
        waza_df = set_waza(waza_df, waza="fire blast", power=110, accuracy=90)
        waza_df = set_waza(waza_df, waza="thunder", accuracy=85)
        waza_df = set_waza(waza_df, waza="pyro ball", power=90, accuracy=100)  # fuck cinderace
        waza_df = set_waza(waza_df, waza="snipe shot", power=95, accuracy=100)
        waza_df = set_waza(waza_df, waza="Drum Beating", power=90, accuracy=100)
        return waza_df

    def edit_moves_nerfs(self, waza_df: pd.DataFrame) -> pd.DataFrame:
        """Nerf some moves.."""
        logger.debug("Running...")
        return waza_df

    def edit_moves_buffs(self, waza_df: pd.DataFrame) -> pd.DataFrame:
        """Buff some cool moves.."""
        logger.debug("Running...")
        waza_df = set_waza(waza_df, waza="mega punch", power=90, accuracy=100)
        waza_df = set_waza(waza_df, waza="mega kick", power=110, accuracy=100)
        waza_df = set_waza(waza_df, waza="blaze kick", power=85, accuracy=100)
        waza_df = set_waza(waza_df, waza="double kick", power=35, accuracy=100)
        waza_df = set_waza(waza_df, waza="triple kick", power=35, accuracy=100)
        waza_df = set_waza(waza_df, waza="swift", power=80)
        waza_df = set_waza(waza_df, waza="shadow punch", power=75)
        waza_df = set_waza(waza_df, waza="water pulse", power=75)
        waza_df = set_waza(waza_df, waza="aurora beam", power=95)
        waza_df = set_waza(waza_df, waza="water shuriken", power=45)
        waza_df = set_waza(
            waza_df,
            waza="dragon dance",
            edits={
                "stat_amps.fstat1_percent": 3,  # Also increase Sp.Atk
                "stat_amps.fstat2_percent": 1,
                "stat_amps.fstat3_percent": 0,
            },
        )
        waza_df = set_waza(waza_df, waza="dragon pulse", power=95)
        return waza_df

    def edit_moves_accuracy_buffs(self, waza_df: pd.DataFrame) -> pd.DataFrame:
        """Buff accuracy of annoying moves."""
        logger.debug("Running...")
        waza_df = set_waza(waza_df, waza="Aqua Tail", accuracy=100)
        waza_df = set_waza(waza_df, waza="Steel Wing", accuracy=100)
        waza_df = set_waza(waza_df, waza="snarl", accuracy=100)
        waza_df = set_waza(waza_df, waza="icy wind", accuracy=100)
        waza_df = set_waza(waza_df, waza="Chloroblast", accuracy=100, edits={"raw_healing": -10})
        waza_df = set_waza(waza_df, waza="Mountain Gale", accuracy=100)
        waza_df = set_waza(waza_df, waza="Supercell Slam", accuracy=100)
        waza_df = set_waza(waza_df, waza="drill run", accuracy=100)
        waza_df = set_waza(waza_df, waza="zen headbutt", accuracy=100)
        waza_df = set_waza(waza_df, waza="play rough", accuracy=100)
        waza_df = set_waza(waza_df, waza="air slash", accuracy=100)
        waza_df = set_waza(waza_df, waza="dual wingbeat", accuracy=100)
        waza_df = set_waza(waza_df, waza="strange steam", accuracy=100)
        waza_df = set_waza(waza_df, waza="iron tail", accuracy=100)
        # Rock
        waza_df = set_waza(waza_df, waza="rock slide", accuracy=100)
        waza_df = set_waza(waza_df, waza="stone axe", accuracy=100)
        waza_df = set_waza(waza_df, waza="rock tomb", accuracy=100)
        return waza_df

    def edit_moves_signature(self, waza_df: pd.DataFrame) -> pd.DataFrame:
        """Legends/signature moves."""
        waza_df = set_waza(
            waza_df, waza="blood moon", power=110, edits={"flag_cant_use_twice": False}
        )
        waza_df = set_waza(
            waza_df, waza="gigaton hammer", power=130, edits={"flag_cant_use_twice": False}
        )
        waza_df = set_waza(waza_df, waza="meteor mash", accuracy=100)
        waza_df = set_waza(waza_df, waza="night daze", accuracy=100)
        waza_df = set_waza(waza_df, waza="steam eruption", accuracy=100)
        waza_df = set_waza(waza_df, waza="dark void", accuracy=100)
        waza_df = set_waza(waza_df, waza="diamond storm", accuracy=100)
        return waza_df

    def edit_moves_johto(self, waza_df: pd.DataFrame) -> pd.DataFrame:
        """Make Johto legends better."""
        logger.debug("Running...")
        waza_df = set_waza(waza_df, waza="Sacred Fire", accuracy=100)
        waza_df = set_waza(waza_df, waza="Aeroblast", accuracy=100)
        return waza_df

    def edit_moves_genies(self, waza_df: pd.DataFrame) -> pd.DataFrame:
        """Make these Storm moves stronger."""
        logger.debug("Running...")
        waza_df = set_waza(waza_df, waza="Bleakwind Storm", accuracy=100)
        waza_df = set_waza(waza_df, waza="Wildbolt Storm", accuracy=100)
        waza_df = set_waza(waza_df, waza="Sandsear Storm", accuracy=100)
        waza_df = set_waza(waza_df, waza="Springtide Storm", accuracy=100)
        return waza_df

    def edit_moves_punch_fangs(self, waza_df: pd.DataFrame) -> pd.DataFrame:
        """Make punch/fang moves stronger."""
        logger.debug("Running...")
        waza_df = set_waza(waza_df, waza="fire punch", accuracy=100, power=85)
        waza_df = set_waza(waza_df, waza="ice punch", accuracy=100, power=85)
        waza_df = set_waza(waza_df, waza="thunder punch", accuracy=100, power=85)
        waza_df = set_waza(waza_df, waza="fire fang", accuracy=100, power=85)
        waza_df = set_waza(waza_df, waza="ice fang", accuracy=100, power=85)
        waza_df = set_waza(waza_df, waza="thunder fang", accuracy=100, power=85)
        waza_df = set_waza(waza_df, waza="poison fang", accuracy=100, power=85)
        waza_df = set_waza(waza_df, waza="poison tail", accuracy=100, power=85)
        return waza_df

    def edit_moves_stronger_grass_types(self, waza_df: pd.DataFrame) -> pd.DataFrame:
        """Make Grass type moves stronger. Grass types suck!"""
        waza_df = set_waza(waza_df, waza="seed flare", accuracy=100)
        waza_df = set_waza(waza_df, waza="razor leaf", accuracy=100, power=90)
        waza_df = set_waza(waza_df, waza="jungle healing", edits={"raw_healing": 50})
        waza_df = set_waza(waza_df, waza="power whip", accuracy=100)
        waza_df = set_waza(waza_df, waza="vine whip", power=80)
        return waza_df

    def edit_moves_hisuian(self, waza_df: pd.DataFrame) -> pd.DataFrame:
        """Have fun with Hisuian forms' related moves."""
        # Starters
        waza_df = set_waza(waza_df, waza="Ceaseless Edge", power=75, accuracy=100)
        waza_df = set_waza(waza_df, waza="Razor Shell", power=75, accuracy=100)
        waza_df = set_waza(waza_df, waza="infernal parade", power=80)
        # Shelter > Iron Defense
        waza_df = set_waza(
            waza_df,
            waza="shelter",
            edits={
                "stat_amps.fstat1_stage": 4,  # Also increase Sp.Def
                "stat_amps.fstat2_state": 2,  # by +2 stages
                "stat_amps.fstat3_stage": 100,
            },
        )
        return waza_df

    def edit_moves_gods(self, waza_df: pd.DataFrame) -> pd.DataFrame:
        """Make Gods real Gods."""
        logger.debug("Running...")
        waza_df = set_waza(waza_df, waza="lunar blessing", edits={"raw_healing": 50})
        waza_df = set_waza(
            waza_df, waza="Prismatic Laser", accuracy=100, edits={"flag_rechargeg": False}
        )
        waza_df = set_waza(waza_df, waza="magma storm", accuracy=100, power=100)
        waza_df = set_waza(waza_df, waza="glaciate", accuracy=100, power=100)
        waza_df = set_waza(waza_df, waza="psystrike", power=120)
        waza_df = set_waza(waza_df, waza="Origin Pulse", accuracy=100, power=150)
        waza_df = set_waza(waza_df, waza="Precipice Blades", accuracy=100, power=150)
        waza_df = set_waza(
            waza_df,
            waza="Dragon Ascent",
            accuracy=100,
            power=150,
            edits={
                "stat_amps.fstat1": 0,
                "stat_amps.fstat2": 0,
                "stat_amps.fstat3": 0,
                "stat_amps.fstat1_stage": 0,
                "stat_amps.fstat2_state": 0,
                "stat_amps.fstat3_stage": 0,
            },
        )
        waza_df = set_waza(waza_df, waza="Spacial Rend", accuracy=100, power=150)
        waza_df = set_waza(
            waza_df, waza="Roar of Time", accuracy=100, edits={"flag_rechargeg": False}
        )
        waza_df = set_waza(
            waza_df,
            waza="Judgment",
            power=180,
            accuracy=101,
            inflicts="confusion",
            inflict_chance=25,
            edits={"flinch": 30},
        )
        return waza_df


def waza(waza_df: pd.DataFrame = None, **kwargs: Any) -> pd.DataFrame:
    """Waza."""
    if waza_df is None:
        waza_df = read_waza(**kwargs)
    # Run
    move_editor = WazaEditor(waza_df)
    waza_df = move_editor.run()
    # Exit
    return waza_df
