import json
import typer
import logging
import pkgutil
from pathlib import Path

from .... import Rezume, RezumeError
from .. import Command, DEFAULT_FILENAME
from . import itty3


log = logging.getLogger(__name__)


class ServeCommand(Command):
    """Serves a rezume for local viewing applying available themes.
    """

    name = "serve"

    def __init__(self, filename: Path, theme: str, port: int):
        self.filename = filename
        self.theme = theme
        self.port = port

    def get_theme_module(self, theme):
        """Locates and returns rezume theme package/module.
        """
        pkg_name = f"rezume_theme_{theme}"
        infos = list(
            filter(lambda p: p.name.startswith(pkg_name), pkgutil.iter_modules())
        )

        if not infos:
            return None

        [finder, name, _] = infos[0]
        return finder.find_module(name).load_module(name)

    def route_index(self, req):
        """HTTP GET request handler for the root route.
        """
        theme = self.theme
        if req.query and "theme" in req.query:
            theme = req.query["theme"][0]

        try:
            # read rezume on every request to allow showing updates
            rezume = Rezume().load(self.filename)

            module = self.get_theme_module(theme)
            if module and hasattr(module, "render"):
                return self.app.render(req, module.render(rezume))

            # send rezume as json data when theme not available
            json_data = json.dumps(rezume.dump_data())
            return self.app.render(req, json_data, content_type=itty3.JSON)
        except (RezumeError, Exception) as ex:
            log.error(ex)
            return self.app.render(req, f"Internal Server Error: {ex}", 500)

    def _serve_web(self):
        self.app = app = itty3.App(debug=True)
        app.add_route(itty3.GET, "/", self.route_index)
        try:
            app.run(port=self.port, debug=True)
        except KeyboardInterrupt:
            typer.secho("server terminated", fg=typer.colors.RED)

    def run(self) -> None:
        if not self.filename.exists():
            typer.secho(f"Rezume not found: {self.filename}", fg=typer.colors.RED)
            self.exit()

        try:
            self._serve_web()
        except RezumeError as ex:
            typer.secho(f"{ex}\n", fg=typer.colors.RED)

    @staticmethod
    def handler(
        filename: Path = DEFAULT_FILENAME,
        theme: str = typer.Option(  # noqa
            "", show_default=False, help="Theme to apply on rezume"
        ),
        port: int = typer.Option(  # noqa
            7770, help="Port number to serve content to on localhost"
        ),
    ):
        """Serves a rezume for local viewing applying available themes
        """
        command = ServeCommand(filename, theme, port)
        command.run()
