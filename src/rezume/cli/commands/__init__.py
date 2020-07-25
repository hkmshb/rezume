import typer
from typing import Any
from pathlib import Path


# CONSTANTS
DEFAULT_FILENAME: Any = typer.Argument(Path("./rezume.yml"))


class Command:
    """Represents the class for all rezume commands
    """

    def run(self) -> None:
        """Executes the logic for a command.
        """
        raise NotImplementedError()


# flake8: noqa
from .init import InitCommand
from .test import TestCommand

registry = [Command, InitCommand, TestCommand]
