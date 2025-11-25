import typer
from loguru import logger

from skypy.app import App
from skypy.fav.main import main as _apply
from skypy.utils.logger import set_up_logging

# Define app
app = typer.Typer()


@app.command()
def apply() -> None:
    """Main app."""
    logger.trace("Creating app...")
    _apply()


@app.command()
def ui() -> None:
    """Run UI."""
    app_ui = App()
    app_ui.mainloop()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Default command."""
    logger.info(f"About to execute command: {ctx.invoked_subcommand}")
    if ctx.invoked_subcommand is None:
        ui()


if __name__ == "__main__":
    set_up_logging()
    app()
