__all__ = ["App"]

import typing as ty
from loguru import logger
import tkinter as tk
import customtkinter as ctk
from pandastable import Table, TableModel

from .waza import MoveEditor


class App(ctk.CTk):
    """App."""

    def __init__(self, *args: ty.Any, **kwargs: ty.Any) -> None:
        """."""
        super().__init__(*args, **kwargs)
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        self.frame = MoveEditor(master=self)
        self.frame.pack()  # grid(row=0, column=0, sticky="nsew")
