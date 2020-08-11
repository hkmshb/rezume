import sys
import types
from pathlib import Path

import pretend
import pytest
from typer.testing import CliRunner

import rezume
from rezume import Rezume
from rezume.cli import create_app, registry
from rezume.cli.commands.init import InitCommand
from rezume.cli.commands.serve import ServeCommand
from rezume.cli.commands.serve import find_theme_module, render_rezume


def test_presense_of_rezume_template():
    """Checks that packaging includes necessary static assets to function properly.
    """
    root_dir = Path(rezume.__file__).parent
    template = root_dir / "assets/rezume-template.yml"
    assert template.exists()
    assert template.is_file()


def test_init_command_can_access_template():
    """Checks that the init command can access and use the rezume template file.
    """
    template_path = InitCommand.get_template_path()
    assert template_path.exists()
    assert template_path.is_file()


@pytest.mark.parametrize(
    "theme_name, has_result", (("valid", True), ("wo_render", True), ("invalid", False))
)
def test_find_rezume_theme_module(theme_name: str, has_result: bool):
    """Checks that serve command :func:`find_rezume_theme` function can find an installed
    rezume theme by name if it exists or return None otherwise.
    """
    # add path to theme package fixtures to python search path
    path = Path(__file__).parent / "themes"
    sys.path.insert(0, str(path))

    result = find_theme_module(theme_name)
    assert isinstance(result, types.ModuleType) == has_result


@pytest.mark.parametrize(
    "theme_name, has_result",
    (("valid", True), ("wo_render", False), ("invalid", False)),
)
def test_render_rezume(sample_rezume, theme_name, has_result):
    """Checks that serve command :func:`render_rezume` function can render a rezume for a
    specified theme if it exists or return None if theme doesn't exist.
    """
    # add path to theme package fixtures to python search path
    path = Path(__file__).parent / "themes"
    sys.path.insert(0, str(path))

    rezume = Rezume().load_data(sample_rezume)
    result = render_rezume(rezume, theme_name)
    assert isinstance(result, str) == has_result


class TestCommands:
    runner = CliRunner()

    def test_init_with_valid_inputs(self, monkeypatch):
        # stub out InitCommand functions
        init_create = pretend.call_recorder(lambda *a, **kw: None)
        monkeypatch.setattr(InitCommand, "create", init_create)

        # clear registry and add patched command
        registry.clear()
        registry.append(InitCommand)
        registry.append(ServeCommand)

        # invoke command through runner
        inputs = "john\njohn@d.com\n"
        create_calls = pretend.call(name="john", email="john@d.com")

        result = self.runner.invoke(create_app(), ["init"], input=inputs)
        assert result.exit_code == 0
        assert init_create.calls[0].kwargs == create_calls.kwargs

    @pytest.mark.parametrize(
        "args, filename, theme, port",
        [
            (["serve"], "rezume.yml", "", 7770),
            (["serve", "imb.yml"], "imb.yml", "", 7770),
            (
                ["serve", "--theme", "onepage", "--port", 8000],
                "rezume.yml",
                "onepage",
                8000,
            ),
        ],
    )
    def test_serve_with_valid_inputs(self, monkeypatch, args, filename, theme, port):
        # stub out ServeCommand functions
        serve_run = pretend.call_recorder(lambda *a, **kw: None)
        monkeypatch.setattr(ServeCommand, "run", serve_run)

        # clear registry and add patched command
        registry.clear()
        registry.append(InitCommand)
        registry.append(ServeCommand)

        # invoke command through runner
        result = self.runner.invoke(create_app(), args)
        assert result.exit_code == 0

        serve_obj = serve_run.calls[0].args[0]
        assert serve_obj.filename.name == filename
        assert serve_obj.theme == theme
        assert serve_obj.port == port
