from datetime import datetime
from abc import abstractmethod
from collections.abc import MutableSet
from typing import Any, Iterable, Optional

from pydantic import BaseModel


class DatedEntry(BaseModel):
    """Represents an entry having a start and end date.
    """

    start_date: datetime
    end_date: Optional[datetime]


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
    def __init__(self, items: Iterable[Any] = None):
        super().__init__(items)
        if not self.name:
            raise ValueError("section name required")

    @property
    @abstractmethod
    def name(self):
        pass


class TimelinedSection(Section):
    """Represent a section within a Resume with dated entries that can be
    presented in a timeline fashion.
    """

    def __init__(self, items: Iterable[DatedEntry] = None, reverse=True):
        super().__init__(items)
        self.reverse = reverse

    def __iter__(self):
        items = sorted(self._items.values(), key=self._sorter, reverse=self.reverse)
        return iter(items)


class ResumeBase(Section):
    """Represents the base abstraction for a resume which is a collection of
    named sections.
    """

    def __getitem__(self, section_name):
        if section_name in self._items:
            return self._items[section_name]
        return None

    def _generate_key(self, section: NamedSection):
        return section.name
