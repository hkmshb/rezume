import pytest
from pathlib import Path
from pydantic import ValidationError

from rezume import get_version, Rezume, RezumeError
from rezume.models import Education, Experience


def test_version():
    assert get_version() == "0.4.0"


class TestResume:
    def test_instance_is_prepopulated_with_data_sections(self):
        rezume = Rezume()
        assert len(rezume) > 0

    def test_adding_item_to_unknown_section_fails(self):
        rezume = Rezume()
        with pytest.raises(RezumeError):
            rezume.add_item("-work-", Experience.construct())

    def test_removing_item_from_unknown_section_fails(self):
        rezume = Rezume()
        with pytest.raises(RezumeError):
            rezume.discard_item("-work-", Experience.construct())

    def test_can_add_item_to_known_section(self):
        try:
            rezume = Rezume()
            section_name = "education"
            assert len(rezume[section_name]) == 0

            item = Education(institution="edX", area="humanity", startDate="2020-07-05")
            rezume.add_item(section_name, item)
            assert len(rezume[section_name]) == 1
        except Exception:
            pytest.fail("Exception not expected")

    @pytest.mark.skip(msg="restore when resume uses generic section")
    def test_adding_item_to_wrong_section_fails(self):
        rezume = Rezume()
        with pytest.raises(RezumeError):
            item = Education(
                institution="edX", area="humanity", start_date="2020-07-05"
            )
            rezume.add_item("work", item)

    @pytest.mark.skip(msg="restore when resume uses generic section")
    def test_removing_item_from_wrong_section_fails(self):
        rezume = Rezume()

        item = Education(institution="edX", area="humanity", start_date="2020-07-05")
        rezume.add_item("education", item)

        with pytest.raises(RezumeError):
            rezume.discard_item("work", item)

    def test_loading_malformed_non_optional_rezume_data_fails(self):
        data = {
            "basics": {  # missing location
                "name": "John Doe",
                "label": "Programmer",
                "email": "john@doe.com",
                "phone": "0807-0000-1111",
                "website": "http://johndoe.com",
                "summary": "A summary of john doe...",
                "profiles": [
                    {
                        "network": "twitter",
                        "username": "john",
                        "url": "http://twitter.com/john",
                    }
                ],
            },
            "education": [
                {
                    "institution": "University",
                    "area": "Bachelor",
                    "startDate": "2020-07-05",
                }
            ],
        }

        rezume = Rezume()
        with pytest.raises(ValidationError):
            rezume.load_data(data)

    def test_can_load_wellformed_non_optional_rezume_data(self):
        data = {
            "basics": {
                "name": "John Doe",
                "label": "Programmer",
                "email": "john@doe.com",
                "phone": "0807-0000-1111",
                "website": "http://johndoe.com",
                "summary": "A summary of john doe...",
                "location": {
                    "address": "276 Alu Avenue",
                    "postal_code": "KN 700214",
                    "city": "Kano",
                    "region": "Kano State",
                    "country_code": "NG",
                },
                "profiles": [
                    {
                        "network": "twitter",
                        "username": "john",
                        "url": "http://twitter.com/john",
                    }
                ],
            },
            "education": [
                {
                    "institution": "University",
                    "area": "Software Engineering",
                    "startDate": "2020-07-05",
                }
            ],
        }

        try:
            rezume = Rezume()
            assert len(rezume.profiles) == 0
            assert len(rezume["education"]) == 0

            rezume.load_data(data)
            assert len(rezume.profiles) == 1
            assert len(rezume["education"]) == 1
        except Exception:
            pytest.fail("Exception not expected")

    @pytest.mark.parametrize(
        "filepath",
        [
            "./non-existing-dir/rezume.yml",
            "./tests/fixtures/rezume-malformed.yml",
            "./tests/fixtures/rezume-empty.yml",
        ],
    )
    def test_fails_for_invalid_file(self, filepath):
        rezume = Rezume()
        with pytest.raises(RezumeError):
            rezume.load(filepath)

    @pytest.mark.parametrize(
        "filepath",
        ["./tests/fixtures/rezume-mini.yml", "./src/rezume/assets/rezume-template.yml"],
    )
    def test_can_load_valid_file(self, filepath):
        rezume = Rezume()
        rezume.load(filepath)

        try:
            assert len(rezume.profiles) == 1
            assert len(rezume["education"]) == 1
        except Exception:
            pytest.fail("Exception not expected")

    def test_can_save_to_non_existing_file(self):
        rezume = Rezume()
        rezume.load("./src/rezume/assets/rezume-template.yml")

        fpath = Path("./tests/fixtures/rezume-saved.yml.log")
        if fpath.exists():
            fpath.unlink()
        assert not fpath.exists()

        rezume.save(fpath)
        assert fpath.exists()

        loaded = Rezume()
        loaded.load(fpath)
        assert len(rezume.profiles) == 1
        assert len(rezume["education"]) == 1

    def test_save_fails_without_overwrite_to_existing_file(self):
        rezume = Rezume()
        fpath = Path("./tests/fixtures/rezume-mini.yml")

        rezume.load(fpath)
        with pytest.raises(RezumeError):
            rezume.save(fpath)

    def test_can_save_to_exiting_file_with_overwrite(self):
        rezume = Rezume()
        fpath = Path("./tests/fixtures/rezume-mini.yml")

        rezume.load(fpath)
        try:
            rezume.save(fpath, True)
        except Exception as ex:
            pytest.fail(f"Exception not expected: {ex}")

    def test_personal_details_are_validated_on_dump(self):
        rezume = Rezume()
        rezume.name = "John"
        rezume.email = "john"

        with pytest.raises(ValidationError):
            rezume.dump_data()
