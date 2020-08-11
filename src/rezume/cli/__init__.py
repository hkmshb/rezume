import typer
from .commands import registry


def create_app():
    app = typer.Typer()
    for cmd in registry:
        if hasattr(cmd, "name") and hasattr(cmd, "handler"):
            app.command(cmd.name)(cmd.handler)

    return app


def main():
    app = create_app()
    app()


if __name__ == "__main__":
    main()
