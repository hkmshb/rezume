import sys
import types
from pathlib import Path

import pytest

import rezume
from rezume import Rezume
from rezume.cli.commands.init import InitCommand
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
