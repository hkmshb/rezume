import typer
from pathlib import Path
from ... import Rezume, RezumeError
from . import Command, DEFAULT_FILENAME


class InitCommand(Command):
    """Initialize a new rezume.yml file
    """

    name = "init"

    def __init__(self, filename: Path):
        self.filename = filename

    def create(self) -> None:
        """Creates a new rezume.yml file based on the template rezume.
        """
        root_dir = Path(__file__).resolve().parents[1]
        template = root_dir / "assets/rezume-template.yml"

        entries = self.get_details()

        try:
            rezume = Rezume()
            rezume.load(template)

            for field, value in entries.items():
                setattr(rezume, field, value)

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

        self.create()

    @staticmethod
    def handler(filename: Path = DEFAULT_FILENAME):
        """Initializes a new rezume.yml file
        """
        command = InitCommand(filename)
        command.run()
