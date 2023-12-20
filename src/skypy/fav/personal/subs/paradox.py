__all__ = ["ParadoxEditor"]

import typing as ty
from loguru import logger

import pandas as pd

from skypy.ops import add_move, set_pokemon, add_evo
from skypy.const.pkmn import POKEMON
from skypy.fav.personal.base import PersonalEditor


class ParadoxEditor(PersonalEditor):
    """ParadoxEditor."""

    def __init__(self, **kwargs: ty.Any) -> None:
        """Just call superclass."""
        super().__init__(**kwargs)

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        # Iron Boulder
        pokemon = "Iron Boulder"
        df = set_pokemon(df, pokemon, ability="Filter")
        # Iron Crown
        pokemon = "Iron Crown"
        df = set_pokemon(df, pokemon, ability="Filter")
        # Raging Bolt
        pokemon = "Raging Bolt"
        df = set_pokemon(df, pokemon, ability="Volt Absorb")
        # Gouging Fire
        pokemon = "Gouging Fire"
        df = set_pokemon(df, pokemon, ability="Flash Fire")
        # Iron Valiant
        p = "Iron Valiant"
        df = set_pokemon(df, p, ability="Magic Guard")
        # Iron Bundle
        p = "Iron Bundle"
        df = set_pokemon(df, p, ability="Adaptability")
        # Iron Thorns
        p = "Iron Thorns"
        df = set_pokemon(df, p, ability="Sand Stream")
        # Iron Jugulis
        p = "Iron Jugulis"
        df = set_pokemon(df, p, ability="No Guard")
        # Iron Hands
        p = "Iron Hands"
        df = set_pokemon(df, p, ability="Scrappy")
        # Iron Moth
        p = "Iron Moth"
        df = set_pokemon(df, p, ability="Flash Fire")
        # Iron Leaves
        p = "Iron Leaves"
        df = set_pokemon(df, p, ability="Filter")
        # Iron Treads
        p = "Iron Treads"
        df = set_pokemon(df, p, ability="Earth Eater")
        # Roaring Moon
        p = "Roaring Moon"
        df = set_pokemon(df, p, ability="Levitate")
        # Slither Wing
        p = "Slither Wing"
        df = set_pokemon(df, p, ability="Scrappy")
        # Flutter Mane
        p = "Flutter Mane"
        df = set_pokemon(df, p, ability="Levitate")
        # Scream Tail
        p = "Scream Tail"
        df = set_pokemon(df, p, ability="Levitate")
        # Sandy Shocks
        p = "Sandy Shocks"
        df = set_pokemon(df, p, ability="Earth Eater")
        # Walking Wake
        p = "Walking Wake"
        df = set_pokemon(df, p, ability="Water Absorb")
        # Brute Bonnet
        p = "Brute Bonnet"
        df = set_pokemon(df, p, ability="Effect Spore")
        # Great Tusk
        p = "Great Tusk"
        df = set_pokemon(df, p, ability="Scrappy")
        return df
