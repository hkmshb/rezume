import typer
from pathlib import Path
from .. import Rezume, RezumeError


app = typer.Typer()

# defaults
DEFAULT_FILENAME = typer.Argument(Path("./rezume.yml"))


class Command:
    """Represents the class for all rezume commands
    """

    def run(self) -> None:
        """Executes the logic for a command.
        """
        raise NotImplementedError()


class InitCommand:
    """Initialize a new rezume.yml file
    """

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

            rezume.save(self.filename, True)
            typer.secho(
                f"\nYour {self.filename.name} file has been created!\n",
                fg=typer.colors.GREEN,
            )
        except RezumeError as ex:
            typer.secho(f"\nerror: {ex}")
            raise typer.Exit()

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
                raise typer.Exit()

        self.create()

    @staticmethod
    @app.command("init")
    def handler(filename: Path = DEFAULT_FILENAME):
        """Initializes a new rezume.yml file
        """
        command = InitCommand(filename)
        command.run()


class TestCommand:
    """Validates correctness of a rezume.yml file
    """

    def __init__(self, filename: Path):
        self.filename = filename

    def run(self) -> None:
        if not self.filename.exists():
            typer.secho(f"Rezume not found: {self.filename}", fg=typer.colors.RED)
            raise typer.Exit()

        try:
            Rezume().load(self.filename)
            typer.secho("Valid!\n", fg=typer.colors.GREEN)
        except RezumeError as ex:
            typer.secho(f"{ex}\n", fg=typer.colors.RED)

    @staticmethod
    @app.command("test")
    def handler(filename: Path = DEFAULT_FILENAME):
        """Validates correctness of a rezume.yml file
        """
        command = TestCommand(filename)
        command.run()
