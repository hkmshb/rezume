from pathlib import Path

import pytest
from pydantic import ValidationError

from rezume import Rezume, RezumeError, get_version
from rezume.models import Education, Experience


def test_version():
    version = get_version()
    assert version is not None
    assert len(version.split(".")) == 3


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
            item = Education(institution="edX", area="humanity", start_date="2020-07-05")
            rezume.add_item("work", item)

    @pytest.mark.skip(msg="restore when resume uses generic section")
    def test_removing_item_from_wrong_section_fails(self):
        rezume = Rezume()

        item = Education(institution="edX", area="humanity", start_date="2020-07-05")
        rezume.add_item("education", item)

        with pytest.raises(RezumeError):
            rezume.discard_item("work", item)

    def test_loading_malformed_non_optional_rezume_data_fails(self, sample_rezume):
        del sample_rezume["basics"]["location"]

        rezume = Rezume()
        with pytest.raises(ValidationError):
            rezume.load_data(sample_rezume)

    def test_can_load_wellformed_non_optional_rezume_data(self, sample_rezume):
        try:
            rezume = Rezume()
            assert len(rezume.profiles) == 0
            assert len(rezume["education"]) == 0

            rezume.load_data(sample_rezume)
            assert len(rezume.profiles) == 1
            assert len(rezume["education"]) == 1
        except Exception as ex:
            pytest.fail(f"Exception not expected: {ex}")

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

    def test_save_fails_without_overwrite_to_existing_file(self, rezume_mini):
        rezume = Rezume()
        rezume.load(rezume_mini)

        with pytest.raises(RezumeError):
            rezume.save(rezume_mini)

    def test_can_save_to_exiting_file_with_overwrite(self, rezume_mini):
        rezume = Rezume()
        rezume.load(rezume_mini)

        try:
            rezume.save(rezume_mini, True)
        except Exception as ex:
            pytest.fail(f"Exception not expected: {ex}")

    def test_load_acts_fluent_by_returning_instance(self, rezume_mini):
        rezume = Rezume().load(rezume_mini)
        assert rezume is not None

    def test_load_data_acts_fluent_by_returning_instance(self, sample_rezume):
        rezume = Rezume().load_data(sample_rezume)
        assert rezume is not None

    def test_personal_details_are_validated_on_dump(self):
        rezume = Rezume()
        rezume.name = "John"
        rezume.email = "john"

        with pytest.raises(ValidationError):
            rezume.dump_data()

    def test_rezume_is_validate_before_dump(self, sample_rezume):
        rezume = Rezume().load_data(sample_rezume)
        section = rezume["education"]

        assert section is not None
        assert len(section) > 0

        entry = list(section)[0]
        section.discard(entry)

        assert len(section) == 0

        # a valid rezume is expected to have at least one entry in the
        # education section in addition to all required basics details
        with pytest.raises(RezumeError):
            rezume.dump_data()

    def test_can_validate_file_via_validate_api(self, rezume_mini):
        try:
            Rezume.validate(rezume_mini)
        except Exception as ex:
            pytest.fail(f"Exception not expected: {ex}")

    def test_can_validate_data_via_validate_api(self, sample_rezume):
        try:
            Rezume.validate(sample_rezume)
        except Exception as ex:
            pytest.fail(f"Exception not expected: {ex}")

    def test_can_validate_file_via_is_valid_api(self, rezume_mini):
        assert Rezume.is_valid(rezume_mini) is True

    def test_can_validate_data_via_is_valid_api(self, sample_rezume):
        assert Rezume.is_valid(sample_rezume) is True
