import rezume
from pathlib import Path
from rezume.cli.commands.init import InitCommand


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
