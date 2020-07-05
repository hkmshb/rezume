from collections.abc import MutableSet
from typing import Any, Iterable
from .models import (
    DatedEntry,
    Education,
    Experience,
    Language,
    NamedKeywords,
    Profile,
)


class Section(MutableSet):
    """Represents a section within a Resume.
    """

    def __init__(self, items: Iterable[Any] = None):
        self._items = {self._generate_key(i): i for i in items or []}

    def __contains__(self, item: Any) -> bool:
        key = self._generate_key(item)
        return key in self._items

    def __iter__(self):
        items = sorted(self._items.values(), key=self._sorter)
        return iter(items)

    def __len__(self):
        return len(self._items)

    def _generate_key(self, item):
        return item

    def _sorter(self, item):
        return self._generate_key(item)

    def add(self, item: Any):
        key = self._generate_key(item)
        if key not in self._items:
            self._items[key] = item

    def discard(self, item: Any):
        key = self._generate_key(item)
        if key in self._items:
            del self._items[key]


class NamedSection(Section):
    """Represents a named section within a Resume.
    """

    def __init__(self, name: str, items: Iterable[Any] = None):
        super().__init__(items)
        self.name = name


class TimelinedSection(NamedSection):
    """Represent a section within a Resume with dated entries that can be
    presented in a timeline fashion.
    """

    def __init__(self, name: str, items: Iterable[DatedEntry] = None, reverse=True):
        super().__init__(name, items)
        self.reverse = reverse

    def __iter__(self):
        items = sorted(self._items.values(), key=self._sorter, reverse=self.reverse)
        return iter(items)


class ProfileSet(NamedSection):
    """Represents a set of profiles.
    """

    def _generate_key(self, elem: Profile) -> str:
        return elem.network

    def _sorter(self, elem: Profile) -> str:
        return elem.network


class EducationSet(TimelinedSection):
    """Represents a set of details describing educational qualifications.
    """

    def _generate_key(self, item: Education):
        return f"{item.institution}:{item.study_area}:{item.study_type}"

    def _sorter(self, item: Education):
        return item.start_date


class ExperienceSet(TimelinedSection):
    """Represents a set of details describing work related experiences.
    """

    def _generate_key(self, item: Experience):
        key = f"{item.company}:{item.position}"
        if item.start_date:
            key += f":{item.start_date.strftime('%Y%m')}"
        return key

    def _sorter(self, item: Education):
        return item.start_date


class LanguageSet(NamedSection):
    """Represents a set of spoken languages.
    """

    def _generate_key(self, item: Language):
        return item.language


class NamedKeywordsSet(NamedSection):
    """Represents a set of named keyworks.
    """

    def _generate_key(self, item: NamedKeywords):
        return item.name


class ResumeBase(Section):
    """Represents the base abstraction for a resume which is a collection of
    named sections.
    """

    @property
    def sections(self) -> Iterable[NamedSection]:
        """Returns the sections within a resume.
        """
        return self._items.values()

    def __getitem__(self, section_name):
        if section_name in self._items:
            return self._items[section_name]
        return None

    def _generate_key(self, section: NamedSection):
        return section.name
