import typer
from loguru import logger

from skypy.utils.logger import set_up_logging

# Define app
app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Default command."""
    set_up_logging()
    logger.info(f"About to execute command: {ctx.invoked_subcommand}")


if __name__ == "__main__":
    app()
