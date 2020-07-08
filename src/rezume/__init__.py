import pkg_resources
from pathlib import Path
from .models import Rezume as RezumeModel
from .sections import (
    EducationSet,
    ExperienceSet,
    LanguageSet,
    NamedKeywordsSet,
    RezumeBase,
)


def get_version():
    """Retrieves and returns the package version details.
    """
    package = pkg_resources.require("rezume")
    return package[0].version


class Rezume(RezumeBase):
    """Represents a resume.
    """

    FIELDS = [
        "name",
        "email",
        "label",
        "location",
        "phone",
        "picture",
        "summary",
        "website",
    ]

    SECTIONS = {
        "education": EducationSet,
        "interests": NamedKeywordsSet,
        "languages": LanguageSet,
        "skills": NamedKeywordsSet,
        "volunteer": ExperienceSet,
        "work": ExperienceSet,
    }

    def __init__(self):
        sections = [cls(name) for name, cls in self.SECTIONS.items()]
        super().__init__(sections)

    def clear(self):
        super().clear()
        self.profiles.clear()

        sections = [cls(name) for name, cls in self.SECTIONS.items()]
        for section in sections:
            self.add(section)

    def dump_data(self) -> dict:
        # collect basics
        basics = {getattr(self, f) for f in self.FIELDS}
        basics["profiles"] = [p.dict() for p in self.profiles]  # type: ignore
        data = {"basics": basics}

        # collect sections
        for section_name in self.SECTIONS:
            if not self[section_name]:
                continue

            items = [i.dict(exclude_none=True) for i in self[section_name]]
            data[section_name] = items  # type: ignore

        return data

    def load_data(self, data: dict):
        """Loads the provide rezume data.
        """
        self.clear()
        rezume = RezumeModel(**data)

        # set attribbutes
        basics = rezume.basics
        for f in self.FIELDS:
            value = getattr(basics, f)
            setattr(self, f, value)

        # set profiles
        for profile in rezume.basics.profiles or []:
            self.profiles.add(profile)

        # assign sections
        for section_name in self.SECTIONS:
            if not hasattr(rezume, section_name):
                continue

            section = getattr(rezume, section_name)
            if not section:
                continue

            for item in section:
                self.add_item(section_name, item)

    def load(self, filepath: Path) -> None:
        pass

    def save(self, filepath: Path = None) -> None:
        pass
