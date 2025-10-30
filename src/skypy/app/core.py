__all__ = ["App"]

import tkinter as tk
import typing as ty

import customtkinter as ctk

from .mon import MonEditor


class App(ctk.CTk):
    """App."""

    def __init__(self, *args: ty.Any, **kwargs: ty.Any) -> None:
        """Init."""
        super().__init__(*args, **kwargs)
        self.title("Sky-py")
        self.geometry("400x300")
        self.move_editor = MonEditor(self)
        self.move_editor.pack(fill=tk.BOTH, expand=True)
        self.mon_editor = MonEditor(self)
        self.mon_editor.pack(fill=tk.BOTH, expand=True)
        self.mon_editor.forget()  # Hide frame 2 initially
        self.create_buttons()

    def create_buttons(self) -> None:
        """Create buttons to switch between frames."""
        button_frame1 = tk.Button(
            self, text="Pokémon Editor", command=self.show_mon_editor
        )
        button_frame1.pack(side=tk.LEFT, padx=10, pady=10)
        button_frame2 = tk.Button(
            self, text="Move Editor", command=self.show_move_editor
        )
        button_frame2.pack(side=tk.RIGHT, padx=10, pady=10)

    def show_move_editor(self) -> None:
        """Go to Move Editor."""
        self.mon_editor.forget()
        self.move_editor.pack(fill=tk.BOTH, expand=True)

    def show_mon_editor(self) -> None:
        """Go to Pokémon Editor."""
        self.move_editor.forget()
        self.mon_editor.pack(fill=tk.BOTH, expand=True)
