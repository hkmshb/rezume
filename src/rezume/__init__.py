from pathlib import Path
from importlib import metadata
from typing import Any, Union
from datetime import date, datetime
from yaml import dump, load, Dumper, Loader, parser
from pydantic import BaseModel, HttpUrl, ValidationError

from .base import RezumeError
from .models import PersonalInfo, Rezume as RezumeModel
from .sections import (
    AwardSet,
    EducationSet,
    ExperienceSet,
    LanguageSet,
    PublicationSet,
    NamedKeywordsSet,
    ReferenceSet,
    RezumeBase,
)


def get_version():
    """Retrieves and returns the package version details.
    """
    return metadata.version("rezume")


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
        "work": ExperienceSet,
        "volunteer": ExperienceSet,
        "education": EducationSet,
        "awards": AwardSet,
        "publications": PublicationSet,
        "skills": NamedKeywordsSet,
        "languages": LanguageSet,
        "interests": NamedKeywordsSet,
        "references": ReferenceSet,
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

    def dump_data(self, exclude_none=True) -> dict:
        def sanitize(value):
            return self._sanitize(value, exclude_none)

        # dump basics
        basics = {}
        for field in self.FIELDS:
            value = getattr(self, field)
            if not value and exclude_none:
                continue
            basics[field] = sanitize(value)

        basics["profiles"] = list(map(sanitize, self.profiles))
        data = {"basics": sanitize(PersonalInfo(**basics))}

        # dump sections
        for section in self.sections:
            if not section:
                continue
            data[section.name] = list(map(sanitize, section))  # type: ignore

        # validate data to be returned to ensure it's well formed
        try:
            RezumeModel(**data)
            return data
        except ValidationError as ex:
            raise RezumeError(f"error: {ex}")

    def load_data(self, data: dict) -> "Rezume":
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

        # allows fluent method chaining on `load_data`
        return self

    def load(self, filepath: Union[str, Path]) -> "Rezume":
        if not isinstance(filepath, Path):
            filepath = Path(filepath)

        if not filepath.exists() or filepath.is_dir():
            raise RezumeError(f"File not found: {filepath}")

        try:
            with filepath.open() as fp:
                content = load(fp, Loader=Loader)
                self.load_data(content)
        except (TypeError, parser.ParserError):
            raise RezumeError(f"Invalid file format: {filepath}")
        except ValidationError as ex:
            raise RezumeError(f"error: {ex}")
        else:
            # allows fluent method chaining on `load`
            return self

    def save(self, filepath: Path, overwrite=False, exclude_none=True) -> None:
        if not isinstance(filepath, Path):
            filepath = Path(filepath)

        if filepath.exists() and not overwrite:
            raise RezumeError("File already exist, set overwrite if intended")

        try:
            with filepath.open("w") as fp:
                content = dump(self.dump_data(exclude_none), Dumper=Dumper)
                fp.write(content)
        except Exception as ex:
            raise RezumeError(f"Save operation failed: {ex}")

    def _sanitize(self, value: Any, exclude_none) -> Any:
        def sanitize(val):
            return self._sanitize(val, exclude_none)

        if isinstance(value, BaseModel):
            return sanitize(value.dict(by_alias=True, exclude_none=exclude_none))
        elif isinstance(value, HttpUrl):
            return str(value)
        elif isinstance(value, (date, datetime)):
            return value.isoformat()
        elif isinstance(value, (list, tuple)):
            return list(map(sanitize, value))
        elif isinstance(value, dict):
            return {key: sanitize(value) for key, value in value.items() if value}
        else:
            return str(value)

    @classmethod
    def is_valid(cls, source: Union[dict, str, Path]) -> bool:
        try:
            cls.validate(source)
            return True
        except RezumeError:
            return False

    @classmethod
    def validate(cls, source: Union[dict, str, Path]):
        if isinstance(source, str):
            source = Path(source)

        func_name = "load_data" if isinstance(source, dict) else "load"
        getattr(Rezume(), func_name)(source)
