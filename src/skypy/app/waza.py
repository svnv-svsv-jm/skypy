__all__ = ["MoveEditor"]

import typing as ty
from loguru import logger
import tkinter as tk
import customtkinter as ctk
import copy
import pandas as pd
from pandastable import Table, TableModel

from skypy.utils.nb import nb_init, pretty_waza
from skypy.const import ABILITIES, POKEMON, TYPES, MOVES
from skypy.ops import resume_waza, read_waza, write_waza_to_json, set_waza
from .utils import to_bin


class MoveEditor(ctk.CTkScrollableFrame):
    """Move editor."""

    def __init__(self, master: tk.Tk, **kwargs: ty.Any) -> None:
        """
        Args:
            master (tk.Tk): Main app.
        """
        super().__init__(master, **kwargs)
        self.master = master
        self.master.title("Move editor")
        self.master.geometry("1200x500")
        self.df = read_waza()
        logger.debug(f"Got {self.df.head()}")
        # Attributes
        self.moves = list(copy.deepcopy(MOVES))
        self.moves.sort()
        # Init selected item var
        self.selected_item: str = ""
        # Create widgets/grid
        self.create_widgets()
        # Populate initial list
        self.populate_list()

    def create_widgets(self) -> None:
        """Creates all necessary widgets."""
        # Create an entry box
        self.waza_entry = tk.Entry(self.master)
        self.waza_entry.pack(side="top")
        self.waza_entry.bind("<KeyRelease>", func=self.__check)
        # Waza list (listbox)
        self.waza_list = tk.Listbox(self.master, height=22, width=50, border=0)
        self.waza_list.pack(side="left", expand=False)
        self.scrollbar = ctk.CTkScrollbar(self.master)
        self.scrollbar.pack(side="left", expand=False)
        self.waza_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.waza_list.yview)
        self.waza_list.bind("<<ListboxSelect>>", self.__select_item)
        # Create data info
        self.move_info_frame = ctk.CTkScrollableFrame(self.master)
        self.move_info_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.move_info_labels: ty.Dict[str, ctk.CTkLabel] = {}
        self.move_info_entries: ty.Dict[str, ctk.CTkEntry] = {}
        for c in self.df.columns:
            self.move_info_labels[c] = ctk.CTkLabel(self.move_info_frame, text=c)
            self.move_info_labels[c].pack()
            self.move_info_entries[c] = ctk.CTkEntry(
                self.move_info_frame, textvariable=ctk.Variable(name=c, value="")
            )
            self.move_info_entries[c].bind("<Return>", command=self.__update_df)
            self.move_info_entries[c].pack()
        # Create save button
        self.save_button = ctk.CTkButton(self.master, text="Save", command=self.__save)
        self.save_button.pack()

    def populate_list(self) -> None:
        """Populate list."""
        # Delete items before update. So when you keep pressing it doesnt keep getting (show example by calling this twice)
        self.waza_list.delete(0, tk.END)
        # Loop through records
        for row in self.moves:
            # Insert into list
            self.waza_list.insert(tk.END, row)

    def __select_item(self, event: tk.Event) -> None:
        """Runs when item is selected."""
        logger.debug(event)
        # Delete whatever is in the entry box
        self.waza_entry.delete(0, tk.END)
        try:
            # Get index
            index = self.waza_list.curselection()[0]  # type: ignore
            # Get selected item
            self.selected_item = self.waza_list.get(index)
            logger.debug(self.selected_item)
            # Show move info
            self.show_move_info()
        except IndexError:
            pass
        # Add clicked list item to entry box
        self.waza_entry.insert(0, self.waza_list.get(tk.ACTIVE))

    def __update(self, data: ty.List[str]) -> None:
        """Update the listbox."""
        # Clear the listbox
        self.waza_list.delete(0, tk.END)
        # Add toppings to listbox
        for item in data:
            self.waza_list.insert(tk.END, item)

    def __check(self, event: tk.Event) -> None:
        """Create function to check entry vs listbox."""
        logger.debug(event)
        # grab what was typed
        typed = self.waza_entry.get()
        if typed == "":
            data = self.moves
        else:
            data = []
            for item in self.moves:
                if typed.lower() in item.lower():
                    data.append(item)
        # update our listbox with selected items
        self.__update(data)

    def __update_df(self, event: tk.Event) -> None:
        """Update waza data with value in entry."""
        logger.debug(event)
        edits = {}
        for key, entry in self.move_info_entries.items():
            # Cannot change move_id
            if key.lower() in ["move_id"]:
                continue
            value = entry.get()
            # Need to convert type from str to int
            if key.lower() in ["type"]:
                for i, t in TYPES.items():
                    if t.lower() == value.lower():
                        value = i
                        break
            edits[key] = value
        logger.debug(f"Changing move {self.selected_item} with:\n{edits}")
        self.df = set_waza(self.df, self.selected_item, edits=edits)
        logger.debug(f"{self.df.head()}")

    def __save(self) -> None:
        """Save Dataframe."""
        logger.debug("Saving...")
        write_waza_to_json(self.df)
        to_bin()

    def show_move_info(self) -> None:
        """Show move info."""
        df = self.load_waza_table()
        idx = pd.Series(MOVES) == self.selected_item
        df = df.loc[idx]
        for c in self.df.columns:
            v = df[c].values[0]
            self.move_info_entries[c].delete(0, tk.END)
            self.move_info_entries[c].insert(0, v)

    def load_waza_table(self) -> pd.DataFrame:
        """Load pretty waza table."""
        df = resume_waza(self.df, self.selected_item)
        df["move_id"] = pd.Series(MOVES)
        df["type"] = self.df["type"].apply(lambda x: TYPES[x]).astype("string")
        return df
        # self.waza_table = Table(
        #     f,
        #     dataframe=df.transpose(),
        #     editable=True,
        #     showtoolbar=True,
        #     showstatusbar=True,
        # )
        # self.waza_table.show()
        # canvas = tk.Canvas(f)
        # frame = tk.Frame(canvas)
        # myscrollbar = tk.Scrollbar(f, orient="vertical", command=canvas.yview)
        # canvas.configure(yscrollcommand=myscrollbar.set)
        # myscrollbar.pack(side="right", fill="y")
        # canvas.pack(side="left")
        # canvas.create_window((0, 0), window=frame, anchor="nw")
        # frame.bind(
        #     "<Configure>", lambda: canvas.configure(scrollregion=canvas.bbox("all"), width=200, height=200)  # type: ignore
        # )
        # for c in df.columns:
        #     tk.Label(frame, text=c).pack(side="bottom")
