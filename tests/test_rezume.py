from rezume import get_version


def test_version():
    assert get_version() == "0.1.0"
