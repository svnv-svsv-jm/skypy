import tkinter as tk
import customtkinter as ctk

from skypy.utils.nb import nb_init, pretty_waza
from skypy.app import App

# MAIN
if __name__ == "__main__":
    nb_init(logger_level="DEBUG")
    # Start app
    app = App()
    app.mainloop()
