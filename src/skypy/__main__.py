import typer

from skypy.utils.logger import set_up_logging
from skypy.za import ZATrainerEditor

# Define app
app = typer.Typer()


@app.command()
def trainer_editor_za() -> None:
    """Launch the ZA Trainer Editor."""
    set_up_logging()
    ui = ZATrainerEditor()
    ui.mainloop()


if __name__ == "__main__":
    app()
