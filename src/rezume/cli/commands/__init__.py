import typer
from typing import Any
from pathlib import Path


# CONSTANTS
DEFAULT_FILENAME: Any = typer.Argument(Path("./rezume.yml"))


class Command:
    """Represents the class for all rezume commands"""

    def exit(self) -> None:
        """Raise typer Exit exception which terminates a running typer app."""
        raise typer.Exit()

    def run(self) -> None:
        """Executes the logic for a command."""
        raise NotImplementedError()


# flake8: noqa
from .init import InitCommand
from .test import TestCommand
from .serve import ServeCommand

registry = [Command, InitCommand, TestCommand, ServeCommand]
