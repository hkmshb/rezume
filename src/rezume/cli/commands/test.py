import typer
from pathlib import Path
from ... import Rezume, RezumeError
from . import Command, DEFAULT_FILENAME


class TestCommand(Command):
    """Validates correctness of a rezume.yml file
    """

    name = "test"

    def __init__(self, filename: Path):
        self.filename = filename

    def run(self) -> None:
        if not self.filename.exists():
            typer.secho(f"Rezume not found: {self.filename}", fg=typer.colors.RED)
            self.exit()

        try:
            Rezume.validate(self.filename)
            typer.secho("Rezume is valid!\n", fg=typer.colors.GREEN)
        except RezumeError as ex:
            typer.secho(f"{ex}\n", fg=typer.colors.RED)

    @staticmethod
    def handler(filename: Path = DEFAULT_FILENAME):
        """Validates correctness of a rezume.yml file
        """
        command = TestCommand(filename)
        command.run()
