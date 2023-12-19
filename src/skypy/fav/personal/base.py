from typing import Any, List
from loguru import logger

import pandas as pd

from skypy.utils import get_all_subclasses
from skypy.ops import read_data


class PersonalEditor:
    """Implements changes."""

    def __init__(
        self,
        df: pd.DataFrame = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            df (pd.DataFrame):
                Personal table.
        """
        if df is None:
            df = read_data(**kwargs)
        self.df = df

    def run(self) -> pd.DataFrame:
        """Run all."""
        # Table
        df: pd.DataFrame = self.df
        # Get all subclasses
        all_classes = get_all_subclasses(self.__class__)
        # For each subclass, call the `edit_personal` method
        for klass in all_classes:
            obj: PersonalEditor = klass(self.df)
            df = obj(df)
        # Return
        return df

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        """Main entrypoint."""
        # Get table
        if df is None:
            df = self.df
        # Run
        df = self.edit_personal(df)
        return df

    def edit_personal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement this."""
        raise NotImplementedError("Implement this method.")
