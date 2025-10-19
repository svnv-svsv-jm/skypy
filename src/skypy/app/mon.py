__all__ = ["MonEditor"]

import customtkinter as ctk


class MonEditor(ctk.CTkScrollableFrame):
    """Pokémon editor."""

    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master)
        self.master = master
        self.configure()
        self.create_widgets()

    def create_widgets(self) -> None:
        """Creates widgets."""
        label = ctk.CTkLabel(self, text="Pokémon editor", font=("Helvetica", 18))
        label.pack(pady=20)
