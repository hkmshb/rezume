import typer
from .commands import registry


def main():
    app = typer.Typer()

    for cmd in registry:
        if hasattr(cmd, "name") and hasattr(cmd, "handler"):
            app.command(cmd.name)(cmd.handler)

    app()


if __name__ == "__main__":
    main()
