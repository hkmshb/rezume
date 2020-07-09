import pkg_resources
from pathlib import Path
from typing import Any, Union
from datetime import date, datetime
from yaml import dump, load, Dumper, Loader
from pydantic import BaseModel, HttpUrl, ValidationError

from .base import RezumeError
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

    NAMED_SECTIONS = {
        "education": EducationSet,
        "interests": NamedKeywordsSet,
        "languages": LanguageSet,
        "skills": NamedKeywordsSet,
        "volunteer": ExperienceSet,
        "work": ExperienceSet,
    }

    def __init__(self):
        sections = [cls(name) for name, cls in self.NAMED_SECTIONS.items()]
        super().__init__(sections)

    def clear(self):
        super().clear()
        self.profiles.clear()

        sections = [cls(name) for name, cls in self.NAMED_SECTIONS.items()]
        for section in sections:
            self.add(section)

    def dump_data(self) -> dict:
        # dump basics
        basics = {}
        for field in self.FIELDS:
            value = getattr(self, field)
            if not value:
                continue
            basics[field] = self._sanitize(value)

        basics["profiles"] = list(map(self._sanitize, self.profiles))
        data = {"basics": basics}

        # dump sections
        for section in self.sections:
            if not section:
                continue
            data[section.name] = list(map(self._sanitize, section))  # type: ignore

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
        for section_name in self.NAMED_SECTIONS:
            if not hasattr(rezume, section_name):
                continue

            section = getattr(rezume, section_name)
            if not section:
                continue

            for item in section:
                self.add_item(section_name, item)

    def load(self, filepath: Union[str, Path]) -> None:
        if not isinstance(filepath, Path):
            filepath = Path(filepath)

        if not filepath.exists() or filepath.is_dir():
            raise RezumeError(f"File not found: {filepath}")

        try:
            with filepath.open() as fp:
                content = load(fp, Loader=Loader)
                self.load_data(content)
        except (TypeError, ValidationError):
            raise RezumeError(f"Invalid file format: {filepath}")

    def save(self, filepath: Path, overwrite=False) -> None:
        if not isinstance(filepath, Path):
            filepath = Path(filepath)

        if filepath.exists() and not overwrite:
            raise RezumeError("File already exist, set overwrite if intended")

        try:
            with filepath.open("w") as fp:
                content = dump(self.dump_data(), Dumper=Dumper)
                fp.write(content)
        except Exception as ex:
            raise RezumeError(f"Save operation failed: {ex}")

    def _sanitize(self, value: Any) -> Any:
        if isinstance(value, BaseModel):
            return self._sanitize(value.dict(exclude_none=True))
        elif isinstance(value, HttpUrl):
            return str(value)
        elif isinstance(value, (date, datetime)):
            return value.isoformat()
        elif isinstance(value, (list, tuple)):
            return list(map(self._sanitize, value))
        elif isinstance(value, dict):
            return {key: self._sanitize(value) for key, value in value.items() if value}
        else:
            return str(value)
