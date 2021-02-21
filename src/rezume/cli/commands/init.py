import sys
from pathlib import Path

import typer
from pydantic import EmailStr

from ... import Rezume, RezumeError
from . import DEFAULT_FILENAME, Command


class InitCommand(Command):
    """Initialize a new rezume.yml file"""

    name = "init"

    def __init__(self, filename: Path):
        self.filename = filename

    def create(self, name: str, email: str) -> None:
        """Creates a new rezume.yml file based on the template rezume."""
        template_path = InitCommand.get_template_path()
        if not template_path.exists():
            typer.secho("\nrezume template file not found.\n", fg=typer.colors.RED)
            self.exit()

        try:
            rezume = Rezume()
            rezume.load(template_path)

            rezume.name = name
            rezume.email = EmailStr(email)

            rezume.save(self.filename, overwrite=True, exclude_none=True)
            typer.secho(
                f"\nYour {self.filename.name} file has been created!\n",
                fg=typer.colors.GREEN,
            )
        except RezumeError as ex:
            typer.secho(f"\nerror: {ex}")
            self.exit()

    def get_details(self) -> dict:
        typer.secho(
            f"\nThis will generate a {self.filename.name} file in your current working "
            "directory. \nFill out your name and email to get started.\n",
            fg=typer.colors.BLUE,
        )

        fields = {}
        for field in ["name", "email"]:
            value = typer.prompt(field)
            if value:
                fields[field] = value.strip()
        return fields

    def run(self) -> None:
        """
        Executes logic to initialize a new rezume.yml file.
        """
        if self.filename.exists():
            typer.secho(
                "\nA rezume.yml already exist in this directory", fg=typer.colors.YELLOW
            )
            overwrite = typer.confirm("Do you want to overwrite?")
            if not overwrite:
                self.exit()

        entries = self.get_details()
        self.create(**entries)

    @staticmethod
    def get_template_path() -> Path:
        """Returns path to rezume-template.yml file."""
        rezume_module = sys.modules["rezume"]

        root_dir = Path(rezume_module.__file__).parent
        return root_dir / "assets/rezume-template.yml"

    @staticmethod
    def handler(filename: Path = DEFAULT_FILENAME):
        """Initializes a new rezume.yml file"""
        command = InitCommand(filename)
        command.run()
